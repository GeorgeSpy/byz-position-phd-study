"""A2 design-stage simulations: shared synthetic generator and pooled AP_fam.

Protocol v16.5 §6–§8. AP_fam is one-vs-rest average precision per family, with
tie blocks inserted simultaneously (AP = sum_k (R_k - R_{k-1}) P_k), equal weight
per occurrence and macro mean over the frozen family set F0. S is the mean over
the R replicate bases. Contrasts:
  Delta_know   = 1/2 {S(D,V) - mean_l S(D,P_l) + S(F,V) - mean_l S(F,P_l)}
  Delta_logic  = S(D,V) - S(F,V)

The data are synthetic, with arbitrary noise, prevalence and clustering. They show
mechanisms and orders of magnitude, not the performance of the real corpus.
"""
import json
import platform
import sys

import numpy as np

K = 6                                                     # known families in F0
PREV = np.array([.25, .20, .15, .12, .10, .08]) * 0.9     # unknown family: 0.10
NP = 10                                                   # perturbations P_1..P_10
COND = ['FV', 'DV'] + [f'FP{l}' for l in range(NP)] + [f'DP{l}' for l in range(NP)]
C = len(COND)
F_INDEX = [0] + [2 + l for l in range(NP)]                # F-slot of (V, P_1..P_NP)
D_INDEX = [1] + [2 + NP + l for l in range(NP)]           # matching D-slot


def gen(rng, G, alpha, delta, sig_gc, ties, R, symmetrize_fd=False, occ_mean=25):
    """Return group labels, one-hot labels Y (N x K) and probabilities p (C x R x N x K).

    delta: knowledge signal per condition type FV, DV, FP, DP.
    symmetrize_fd: exchange the F and D slots of a whole group with probability 1/2
    (one coin per group, applied to V and every P_l). F and D then have identical
    marginal laws, so the population value of Delta_logic is exactly zero.
    """
    n_g = np.maximum(5, rng.poisson(occ_mean, G))
    grp = np.repeat(np.arange(G), n_g)
    N = grp.size
    p_full = np.r_[PREV, 0.10]
    comp = rng.dirichlet(alpha * p_full * len(p_full), G)        # family composition per group
    y = np.array([rng.choice(K + 1, p=comp[g]) for g in grp])     # K == unknown family
    Y = (y[:, None] == np.arange(K)[None, :]).astype(np.float32)
    u = rng.normal(0, .5, (G, K))[grp]                            # shared group style
    base = 1.5 * Y[None] + u[None] + rng.normal(0, 1, (R, N, K))  # R x N x K
    specs = ['V'] + [f'P{l}' for l in range(NP)]
    noise = {}
    for s in specs:                     # knowledge noise shared by F and D of the same specification
        e_g = rng.normal(0, sig_gc, (G, K))[grp]
        eta = rng.normal(0, .7, (N, K))
        e_gD = rng.normal(0, sig_gc / 2, (G, K))[grp]            # extra group variation of the logic term
        etaD = rng.normal(0, .3, (N, K))
        noise[s] = (e_g + eta, e_gD + etaD)
    sig = np.zeros((C, R, N, K + 1), np.float32)
    for ci, c in enumerate(COND):
        s = 'V' if c[1] == 'V' else 'P' + c[2:]
        dF = delta['F' + c[1]]
        dD = delta['D' + c[1]]
        know = dF * Y + noise[s][0]
        if c[0] == 'D':
            know = know + (dD - dF) * Y + noise[s][1]
        logit = base + know[None] + rng.normal(0, .05, (R, N, K))
        if ties:
            logit = np.round(logit * 2) / 2
        sig[ci, :, :, :K] = logit
        sig[ci, :, :, K] = 0.5
    p = np.exp(sig - sig.max(-1, keepdims=True))
    p = (p / p.sum(-1, keepdims=True))[..., :K]
    if symmetrize_fd:
        swap = rng.integers(0, 2, G).astype(bool)
        mask = swap[grp]
        for fi, di in zip(F_INDEX, D_INDEX):
            old = p[fi][:, mask, :].copy()
            p[fi][:, mask, :] = p[di][:, mask, :]
            p[di][:, mask, :] = old
    return grp, Y, p


def prep(p, Y):
    """Sort once per (condition, base, family); return order, sorted labels, block-end mask."""
    order = np.argsort(-p, axis=2, kind='stable')
    ps = np.take_along_axis(p, order, 2)
    ys = np.take_along_axis(np.broadcast_to(Y[None, None], p.shape), order, 2)
    be = np.ones_like(ps, bool)
    be[:, :, :-1] = ps[:, :, :-1] != ps[:, :, 1:]
    return order, ys, be


def ap_fam(order, ys, be, w):
    """w: (E, N) occurrence weights -> AP (E, C, R, K); NaN where a family has no positives."""
    ws = w[:, order]
    tp = np.cumsum(ws * ys[None], 3)
    nn = np.cumsum(ws, 3)
    P = tp[:, :, :, -1:, :]
    tpe = np.where(be[None], tp, 0.)
    prev = np.zeros_like(tpe)
    prev[:, :, :, 1:] = np.maximum.accumulate(tpe, 3)[:, :, :, :-1]
    with np.errstate(invalid='ignore', divide='ignore'):
        contrib = np.where(be[None] & (tp > prev), (tp - prev) / P * tp / nn, 0.)
        ap = contrib.sum(3)
    ap[np.broadcast_to(P[:, :, :, 0, :] <= 0, ap.shape)] = np.nan
    return ap


def contrasts(ap):
    """AP (E, C, R, K) -> (E, 2): [Delta_know, Delta_logic]. NaN propagates (undefined)."""
    S = ap.mean(2).mean(-1)
    fv, dv = S[:, 0], S[:, 1]
    fp, dp = S[:, 2:2 + NP].mean(1), S[:, 2 + NP:].mean(1)
    return np.stack([.5 * (dv - dp + fv - fp), dv - fv], 1)


def streams(seed, M):
    """Independent random streams: one for the reference values, one child stream per
    Monte Carlo dataset. Changing the number of reference replications leaves the
    experimental datasets unchanged; dataset i can be regenerated from (seed, i)."""
    ref_ss, exp_ss = np.random.SeedSequence(seed).spawn(2)
    return np.random.default_rng(ref_ss), [np.random.default_rng(c) for c in exp_ss.spawn(M)]


def reference_values(cfg, rng, R, Gbig=400, reps=5):
    """Large-G Monte Carlo reference for the population contrasts.

    Returns the mean, its Monte Carlo standard error and the individual replications."""
    vals = []
    for _ in range(reps):
        grp, Y, p = gen(rng, Gbig, cfg['alpha'], cfg['delta'], cfg['sig_gc'], cfg['ties'], R,
                        cfg.get('symmetrize_fd', False))
        o, ys, be = prep(p, Y)
        vals.append(contrasts(ap_fam(o, ys, be, np.ones((1, Y.shape[0]), np.float32)))[0])
    vals = np.array(vals)
    return vals.mean(0), vals.std(0, ddof=1) / np.sqrt(reps), vals


def allocate_h(rng, present, G, m_H):
    """Prespecified label-only allocation of groups to H with family coverage.

    present: (G_pool, K) boolean, family k has positives in group g.
    Families are served from rarest to most frequent (random tie order); each needs m_H
    groups in H. Remaining H slots are filled at random. Returns the selected group indices,
    or None when the coverage rule cannot be met within G groups."""
    G_pool, K = present.shape
    counts = present.sum(0)
    order = np.lexsort((rng.random(K), counts))
    chosen = np.zeros(G_pool, bool)
    for f in order:
        need = m_H - int((chosen & present[:, f]).sum())
        if need <= 0:
            continue
        cand = np.where(~chosen & present[:, f])[0]
        if len(cand) < need:
            return None
        chosen[rng.choice(cand, need, replace=False)] = True
        if chosen.sum() > G:
            return None
    rest = np.where(~chosen)[0]
    chosen[rng.choice(rest, G - int(chosen.sum()), replace=False)] = True
    return np.where(chosen)[0]


def subset_groups(grp, Y, p, keep):
    """Restrict a generated dataset to the groups in keep, re-indexed 0..len(keep)-1."""
    mask = np.isin(grp, keep)
    remap = {int(g): i for i, g in enumerate(keep)}
    return np.array([remap[int(g)] for g in grp[mask]]), Y[mask], p[:, :, mask, :]


def environment():
    import scipy
    out = dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
               argv=sys.argv)
    try:
        import sklearn
        out['sklearn'] = sklearn.__version__
    except ImportError:
        pass
    return out


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, default=lambda x: x.tolist() if hasattr(x, 'tolist') else str(x))

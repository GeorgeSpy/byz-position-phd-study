"""Synthetic paired scores and fixed-family tie-block AP.

Adapted from the supplied A2 design simulations (2026-11-03).
This score-level model does not simulate trained A2 heads or actual chant.
Arrays: condition x repetition x occurrence x family. Unknown-family probability
is retained in the softmax denominator. Missing positive classes propagate NaN.
"""
import numpy as np

K = 6                      # known families in F0
PREV = np.array([.25, .20, .15, .12, .10, .08]) * 0.9   # relative Dirichlet weights; unknown has weight 0.10
R = 5                      # seeds (bases)
NP = 10                    # perturbations
COND = ['FV', 'DV'] + [f'FP{l}' for l in range(NP)] + [f'DP{l}' for l in range(NP)]
C = len(COND)


def gen(rng, G, alpha, delta, sig_gc, ties, occ_mean=25):
    """delta: dict of knowledge signal per condition type FV, DV, FP, DP."""
    n_g = np.maximum(5, rng.poisson(occ_mean, G))
    grp = np.repeat(np.arange(G), n_g)
    N = grp.size
    p_full = np.r_[PREV, 0.10]  # sum 0.91; Dirichlet normalises these relative weights
    # group-specific family composition (clustering of families by work group)
    comp = rng.dirichlet(alpha * p_full * len(p_full), G)
    y = np.array([rng.choice(K + 1, p=comp[g]) for g in grp])   # K == unknown
    Y = (y[:, None] == np.arange(K)[None, :]).astype(np.float32)  # N x K
    u = rng.normal(0, .5, (G, K))[grp]                      # shared group style
    sig = np.zeros((C, R, N, K + 1), np.float32)
    base = 1.5 * Y[None] + u[None] + rng.normal(0, 1, (R, N, K))   # R x N x K
    specs = ['V'] + [f'P{l}' for l in range(NP)]
    kF = {}
    for s in specs:                                          # knowledge noise shared by F and D of the same spec
        e_g = rng.normal(0, sig_gc, (G, K))[grp]
        eta = rng.normal(0, .7, (N, K))
        e_gD = rng.normal(0, sig_gc / 2, (G, K))[grp]       # extra group variation of the logic term
        etaD = rng.normal(0, .3, (N, K))
        kF[s] = (e_g + eta, e_gD + etaD)
    for ci, c in enumerate(COND):
        s = 'V' if c[1] == 'V' else 'P' + c[2:]
        dF = delta['F' + c[1]]; dD = delta['D' + c[1]]
        know = dF * Y + kF[s][0]
        if c[0] == 'D':
            know = know + (dD - dF) * Y + kF[s][1]
        logit = base + know[None] + rng.normal(0, .05, (R, N, K))
        if ties:
            logit = np.round(logit * 2) / 2
        sig[ci, :, :, :K] = logit
        sig[ci, :, :, K] = 0.5                               # unknown family logit
    p = np.exp(sig - sig.max(-1, keepdims=True))
    p = (p / p.sum(-1, keepdims=True))[..., :K]              # C x R x N x K
    return grp, Y, p


def prep(p, Y):
    """Sort once per (c,r,f); return order, sorted labels, block-end mask."""
    order = np.argsort(-p, axis=2, kind='stable')            # C R N K
    ps = np.take_along_axis(p, order, 2)
    ys = np.take_along_axis(np.broadcast_to(Y[None, None], p.shape), order, 2)
    be = np.ones_like(ps, bool)
    be[:, :, :-1] = ps[:, :, :-1] != ps[:, :, 1:]
    return order, ys, be


def ap_fam(order, ys, be, w):
    """w: (E, N) occurrence weights -> AP (E, C, R, K) with tie blocks."""
    ws = w[:, order]                                          # E C R N K
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
    S = ap.mean(2)            # mean over seeds (nan propagates)
    S = S.mean(-1)                                           # macro over F0 -> (E, C)
    fv, dv = S[:, 0], S[:, 1]
    fp, dp = S[:, 2:2 + NP].mean(1), S[:, 2 + NP:].mean(1)
    know = .5 * (dv - dp + fv - fp)
    logic = dv - fv
    return np.stack([know, logic], 1)                         # E x 2


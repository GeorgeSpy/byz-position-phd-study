"""Sensitivity sub-study: per-dataset paired cluster bootstrap-t (A2 protocol, Appendix K §K.8, sensitivity).

Each dataset: B group-bootstrap draws; each draw has an inner delete-one-draw jackknife
(one copy removed when a group was drawn several times). T_b = (theta_b - theta_hat)/SE_b.
One-sided p = (1 + #{T_b >= T}) / (B + 1); Holm at 0.025.

Strict rule (as in the protocol): if the original estimate, its jackknife, or any of the B
draws or their inner jackknives is undefined or has SE <= 0, no p-value is issued for that
dataset. A lenient variant that drops undefined draws is reported only as a diagnostic.
Reference values and datasets use independent random streams (a2_ap.streams).
This is a small sub-study (single base, modest M and B); it does not replace the
full calibration in the pilot.
"""
import argparse
import time

import numpy as np

import a2_ap as s
from oc_jackknife_t import SCEN, cp, holm


def thetas(o, ys, be, Wg, onehot, chunk=150):
    out = []
    for i in range(0, len(Wg), chunk):
        out.append(s.contrasts(s.ap_fam(o, ys, be, (Wg[i:i + chunk] @ onehot.T).astype(np.float32))))
    return np.vstack(out)


def jse(th, G):
    return np.sqrt((G - 1) / G * ((th - th.mean(0)) ** 2).sum(0))


def one(rng, cfg, B, R):
    G = cfg['G']
    grp, Y, p = s.gen(rng, G, cfg['alpha'], cfg['delta'], cfg['sig_gc'], cfg['ties'], R, cfg['symmetrize_fd'])
    onehot = (grp[:, None] == np.arange(G)[None]).astype(np.float32)
    pos_g = onehot.T @ Y
    W = [np.ones(G)] + [1 - np.eye(G)[g] for g in range(G)]
    for d in rng.integers(0, G, (B, G)):
        cnt = np.bincount(d, minlength=G).astype(float)
        W.append(cnt)
        W += [cnt - np.eye(G)[d[j]] for j in range(G)]
    Wg = np.array(W)
    undef = ((Wg @ pos_g) <= 0).any(1)
    if undef[:G + 1].any():
        return dict(defined=False)
    o, ys, be = s.prep(p, Y)
    th = thetas(o, ys, be, Wg, onehot)
    th0, se0 = th[0], jse(th[1:G + 1], G)
    if not (np.isfinite(se0).all() and (se0 > 0).all()):
        return dict(defined=True, se_ok=False)
    Tb = np.full((B, 2), np.nan)
    bad = np.zeros(B, bool)
    for b in range(B):
        i0 = (G + 1) * (b + 1)
        if undef[i0:i0 + G + 1].any():
            bad[b] = True
            continue
        seb = jse(th[i0 + 1:i0 + G + 1], G)
        if not (np.isfinite(seb).all() and (seb > 0).all()):
            bad[b] = True
            continue
        Tb[b] = (th[i0] - th0) / seb
    return dict(defined=True, se_ok=True, th0=th0, se0=se0, T=th0 / se0, Tb=Tb, bad=bad)


def run(a):
    delta, null_exact = SCEN[a.scenario]
    cfg = dict(scenario=a.scenario, G=a.G, alpha=a.alpha, sig_gc=a.sig_gc, ties=a.ties,
               delta=delta, symmetrize_fd=a.symmetrize_fd)
    rng_ref, rngs = s.streams(a.seed, a.M)
    ref, ref_se, ref_vals = s.reference_values(cfg, rng_ref, a.R, reps=a.ref_reps)
    truth = np.where(null_exact, 0., ref)
    null = np.array(null_exact)
    n_def = n_strict = n_len = 0
    rs = np.zeros((a.M, 2), bool)
    rl = np.zeros((a.M, 2), bool)
    cov_s = []; bad_rate = []
    t0 = time.time()
    for i in range(a.M):
        r = one(rngs[i], cfg, a.B, a.R)
        if not r['defined']:
            continue
        n_def += 1
        if not r['se_ok']:
            continue
        good = ~r['bad']
        bad_rate.append(float(r['bad'].mean()))
        if good.any():
            Tb = r['Tb'][good]
            pl = np.array([(1 + (Tb[:, k] >= r['T'][k]).sum()) / (len(Tb) + 1) for k in range(2)])
            rl[i] = holm(pl)
            n_len += 1
        if good.all():
            n_strict += 1
            Tb = r['Tb']
            ps = np.array([(1 + (Tb[:, k] >= r['T'][k]).sum()) / (a.B + 1) for k in range(2)])
            rs[i] = holm(ps)
            qlo, qhi = np.quantile(Tb, [.025, .975], 0)
            cov_s.append((r['th0'] - qhi * r['se0'] <= truth) & (truth <= r['th0'] - qlo * r['se0']))
    fs = int(rs[:, null].any(1).sum()) if null.any() else 0
    fl = int(rl[:, null].any(1).sum()) if null.any() else 0
    return dict(cfg=cfg, R=a.R, B=a.B, seed=a.seed, reference_reps=a.ref_reps, M_planned=a.M, M_defined=n_def,
                M_issued_strict=n_strict, M_issued_lenient=n_len, null_exact=null_exact, truth=truth,
                reference_mc_se=ref_se, reference_values=ref_vals,
                streams='SeedSequence(seed).spawn(2); datasets: child i of stream 2',
                p_issue_strict=n_strict / a.M, p_issue_strict_cp95=cp(n_strict, a.M),
                fwer_strict_unconditional=fs / a.M, fwer_strict_unconditional_cp95=cp(fs, a.M),
                fwer_strict_conditional=(fs / n_strict if n_strict else None),
                fwer_lenient_conditional_diagnostic=(fl / n_len if n_len else None),
                power_strict_unconditional=rs.mean(0),
                coverage95_strict=(np.mean(cov_s, 0) if cov_s else None),
                mean_undefined_draw_rate=(float(np.mean(bad_rate)) if bad_rate else None),
                seconds=round(time.time() - t0, 1), env=s.environment())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--scenario', choices=SCEN, required=True)
    ap.add_argument('--G', type=int, default=12)
    ap.add_argument('--R', type=int, default=1)
    ap.add_argument('--M', type=int, default=100)
    ap.add_argument('--B', type=int, default=199)
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--alpha', type=float, default=2.0)
    ap.add_argument('--sig-gc', dest='sig_gc', type=float, default=0.2)
    ap.add_argument('--ties', action='store_true')
    ap.add_argument('--symmetrize-fd', dest='symmetrize_fd', action='store_true')
    ap.add_argument('--ref-reps', dest='ref_reps', type=int, default=20)
    print(s.dump(run(ap.parse_args())))

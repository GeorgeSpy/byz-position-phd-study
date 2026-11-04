"""Operating characteristics of the primary candidate procedure of the A2 protocol, Appendix K §K.8.

For each contrast theta in {Delta_know, Delta_logic}:
  theta_hat  original pooled estimate on all G groups (not the jackknife mean, not bias-corrected)
  SE_J       = sqrt((G-1)/G * sum_g (theta_(-g) - mean_g theta_(-g))^2)  (delete one work-source group)
  T          = theta_hat / SE_J,  one-sided p = 1 - F_t(T; G-1)
Holm over the two contrasts at family level 0.025.

Issuance rule: the original estimate and all G delete-one estimates are defined
(every family of F0 has positives in every delete-one sample), and SE_J is finite
and > 0 for both contrasts. Otherwise no confirmatory p-value is issued.

Exact nulls: H1 (Delta_know = 0) when V and P have equal laws (FV=FP, DV=DP);
H2 (Delta_logic = 0) by groupwise F/D exchange (--symmetrize-fd). Both remain exact
under the label-only allocation of groups to H.

Random streams: the reference values and every Monte Carlo dataset use independent
streams spawned from --seed, so changing --ref-reps does not change the datasets.

--allocate-h: each dataset first generates a pool of ceil(pool_factor*G) groups and
selects the G groups of H with the prespecified coverage rule (every family in at least
m_H groups of H; a2_ap.allocate_h). Allocation failures count as non-issued. Under this
design the evaluation distribution differs from simple group sampling, so coverage is
reported only for components with an exact null value; estimates and SDs are reported
for the others.

Denominators reported separately: planned, allocated, defined, issued. FWER and power
are given over all planned datasets (non-issued counted as non-rejection) and
conditionally on issuance, with Clopper-Pearson 95% Monte Carlo intervals.
"""
import argparse
import math
import time
import warnings

import numpy as np
from scipy.stats import beta, t as tdist

import a2_ap as s

SCEN = {
    'null':       (dict(FV=.5, DV=.555, FP=.5, DP=.555), [True, True]),
    'partial':    (dict(FV=.8, DV=.855, FP=.5, DP=.555), [False, True]),
    'logic_only': (dict(FV=.5, DV=.855, FP=.5, DP=.855), [True, False]),
    'alt':        (dict(FV=.62, DV=.775, FP=.5, DP=.555), [False, False]),
}


def cp(k, n):
    if n == 0:
        return [None, None]
    lo = float(beta.ppf(.025, k, n - k + 1)) if k > 0 else 0.
    hi = float(beta.ppf(.975, k + 1, n - k)) if k < n else 1.
    return [lo, hi]


def holm(p, alpha=.025):
    rej = np.zeros(2, bool)
    i = int(np.argmin(p))
    if p[i] <= alpha / 2:
        rej[i] = True
        if p[1 - i] <= alpha:
            rej[1 - i] = True
    return rej


def one(rng, cfg, R, alloc):
    G = cfg['G']
    info = {}
    if alloc:
        G_pool = int(math.ceil(alloc['pool_factor'] * G))
        grp, Y, p = s.gen(rng, G_pool, cfg['alpha'], cfg['delta'], cfg['sig_gc'], cfg['ties'], R,
                          cfg['symmetrize_fd'])
        oh = (grp[:, None] == np.arange(G_pool)[None]).astype(np.float32)
        present = (oh.T @ Y) > 0
        keep = s.allocate_h(rng, present, G, alloc['m_H'])
        if keep is None:
            return dict(allocated=False)
        rest = np.setdiff1d(np.arange(G_pool), keep)
        info['dev_min_groups_per_family'] = int(present[rest].sum(0).min())
        grp, Y, p = s.subset_groups(grp, Y, p, keep)
    else:
        grp, Y, p = s.gen(rng, G, cfg['alpha'], cfg['delta'], cfg['sig_gc'], cfg['ties'], R, cfg['symmetrize_fd'])
    onehot = (grp[:, None] == np.arange(G)[None]).astype(np.float32)
    pos_g = onehot.T @ Y                                         # G x K
    info['h_min_groups_per_family'] = int((pos_g > 0).sum(0).min())
    info['prevalence'] = (Y.sum(0) / len(Y)).round(4)
    Wg = np.vstack([np.ones(G), 1 - np.eye(G)])                  # original + delete-one
    if not bool(((Wg @ pos_g) > 0).all()):
        return dict(allocated=True, defined=False, **info)
    o, ys, be = s.prep(p, Y)
    th = s.contrasts(s.ap_fam(o, ys, be, (Wg @ onehot.T).astype(np.float32)))
    th0, jk = th[0], th[1:]
    se = np.sqrt((G - 1) / G * ((jk - jk.mean(0)) ** 2).sum(0))
    ok_se = bool(np.isfinite(se).all() and (se > 0).all() and np.isfinite(th0).all())
    return dict(allocated=True, defined=True, se_ok=ok_se, th0=th0, se=se, **info)


def run(a):
    warnings.filterwarnings('ignore', message='Mean of empty slice')
    delta, null_exact = SCEN[a.scenario]
    cfg = dict(scenario=a.scenario, G=a.G, alpha=a.alpha, sig_gc=a.sig_gc, ties=a.ties,
               delta=delta, symmetrize_fd=a.symmetrize_fd)
    if null_exact[1] and not a.symmetrize_fd:
        raise SystemExit('H2 null requires --symmetrize-fd for an exact boundary value')
    alloc = dict(pool_factor=a.pool_factor, m_H=a.m_H) if a.allocate_h else None
    rng_ref, rngs = s.streams(a.seed, a.M)
    null = np.array(null_exact)
    if alloc:
        ref = ref_se = ref_vals = None
        truth = np.where(null, 0., np.nan)
    else:
        ref, ref_se, ref_vals = s.reference_values(cfg, rng_ref, a.R, Gbig=a.ref_G, reps=a.ref_reps)
        truth = np.where(null, 0., ref)
    q = tdist.ppf(.975, a.G - 1)
    planned = a.M
    n_alloc = n_def = n_iss = 0
    rej_all = np.zeros((planned, 2), bool)
    issued = np.zeros(planned, bool)
    cov2 = []; cov1 = []; est = []; ses = []; idx = []
    hmin = []; dmin = []; prev = []
    t0 = time.time()
    for i in range(planned):
        r = one(rngs[i], cfg, a.R, alloc)
        if not r['allocated']:
            continue
        n_alloc += 1
        hmin.append(r['h_min_groups_per_family']); prev.append(r['prevalence'])
        if 'dev_min_groups_per_family' in r:
            dmin.append(r['dev_min_groups_per_family'])
        if not r['defined']:
            continue
        n_def += 1
        if not r['se_ok']:
            continue
        n_iss += 1; issued[i] = True
        T = r['th0'] / r['se']
        pv = 1 - tdist.cdf(T, a.G - 1)
        rej_all[i] = holm(pv)
        cov2.append((r['th0'] - q * r['se'] <= truth) & (truth <= r['th0'] + q * r['se']))
        cov1.append(r['th0'] - q * r['se'] <= truth)
        est.append(r['th0']); ses.append(r['se']); idx.append(i)
    fr = rej_all[:, null].any(1) if null.any() else np.zeros(planned, bool)
    k_f = int(fr.sum())
    cov2 = np.array(cov2, float); cov1 = np.array(cov1, float)
    if alloc and len(cov2):
        cov2[:, ~null] = np.nan; cov1[:, ~null] = np.nan
    est = np.array(est); ses = np.array(ses)
    out = dict(cfg=cfg, R=a.R, seed=a.seed, allocation=alloc, streams='SeedSequence(seed).spawn(2); datasets: child i of stream 2',
               M_planned=planned, M_allocated=n_alloc, M_defined=n_def, M_issued=n_iss,
               p_issue=n_iss / planned, p_issue_cp95=cp(n_iss, planned),
               null_exact=null_exact, truth=truth, reference_mc_se=ref_se, reference_values=ref_vals,
               reference_G=a.ref_G, reference_reps=(None if alloc else a.ref_reps),
               fwer_unconditional=k_f / planned, fwer_unconditional_cp95=cp(k_f, planned),
               fwer_conditional=(k_f / n_iss if n_iss else None), fwer_conditional_cp95=cp(k_f, n_iss),
               rejections=rej_all.sum(0),
               power_unconditional=rej_all.mean(0),
               power_conditional=(rej_all[issued].mean(0) if n_iss else None),
               coverage95_two_sided=(np.nanmean(cov2, 0) if len(cov2) else None),
               coverage975_lower_bound=(np.nanmean(cov1, 0) if len(cov1) else None),
               mean_estimate=(est.mean(0) if len(est) else None),
               mean_se=(ses.mean(0) if len(ses) else None),
               sd_estimate=(est.std(0, ddof=1) if len(est) > 1 else None),
               bias=(est.mean(0) - truth if len(est) and not alloc else None),
               h_min_groups_per_family_mean=(float(np.mean(hmin)) if hmin else None),
               dev_min_groups_per_family_min=(int(np.min(dmin)) if dmin else None),
               dev_some_family_below_2_groups_rate=(float(np.mean(np.array(dmin) < 2)) if dmin else None),
               mean_prevalence=(np.mean(prev, 0).round(4) if prev else None),
               per_rep_index_estimate_se=(np.hstack([np.array(idx)[:, None], est, ses]).round(6) if len(est) else None),
               seconds=round(time.time() - t0, 1), env=s.environment())
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--scenario', choices=SCEN, required=True)
    ap.add_argument('--G', type=int, default=12)
    ap.add_argument('--R', type=int, default=1)
    ap.add_argument('--M', type=int, default=1000)
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--alpha', type=float, default=2.0, help='Dirichlet concentration of family composition per group')
    ap.add_argument('--sig-gc', dest='sig_gc', type=float, default=0.2)
    ap.add_argument('--ties', action='store_true')
    ap.add_argument('--symmetrize-fd', dest='symmetrize_fd', action='store_true')
    ap.add_argument('--ref-G', dest='ref_G', type=int, default=400)
    ap.add_argument('--ref-reps', dest='ref_reps', type=int, default=20)
    ap.add_argument('--allocate-h', dest='allocate_h', action='store_true')
    ap.add_argument('--pool-factor', dest='pool_factor', type=float, default=2.5)
    ap.add_argument('--m-H', dest='m_H', type=int, default=3)
    print(s.dump(run(ap.parse_args())))

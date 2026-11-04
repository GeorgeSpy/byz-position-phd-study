"""Where to fit the knowledge heads (w, lambda) on a frozen base (A2 protocol, Appendix K §K.7).

Occurrences belong to work-source groups; all splits are by group.
  A_train  heads on the base's own training groups (previous revision), temperature on internal development
  B_dev    heads on the internal development groups, where the temperature is also fitted (current revision)
  C_cross  sensitivity only: grouped 5-fold cross-fitting on training groups; heads and temperature
           on out-of-fold logits; on H the five fold models' logits are averaged (a model
           combination, which itself can change the scores), scaled by the same temperature.
           Fold group IDs and convergence flags are recorded.
The base model sees features that are independent of the concepts given the family.
The specification V comes from the generator bank. If a family of F0 has no positives in H,
AP_fam is undefined and the replication is counted as undefined (not skipped per family).
"""
import argparse
import json
import warnings

import numpy as np
from scipy.optimize import minimize
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score as aps
from sklearn.model_selection import GroupKFold

import a2_ap
import generator_feasibility as g1

warnings.filterwarnings('ignore')


def qv_all(X, specs):
    Q, _, v = zip(*[g1.Q_phi(X, s) for s in specs])
    return np.stack(Q, 1), np.stack(v, 1)


def logits(b, T, Q, v, w, lam):
    K = Q.shape[1]
    L = (b / T).copy()
    L[:, :K] += Q @ w - lam * v
    return L


def nll(L, y):
    L = L - L.max(1, keepdims=True)
    return -(L[np.arange(len(y)), y] - np.log(np.exp(L).sum(1))).mean()


def fit_T(b, y):
    r = minimize(lambda t: nll(b / np.exp(t[0]), y), [0.], method='L-BFGS-B')
    return float(np.exp(r.x[0]))


def fit_head(b, T, Q, v, y, structured):
    def unpack(x):
        e = np.exp(x[:3] - x[:3].max())
        w = .1 + .7 * e / e.sum()                  # W = {sum w = 1, w_r >= 0.1}
        return w, (x[3] if structured else 0.)
    best = None
    for start in ([0, 0, 0, .5], [1, 0, -1, 1.5], [-1, 1, 0, .1]):
        r = minimize(lambda x: nll(logits(b, T, Q, v, *unpack(x)), y), np.array(start, float),
                     method='L-BFGS-B', bounds=[(-8, 8)] * 3 + [(0, 2)])
        if best is None or r.fun < best.fun:
            best = r
    return unpack(best.x)


def ap_fam(L, y, K):
    if not all((y == f).any() for f in range(K)):
        return np.nan
    p = np.exp(L - L.max(1, keepdims=True))
    p /= p.sum(1, keepdims=True)
    return float(np.mean([aps(y == f, p[:, f]) for f in range(K)]))


def one(seed, C_reg, G_tr=24, G_dev=8, G_H=16, occ=30, d=40, sep=.35, sd_group=.5):
    rng = np.random.default_rng(seed)
    K = 6
    concepts = g1.make_bank(rng, True)
    specs = g1.make_specs(rng, concepts, K)
    G = G_tr + G_dev + G_H
    n_g = np.maximum(10, rng.poisson(occ, G))
    grp = np.repeat(np.arange(G), n_g)
    N = grp.size
    comp = rng.dirichlet(np.full(K + 1, 2.), G)
    y = np.array([rng.choice(K + 1, p=comp[gg]) for gg in grp])
    _, X = g1.simulate_data(rng, concepts, specs, N)
    # re-draw concept states conditional on the group-assigned family
    Xf = np.zeros_like(X)
    for f in range(K + 1):
        idx = np.where(y == f)[0]
        if len(idx):
            yy, XX = g1.simulate_data(rng, concepts, specs, 4 * len(idx) + 50)
            pool = np.where(yy == f)[0]
            Xf[idx] = XX[rng.choice(pool, len(idx), replace=True)]
    X = Xf
    mu = rng.normal(0, sep, (K + 1, d))
    F = mu[y] + rng.normal(0, sd_group, (G, d))[grp] + rng.normal(0, 1, (N, d))
    Q, v = qv_all(X, specs)
    perm = rng.permutation(G)
    gtr, gdv, gH = perm[:G_tr], perm[G_tr:G_tr + G_dev], perm[G_tr + G_dev:]
    tr, dv, H = (np.where(np.isin(grp, s))[0] for s in (gtr, gdv, gH))
    base = LogisticRegression(C=C_reg, max_iter=3000).fit(F[tr], y[tr])
    converged = [bool(np.max(base.n_iter_) < 3000)]
    folds = []
    b = base.decision_function(F)
    T = fit_T(b[dv], y[dv])
    oof = np.zeros((len(tr), K + 1))
    bH_cf = np.zeros((len(H), K + 1))
    for a, c in GroupKFold(5).split(tr, groups=grp[tr]):
        m = LogisticRegression(C=C_reg, max_iter=3000).fit(F[tr][a], y[tr][a])
        converged.append(bool(np.max(m.n_iter_) < 3000))
        folds.append(sorted(int(x) for x in np.unique(grp[tr][c])))
        oof[c] = m.decision_function(F[tr][c])
        bH_cf += m.decision_function(F[H]) / 5
    T_oof = fit_T(oof, y[tr])
    out = dict(seed=seed, C=C_reg, T_dev=round(T, 3), T_oof=round(T_oof, 3),
               cross_fit_fold_groups=folds, base_models_converged=all(converged),
               base_AP_H=ap_fam(b[H] / T, y[H], K))
    alloc = dict(A_train=(b[tr], T, tr, b[H], T), B_dev=(b[dv], T, dv, b[H], T),
                 C_cross=(oof, T_oof, tr, bH_cf, T_oof))
    for name, (bb, TT, idx, bH, TH) in alloc.items():
        wF, _ = fit_head(bb, TT, Q[idx], v[idx], y[idx], False)
        wD, lam = fit_head(bb, TT, Q[idx], v[idx], y[idx], True)
        apF = ap_fam(logits(bH, TH, Q[H], v[H], wF, 0.), y[H], K)
        apD = ap_fam(logits(bH, TH, Q[H], v[H], wD, lam), y[H], K)
        out[name] = dict(lam=float(lam), wF=np.round(wF, 3), wD=np.round(wD, 3), apF=apF, apD=apD,
                         d_logic=apD - apF, nllD_H=nll(logits(bH, TH, Q[H], v[H], wD, lam), y[H]))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--C', type=float, required=True, help='inverse L2 strength of the base model')
    ap.add_argument('--n', type=int, default=60)
    ap.add_argument('--seed0', type=int, default=5000)
    a = ap.parse_args()
    env = a2_ap.environment()
    for s in range(a.n):
        r = one(a.seed0 + s, a.C)
        r['env'] = env
        print(a2_ap.dump(r), flush=True)

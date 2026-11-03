"""Grouped known-boundary prototype: head fitting on train vs held-out groups.

A/B share the same final base and temperature. C is a separately labelled,
more expensive grouped cross-fit/ensemble sensitivity with each fold model's
calibration applied consistently at head fitting and prediction. This toy
logistic base probes mechanisms; the real frozen A requires a full pilot.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import softmax, logsumexp
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import average_precision_score
from synthetic_concepts import make_bank, make_specs, simulate_data, evaluate


def nll(b, y):
    return float(np.mean(logsumexp(b, axis=1)-b[np.arange(len(y)), y]))


def temperature(b, y):
    r = minimize_scalar(lambda z: nll(b/np.exp(z), y), bounds=(-4, 4), method='bounded')
    if not r.success:
        raise RuntimeError('temperature fit failed')
    return float(np.exp(r.x))


def head_logits(b, Q, v, w, lam):
    z = b.copy(); z[:, :Q.shape[1]] += Q@w-lam*v
    return z


def fit_head(b, Q, v, y, structured):
    def objective(x):
        return nll(head_logits(b, Q, v, x[:3], x[3] if structured else 0.), y)
    r = minimize(objective, [.34, .33, .33, .5 if structured else 0.], method='SLSQP',
                 bounds=[(.1, .8)]*3+([(0., 2.)] if structured else [(0., 0.)]),
                 constraints=[dict(type='eq', fun=lambda x: x[:3].sum()-1)],
                 options=dict(ftol=1e-10, maxiter=300))
    if not r.success or abs(r.x[:3].sum()-1) > 1e-7:
        raise RuntimeError('head fit failed: '+r.message)
    return r.x[:3], float(r.x[3])


def ap_fixed(prob, y, K):
    if any(not np.any(y == f) for f in range(K)):
        return None
    return float(np.mean([average_precision_score(y == f, prob[:, f]) for f in range(K)]))


def base_fit(F, y, ix, K, C):
    model = LogisticRegression(C=C, max_iter=2000).fit(F[ix], y[ix])
    if not np.array_equal(model.classes_, np.arange(K+1)) or model.n_iter_.max() >= 2000:
        raise RuntimeError('base class coverage/convergence failed')
    return model


def one(seed=5000, C=100., group_count=30, per_group=25, dimension=40):
    rng = np.random.default_rng(seed); K = 6
    bank = make_bank(rng, True); specs = make_specs(rng, bank, K)
    y, X = simulate_data(rng, bank, specs, group_count*per_group)
    group = np.repeat(np.arange(group_count), per_group)
    mu = rng.normal(0, .35, (K+1, dimension))
    shared = rng.normal(0, .3, (group_count, dimension))
    F = mu[y]+shared[group]+rng.normal(0, 1, (len(y), dimension))
    Q, v, _ = zip(*(evaluate(X, s) for s in specs))
    Q, v = np.stack(Q, 1), np.stack(v, 1)
    train = np.flatnonzero(group < 16)
    dev = np.flatnonzero((group >= 16) & (group < 22))
    H = np.flatnonzero(group >= 22)
    base = base_fit(F, y, train, K, C)
    b = base.decision_function(F); T = temperature(b[dev], y[dev]); calibrated = b/T
    out = dict(seed=seed, C=C, fixed_families=K, final_temperature=T,
               final_base_AP=ap_fixed(softmax(calibrated[H], axis=1), y[H], K), methods={})
    def record(name, fit_scores, ix, test_scores):
        wF, _ = fit_head(fit_scores, Q[ix], v[ix], y[ix], False)
        wD, lam = fit_head(fit_scores, Q[ix], v[ix], y[ix], True)
        pF = np.mean([softmax(head_logits(bb, Q[H], v[H], wF, 0), axis=1) for bb in test_scores], axis=0)
        pD = np.mean([softmax(head_logits(bb, Q[H], v[H], wD, lam), axis=1) for bb in test_scores], axis=0)
        apF, apD = ap_fixed(pF, y[H], K), ap_fixed(pD, y[H], K)
        out['methods'][name] = dict(lambda_hat=lam, lambda_below_point1=lam < .1,
            lambda_at_upper=lam >= 2-1e-5, wF=wF.tolist(), wD=wD.tolist(),
            AP_F=apF, AP_D=apD, delta_logic=apD-apF if apF is not None and apD is not None else None)
    record('A_base_training_groups', calibrated[train], train, [calibrated[H]])
    record('B_held_out_head_groups', calibrated[dev], dev, [calibrated[H]])
    oof = np.zeros((len(train), K+1)); test_scores=[]; temperatures=[]
    for a, c in GroupKFold(5).split(F[train], y[train], group[train]):
        m = base_fit(F, y, train[a], K, C)
        t = temperature(m.decision_function(F[dev]), y[dev])
        oof[c] = m.decision_function(F[train[c]])/t
        test_scores.append(m.decision_function(F[H])/t); temperatures.append(t)
    record('C_group_crossfit_ensemble_sensitivity', oof, train, test_scores)
    out['crossfit_temperatures'] = temperatures
    out['crossfit_base_AP'] = ap_fixed(np.mean([softmax(bb, axis=1) for bb in test_scores], axis=0), y[H], K)
    out['scope'] = 'grouped synthetic logistic prototype; C uses five additional bases and an ensemble'
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seed', type=int, default=5000)
    p.add_argument('--repeats', type=int, default=10)
    p.add_argument('--C', type=float, default=100.)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    rows = [one(seed=a.seed+i, C=a.C) for i in range(a.repeats)]
    result = json.dumps(rows, indent=2, allow_nan=False)
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True); a.output.write_text(result+'\n')
    print(result)

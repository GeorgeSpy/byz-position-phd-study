"""Score-level feasibility of paired group jackknife + Student t + Holm.

Nulls are constructed by equal V/P laws and/or groupwise F/D exchanges.
Coverage is reported only for certified zero contrasts. Five repeated score
panels are default; they represent synthetic variation, not fitted checkpoints.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
from scipy.stats import beta, t
import synthetic_scores as s


def interval(k, n):
    if not n:
        return None
    return [float(beta.ppf(.025, k, n-k+1)) if k else 0.,
            float(beta.ppf(.975, k+1, n-k)) if k < n else 1.]


def holm(p, alpha=.025):
    ix = np.argsort(p)
    out = np.zeros(2, dtype=bool)
    out[ix[0]] = p[ix[0]] <= alpha/2
    out[ix[1]] = out[ix[0]] and p[ix[1]] <= alpha
    return out


def generate(rng, G, scenario, concentration, ties):
    alternative = scenario == 'h2_null'
    delta = dict(FV=.8 if alternative else .5,
                 DV=.855 if alternative else .555, FP=.5, DP=.555)
    if scenario == 'h1_null':
        delta = dict(FV=.5, DV=.855, FP=.5, DP=.855)
    group, labels, scores = s.gen(rng, G, concentration, delta, .2, ties)
    if scenario != 'h1_null':
        # Makes F and D identically distributed, hence H2 = 0.
        # Pooled AP is nonlinear: this exchange also changes the H1 alternative.
        for g in range(G):
            if rng.integers(2):
                mask = group == g
                for fi, di in [(0, 1)] + [(2+j, 2+s.NP+j) for j in range(s.NP)]:
                    old = scores[fi][:, mask, :].copy()
                    scores[fi][:, mask, :] = scores[di][:, mask, :]
                    scores[di][:, mask, :] = old
    return group, labels, scores


def estimate(group, labels, scores, G):
    order, ys, ends = s.prep(scores, labels)
    onehot = (group[:, None] == np.arange(G)[None]).astype(float)
    W = np.vstack([np.ones(G), np.ones((G, G))-np.eye(G)])
    theta = s.contrasts(s.ap_fam(order, ys, ends, (W @ onehot.T).astype(np.float32)))
    if not np.isfinite(theta).all():
        return None, 'undefined_fixed_family_AP'
    se = np.sqrt((G-1)/G * ((theta[1:]-theta[1:].mean(0))**2).sum(0))
    if not (np.isfinite(se).all() and (se > 0).all()):
        return None, 'nonpositive_or_nonfinite_SE'
    return (theta[0], se), None


def run(M=1000, G=12, R=5, scenario='both_null', concentration=2., ties=False, seed=20261103):
    if M < 1 or G < 3 or R < 1 or concentration <= 0:
        raise ValueError('Require M>=1, G>=3, R>=1, concentration>0')
    s.R = R
    rng = np.random.default_rng(seed)
    null = np.array([scenario != 'h2_null', scenario != 'h1_null'])
    n = false = 0
    rejects = np.zeros(2, int)
    covered = np.zeros(2, int)
    invalid = {}
    start = time.time()
    for _ in range(M):
        group, labels, scores = generate(rng, G, scenario, concentration, ties)
        value, reason = estimate(group, labels, scores, G)
        if reason:
            invalid[reason] = invalid.get(reason, 0)+1
            continue
        th, se = value
        reject = holm(t.sf(th/se, G-1))
        rejects += reject
        false += int(reject[null].any())
        n += 1
        q = t.ppf(.975, G-1)
        covered += ((th-q*se <= 0) & (0 <= th+q*se))
    contrasts = []
    for k, name in enumerate(['knowledge', 'logic_valid']):
        contrasts.append(dict(name=name, exact_zero_null=bool(null[k]), rejections=int(rejects[k]),
            rejection_rate_given_valid=float(rejects[k]/n) if n else None,
            rejection_rate_all=float(rejects[k]/M),
            coverage_95_given_valid=float(covered[k]/n) if n and null[k] else None,
            coverage_mc95=interval(int(covered[k]), n) if null[k] else None))
    return dict(scenario=scenario, M=M, G=G, R=R, perturbations=s.NP, seed=seed,
        concentration=concentration, ties=ties, valid=n, invalid_reasons=invalid,
        probability_valid=n/M, probability_valid_mc95=interval(n, M),
        false_rejections=false, fwer_given_valid=false/n if n else None,
        fwer_given_valid_mc95=interval(false, n), fwer_all=false/M,
        fwer_all_mc95=interval(false, M), contrasts=contrasts,
        seconds=time.time()-start, scope='synthetic score panels; fixed family set; no model fitting')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--M', type=int, default=1000)
    p.add_argument('--G', type=int, default=12)
    p.add_argument('--R', type=int, default=5)
    p.add_argument('--scenario', choices=['both_null', 'h1_null', 'h2_null'], default='both_null')
    p.add_argument('--concentration', type=float, default=2.)
    p.add_argument('--ties', action='store_true', help='quantise logits before softmax; probabilities may still be distinct')
    p.add_argument('--seed', type=int, default=20261103)
    p.add_argument('--output', type=Path)
    a = vars(p.parse_args()); output = a.pop('output')
    result = json.dumps(run(**a), indent=2, allow_nan=False)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result+'\n')
    print(result)

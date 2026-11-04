"""Label-free synthetic search for ten genuinely distinct A2 perturbations.

Tests observed support, canonical cards and Q/v signatures. Numerical LP
bounds cover independently refitted weights and lambda in [0,2]. Expert
semantic judgement and a real corpus are separate feasibility requirements.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from synthetic_concepts import make_bank, make_specs, simulate_data, evaluate, apply_tau, propose, TOL


def canonical(specs):
    return tuple((tuple(sorted(s['R'])),
                  tuple(sorted(tuple(sorted(g)) for g in s['G'])),
                  tuple(sorted(s['E']))) for s in specs)


def summary(X, specs):
    q, v, phi = zip(*(evaluate(X, s) for s in specs))
    return np.vstack(q), np.concatenate(v), np.stack(phi)


def signature(q, v):
    # Same ordered Omega and family order for every candidate.
    return hashlib.sha256(np.round(np.c_[q, v], 12).tobytes()).hexdigest()


def lp_bound(QV, vV, QP, vP, structured):
    A = np.c_[QV, -QP, -vV, vP] if structured else np.c_[QV, -QP]
    A = np.unique(A, axis=0)
    n = A.shape[1]
    c = np.r_[np.zeros(n), 1.]
    U = np.vstack([np.c_[A, -np.ones(len(A))], np.c_[-A, -np.ones(len(A))]])
    E = np.zeros((2, n+1)); E[0, :3] = 1; E[1, 3:6] = 1
    # w<=0.8 follows from w>=0.1 and sum(w)=1. t<=6 is redundant:
    # all score differences lie within [-4,4] for lambda in [0,2].
    bounds = [(.1, .8)]*6 + ([(0., 2.)]*2 if structured else []) + [(0., 6.)]
    result = linprog(c, A_ub=U, b_ub=np.zeros(len(U)), A_eq=E,
                     b_eq=np.ones(2), bounds=bounds, method='highs')
    if not result.success:
        return dict(verified=False, status=int(result.status), message=result.message)
    lo, hi = np.array(bounds).T
    x = result.x
    primal_residual = max(0., float((U@x).max()), float(np.abs(E@x-1).max()),
                          float((lo-x).max()), float((x-hi).max()))
    # Any y<=0 and unrestricted z yield a valid box-Lagrangian lower bound.
    # Recompute it rather than trusting the solver's objective alone.
    y = np.minimum(result.ineqlin.marginals, 0.)
    z = result.eqlin.marginals
    residual = c-U.T@y-E.T@z
    lower = float(z.sum() + np.sum(residual*np.where(residual >= 0, lo, hi))) - 1e-10
    gap = float(result.fun-lower)
    return dict(verified=bool(primal_residual < 1e-8 and -1e-8 <= gap < 1e-7),
                primal=float(result.fun), lower=lower, gap=gap, primal_residual=primal_residual,
                primal_solution=x.tolist(), dual_equalities=z.tolist(),
                dual_inequalities_nonzero=[[int(i), float(v)] for i, v in enumerate(y) if abs(v) > 1e-12])


def run(seed=400, families=4, rich=True, N=300, cap=100000, target=10, seconds=60.):
    if families not in (4, 6) or N < 1 or cap < 1 or target < 1 or seconds <= 0:
        raise ValueError('Require families=4/6, positive N/cap/target/seconds')
    rng = np.random.default_rng(seed)
    concepts = make_bank(rng, rich)
    V = make_specs(rng, concepts, families)
    _, X = simulate_data(rng, concepts, V, N)  # discard synthetic labels here
    return search(rng, concepts, V, X, seed, rich, cap, target, seconds)


def search(rng, concepts, V, X, seed, rich, cap, target, seconds):
    start = time.time()
    Omega = np.unique(X, axis=0)
    QV, vV, phiV = summary(Omega, V)
    used = sorted({j for s in V for j in s['R']+sum(s['G'], [])+s['E']})
    obs = X >= 0
    frequency = (X == 1).sum(0)/np.maximum(obs.sum(0), 1)
    missing = 1-obs.mean(0)
    reasons, accepted = {}, []
    def reject(reason):
        reasons[reason] = reasons.get(reason, 0)+1
    keys = {canonical(V)}
    signatures = {signature(QV, vV)}
    if not ((phiV == 1).any(1).all() and (phiV == 0).any(1).all()):
        return dict(seed=seed, accepted=[], stop='valid_spec_lacks_true_or_false_support',
                    proposals=0, reasons={}, seconds=time.time()-start)
    proposals = 0
    while proposals < cap and len(accepted) < target and time.time()-start < seconds:
        proposals += 1
        tau = propose(rng, concepts, set(used), frequency, missing, smart=True)
        if any(abs(frequency[tau[j]]-frequency[j]) > TOL or
               abs(missing[tau[j]]-missing[j]) > TOL for j in used):
            reject('tolerance'); continue
        P = [apply_tau(s, tau) for s in V]
        if any(canonical([v]) == canonical([p]) for v, p in zip(V, P)):
            reject('unchanged_family'); continue
        key = canonical(P)
        if key in keys:
            reject('canonical_duplicate'); continue
        QP, vP, phiP = summary(Omega, P)
        sig = signature(QP, vP)
        if sig in signatures:
            reject('observed_Qv_duplicate'); continue
        if not (phiP == 1).any(1).all():
            reject('no_true_support'); continue
        if not (phiP == 0).any(1).all():
            reject('no_false_support'); continue
        f = lp_bound(QV, vV, QP, vP, False)
        d = lp_bound(QV, vV, QP, vP, True)
        if not (f['verified'] and d['verified'] and f['lower'] > 1e-6 and d['lower'] > 1e-6):
            reject('LP_separation'); continue
        only_E = sum(canonical([dict(v, E=[])]) == canonical([dict(p, E=[])]) for v, p in zip(V, P))
        agreement = float(np.mean(vV == vP))
        pair_agreement = [float(np.mean(vP == np.array(a['v_signature']))) for a in accepted]
        accepted.append(dict(tau=tau.tolist(), specs=P, dF=f, dD=d,
                             changed_only_E=int(only_E), valid_v_agreement=agreement,
                             earlier_v_agreement=pair_agreement, v_signature=vP.tolist()))
        keys.add(key); signatures.add(sig)
    stop = 'target_reached' if len(accepted) == target else ('proposal_cap' if proposals == cap else 'time_limit')
    for a in accepted:
        a.pop('v_signature')
    return dict(seed=seed, rich=rich, families=len(V), N=len(X), concepts=len(concepts),
                Omega=len(Omega), witness_sha256=hashlib.sha256(Omega.tobytes()).hexdigest(),
                valid_specs=V, concept_bank=concepts, frequency=frequency.tolist(), missingness=missing.tolist(),
                proposal_cap=cap, target=target, proposals=proposals,
                accepted=accepted, stop=stop, reasons=reasons, seconds=time.time()-start,
                scope='synthetic observed states; expert non-synonymy not simulated')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seed', type=int, default=400)
    p.add_argument('--families', type=int, choices=[4, 6], default=4)
    p.add_argument('--small-bank', action='store_true')
    p.add_argument('--N', type=int, default=300)
    p.add_argument('--cap', type=int, default=100000)
    p.add_argument('--target', type=int, default=10)
    p.add_argument('--seconds', type=float, default=60.)
    p.add_argument('--output', type=Path)
    a = vars(p.parse_args()); a['rich'] = not a.pop('small_bank'); out = a.pop('output')
    result = json.dumps(run(**a), indent=2, allow_nan=False)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True); out.write_text(result+'\n')
    print(result)

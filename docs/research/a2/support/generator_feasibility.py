"""Feasibility of the constrained bijective perturbation generator (A2 protocol, Appendix K §K.5).

Synthetic concept banks and family specifications. Each proposal is a universal
permutation tau of concept identities within type blocks (categorical variables:
within the variable; binary concepts: within the block), drawn by a constrained
sampler that only proposes images within the frequency/missingness tolerance 0.10
(computed on train without labels). Acceptance, in this order:
  1. tolerance on every used concept;
  2. minimum change: the canonical card of every family differs from its V card
     (a swap inside one alternative group, or within one role, does not count);
  3. canonical-specification deduplication against V and earlier panels;
  4. per family, a certain witness on train-supported states (phi = 1, not phi = ?);
  5. per family, activation of v (some train-supported state with phi = 0);
  6. functional deduplication: (Q, v) on train-supported states differ from V and earlier panels;
  7. LP certificates d_F, d_D on train-supported states, accepted only if the solver
     succeeded, all quantities are finite, primal residual, dual residual and duality gap
     are <= 1e-8, and a conservative dual lower bound exceeds 1e-6.
A bank is declared infeasible as soon as an immovable family exists (no literal with a
tolerance-compatible alternative image); otherwise the run ends at the target, the
proposal cap or the time cap, and the termination reason is recorded.
Non-synonymy (expert judgement) and the frozen musicological review are not simulated.
"""
import argparse
import json
import time

import numpy as np
from scipy.optimize import linprog

import a2_ap

TOL = 0.10
BLOCKS = ('cad', 'appr', 'pat', 'rhy', 'mod')


def make_bank(rng, rich):
    sizes = dict(cad=7, appr=6 if rich else 4, pat=12 if rich else 6, rhy=8 if rich else 4, mod=6 if rich else 3)
    concepts = []
    var = 0
    for b, n in sizes.items():
        if b in ('cad', 'appr'):                       # categorical variable: mutually exclusive values
            probs = rng.dirichlet(np.ones(n) * 2)
            m = rng.beta(1, 12)
            for k in range(n):
                concepts.append(dict(block=b, var=var, p=probs[k], m=m))
            var += 1
        else:
            for _ in range(n):
                p = rng.beta(1.2, 3) if b != 'mod' else rng.beta(1, 6)
                m = rng.beta(1, 10) if b != 'mod' else rng.beta(1.5, 6)
                concepts.append(dict(block=b, var=var, p=p, m=m))
                var += 1
    return concepts


def make_specs(rng, concepts, K):
    idx = {b: [j for j, c in enumerate(concepts) if c['block'] == b] for b in BLOCKS}
    specs = []
    cad_vals = rng.choice(idx['cad'], K, replace=True)
    for f in range(K):
        R = [int(cad_vals[f])]
        if rng.random() < .5:
            R.append(int(rng.choice(idx['appr'])))
        A = []
        for _ in range(rng.integers(0, 3)):
            A.append([int(x) for x in rng.choice(idx['pat'] + idx['rhy'], 2, replace=False)])
        E = [int(rng.choice(idx['mod']))] if rng.random() < .6 else []
        specs.append(dict(R=R, A=A, E=E))
    return specs


def simulate_data(rng, concepts, specs, N):
    K = len(specs)
    J = len(concepts)
    y = rng.choice(K + 1, N, p=np.r_[np.full(K, .9 / K), .1])
    X = np.zeros((N, J))
    vars_ = {}
    for j, c in enumerate(concepts):
        vars_.setdefault(c['var'], []).append(j)
    for i in range(N):
        sp = specs[y[i]] if y[i] < K else None
        for v, js in vars_.items():
            if len(js) > 1:
                req = [j for j in js if sp and j in sp['R']]
                if req and rng.random() < .85:
                    k = req[0]
                else:
                    pr = np.array([concepts[j]['p'] for j in js])
                    k = rng.choice(js, p=pr / pr.sum())
                X[i, js] = 0
                X[i, k] = 1
            else:
                j = js[0]
                p = concepts[j]['p']
                if sp:
                    if j in sp['R']:
                        p = .85
                    if j in sp['E']:
                        p = .05
                X[i, j] = rng.random() < p
        if sp:
            for g in sp['A']:
                if rng.random() < .8:
                    X[i, rng.choice(g)] = 1
        for v, js in vars_.items():
            if rng.random() < concepts[js[0]]['m']:
                X[i, js] = -1                         # unknown (?)
    return y, X


def Q_phi(X, spec):
    """States x J in {1, 0, -1 (?)} -> Q (states x 3), phi in {0, 1/2, 1} (Kleene), v = 1[phi = 0]."""
    def q_req(j):
        c = X[:, j]
        return np.where(c < 0, 0, 2 * c - 1)

    def q_exc(j):
        c = X[:, j]
        return np.where(c < 0, 0, 1 - 2 * c)
    n = len(X)
    QR = np.mean([q_req(j) for j in spec['R']], 0) if spec['R'] else np.zeros(n)
    QA = np.mean([np.mean([q_req(j) for j in g], 0) for g in spec['A']], 0) if spec['A'] else np.zeros(n)
    QE = np.mean([q_exc(j) for j in spec['E']], 0) if spec['E'] else np.zeros(n)
    tv = lambda j: np.where(X[:, j] < 0, .5, X[:, j])
    phi = np.ones(n)
    for j in spec['R']:
        phi = np.minimum(phi, tv(j))
    for g in spec['A']:
        phi = np.minimum(phi, np.max([tv(j) for j in g], 0))
    for j in spec['E']:
        phi = np.minimum(phi, 1 - tv(j))
    return np.stack([QR, QA, QE], 1), phi, (phi == 0).astype(float)


def canonical(specs):
    return tuple((tuple(sorted(s['R'])), tuple(sorted(tuple(sorted(g)) for g in s['A'])), tuple(sorted(s['E'])))
                 for s in specs)


LP_TOL = 1e-8
CERT_MIN = 1e-6


def lp_cert(QV, vV, QP, vP, use_lambda):
    """min_x max_states |A x| over W x W (and lambda_V, lambda_P in [0, 2]).

    Returns the optimal value, solver status, primal residual, dual residual
    (stationarity and sign conditions of the HiGHS multipliers), duality gap and a
    conservative dual lower bound: dual objective minus |stationarity residual|_1 times a
    bound on |x| over the feasible box. The certificate is accepted by cert_ok()."""
    A = np.hstack([QV, -QP, -vV[:, None], vP[:, None]]) if use_lambda else np.hstack([QV, -QP])
    A = np.unique(A, axis=0)
    n = A.shape[1]
    c = np.r_[np.zeros(n), 1.]
    A_ub = np.vstack([np.hstack([A, -np.ones((len(A), 1))]), np.hstack([-A, -np.ones((len(A), 1))])])
    b_ub = np.zeros(2 * len(A))
    A_eq = np.zeros((2, n + 1))
    A_eq[0, 0:3] = 1
    A_eq[1, 3:6] = 1
    b_eq = np.array([1., 1.])
    lb = np.r_[np.full(6, .1), np.zeros(2) if use_lambda else [], 0.]
    ub = np.r_[np.full(6, np.inf), np.full(2, 2.) if use_lambda else [], np.inf]
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=list(zip(lb, ub)), method='highs')
    if r.status != 0:
        return dict(value=np.nan, status=int(r.status))
    x = r.x
    primal = max(float(np.max(A_ub @ x - b_ub, initial=0)), float(np.max(np.abs(A_eq @ x - b_eq))),
                 float(np.max(lb - x, initial=0)), float(np.max(x - ub, initial=0)))
    y_ub, y_eq = r.ineqlin.marginals, r.eqlin.marginals
    z_l, z_u = r.lower.marginals, r.upper.marginals
    fin_ub = np.isfinite(ub)
    stat = c - A_ub.T @ y_ub - A_eq.T @ y_eq - z_l - z_u
    sign = max(float(np.max(y_ub, initial=0)), float(np.max(-z_l, initial=0)), float(np.max(z_u, initial=0)),
               float(np.max(np.abs(z_u[~fin_ub]), initial=0)))
    dual_obj = float(b_ub @ y_ub + b_eq @ y_eq + lb @ z_l + ub[fin_ub] @ z_u[fin_ub])
    # feasible box: each weight in [0.1, 0.8], lambdas in [0, 2], t <= max_i sum_j |A_ij| xmax_j
    xmax = np.r_[np.full(6, .8), np.full(2, 2.) if use_lambda else []]
    box = np.r_[xmax, float(np.max(np.abs(A) @ xmax))]
    dual_bound = dual_obj - float(np.abs(stat) @ box)
    return dict(value=float(r.fun), status=0, primal_residual=primal,
                dual_residual=max(float(np.max(np.abs(stat))), sign),
                duality_gap=float(abs(r.fun - dual_obj)), dual_bound=dual_bound)


def cert_ok(d):
    keys = ('value', 'primal_residual', 'dual_residual', 'duality_gap', 'dual_bound')
    return (d.get('status') == 0 and all(np.isfinite(d.get(k, np.nan)) for k in keys)
            and d['primal_residual'] <= LP_TOL and d['dual_residual'] <= LP_TOL
            and d['duality_gap'] <= LP_TOL and d['dual_bound'] > CERT_MIN)


def blocks_of(concepts):
    blocks = {}
    for j, c in enumerate(concepts):
        key = (c['block'], c['var']) if c['block'] in ('cad', 'appr') else c['block']
        blocks.setdefault(key, []).append(j)
    return blocks


def propose(rng, blocks, used, freq, miss, move_pref=0., restarts=50):
    """Constrained sampler: random matching of used concepts to tolerance-compatible images.

    move_pref: probability of excluding the identity image when another compatible image is
    free (0 = uniform over compatible images). Label-free; declared before any model run.
    """
    J = sum(len(v) for v in blocks.values())
    tau = np.arange(J)
    for js in blocks.values():
        js = np.array(js)
        ok = False
        for _ in range(restarts):
            perm = {}
            free = set(js.tolist())
            ok = True
            for j in rng.permutation([j for j in js if j in used]):
                cand = [k for k in free if abs(freq[k] - freq[j]) <= TOL and abs(miss[k] - miss[j]) <= TOL]
                if len(cand) > 1 and j in cand and rng.random() < move_pref:
                    cand.remove(int(j))
                if not cand:
                    ok = False
                    break
                k = int(rng.choice(cand))
                perm[int(j)] = k
                free.remove(k)
            if ok:
                break
        if not ok:
            tau[js] = rng.permutation(js)          # rejected later by the tolerance check
            continue
        rest_src = [int(j) for j in js if int(j) not in perm]
        rest_dst = list(free)
        rng.shuffle(rest_dst)
        perm.update(zip(rest_src, rest_dst))
        for a, b in perm.items():
            tau[a] = b
    return tau


def apply_tau(spec, tau):
    return dict(R=[int(tau[j]) for j in spec['R']], A=[[int(tau[j]) for j in g] for g in spec['A']],
                E=[int(tau[j]) for j in spec['E']])


def run_bank(seed, K, rich, N=300, target=10, cap=100000, cap_sec=30, move_pref=0.):
    rng = np.random.default_rng(seed)
    concepts = make_bank(rng, rich)
    specs = make_specs(rng, concepts, K)
    y, X = simulate_data(rng, concepts, specs, N)
    obs = X >= 0
    freq = np.where(obs.sum(0) > 0, (X == 1).sum(0) / np.maximum(obs.sum(0), 1), 0)
    miss = 1 - obs.mean(0)
    used = sorted(set(j for s in specs for j in s['R'] + [x for g in s['A'] for x in g] + s['E']))
    Om = np.unique(X, axis=0)                          # train-supported states
    QV, phiV, vV = zip(*[Q_phi(Om, s) for s in specs])
    QVs, vVs = np.vstack(QV), np.concatenate(vV)
    V_witness = [bool((p == 1).any()) for p in phiV]
    V_active = [bool(v.max() == 1) for v in vV]
    blocks = blocks_of(concepts)
    J = len(concepts)
    block_of = {j: key for key, js in blocks.items() for j in js}
    movable = {j: any(k != j and block_of[k] == block_of[j] and abs(freq[k] - freq[j]) <= TOL
                      and abs(miss[k] - miss[j]) <= TOL for k in range(J)) for j in used}
    immovable_fam = sum(not any(movable[j] for j in s['R'] + [x for g in s['A'] for x in g] + s['E']) for s in specs)
    seen_canon = {canonical(specs)}
    seen_func = [(QVs, vVs)]
    canon_V = [canonical([s]) for s in specs]
    reasons = dict(identity=0, tolerance=0, family_unchanged=0, canonical_duplicate=0, no_witness=0,
                   no_activation=0, functional_duplicate=0, lp_F=0, lp_D=0)
    acc = []
    t0 = time.time()
    n = 0
    termination = None
    if immovable_fam:
        termination = 'infeasible_immovable_family'
    while termination is None:
        if len(acc) >= target:
            termination = 'target_reached'
            break
        if n >= cap:
            termination = 'proposal_cap'
            break
        if time.time() - t0 >= cap_sec:
            termination = 'time_cap'
            break
        n += 1
        tau = propose(rng, blocks, set(used), freq, miss, move_pref)
        if all(tau[j] == j for j in used):
            reasons['identity'] += 1
            continue
        if any(abs(freq[tau[j]] - freq[j]) > TOL or abs(miss[tau[j]] - miss[j]) > TOL for j in used):
            reasons['tolerance'] += 1
            continue
        P = [apply_tau(s, tau) for s in specs]
        if any(canonical([pf]) == cv for pf, cv in zip(P, canon_V)):
            reasons['family_unchanged'] += 1
            continue
        cP = canonical(P)
        if cP in seen_canon:
            reasons['canonical_duplicate'] += 1
            continue
        QP, phiP, vP = zip(*[Q_phi(Om, s) for s in P])
        if not all((p == 1).any() for p in phiP):
            reasons['no_witness'] += 1
            continue
        if not all(v.max() == 1 for v in vP):
            reasons['no_activation'] += 1
            continue
        QPs, vPs = np.vstack(QP), np.concatenate(vP)
        if any(np.array_equal(QPs, q) and np.array_equal(vPs, v) for q, v in seen_func):
            reasons['functional_duplicate'] += 1
            continue
        dF = lp_cert(QVs, vVs, QPs, vPs, False)
        if not cert_ok(dF):
            reasons['lp_F'] += 1
            continue
        dD = lp_cert(QVs, vVs, QPs, vPs, True)
        if not cert_ok(dD):
            reasons['lp_D'] += 1
            continue
        seen_canon.add(cP)
        seen_func.append((QPs, vPs))
        only_E = [canonical([dict(R=pf['R'], A=pf['A'], E=[])]) == canonical([dict(R=s['R'], A=s['A'], E=[])])
                  for pf, s in zip(P, specs)]
        acc.append(dict(tau=tau, dF=dF, dD=dD, only_E=float(np.mean(only_E)),
                        v_agree=float((vPs == vVs).mean())))
    pair = [np.mean([a['tau'][j] == b['tau'][j] for j in used]) for i, a in enumerate(acc) for b in acc[i + 1:]]
    res = lambda key, f: (float(max(a[key][f] for a in acc)) if acc else None)
    return dict(seed=seed, K=K, rich=rich, move_pref=move_pref, immovable_families=int(immovable_fam), N=N, target=target, cap_proposals=cap, cap_seconds=cap_sec,
                proposals=n, accepted=len(acc), termination=termination, seconds=round(time.time() - t0, 1), reasons=reasons,
                used_concepts=len(used), train_states=len(Om),
                V_witness_all=all(V_witness), V_active_all=all(V_active),
                only_E_change_mean=(round(float(np.mean([a['only_E'] for a in acc])), 3) if acc else None),
                v_agree_mean=(round(float(np.mean([a['v_agree'] for a in acc])), 3) if acc else None),
                pair_overlap=(round(float(np.mean(pair)), 3) if pair else None),
                dF_median=(float(np.median([a['dF']['value'] for a in acc])) if acc else None),
                dD_median=(float(np.median([a['dD']['value'] for a in acc])) if acc else None),
                lp_max_primal_residual=(max(res('dF', 'primal_residual'), res('dD', 'primal_residual')) if acc else None),
                lp_max_duality_gap=(max(res('dF', 'duality_gap'), res('dD', 'duality_gap')) if acc else None),
                lp_max_dual_residual=(max(res('dF', 'dual_residual'), res('dD', 'dual_residual')) if acc else None),
                lp_min_dual_bound=(min(min(a['dF']['dual_bound'], a['dD']['dual_bound']) for a in acc) if acc else None),
                taus=[a['tau'] for a in acc])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--banks', type=int, default=4, help='banks per (K, rich) cell')
    ap.add_argument('--cap-sec', dest='cap_sec', type=float, default=30)
    ap.add_argument('--move-pref', dest='move_pref', type=float, default=0.)
    a = ap.parse_args()
    env = a2_ap.environment()
    for K in (4, 6):
        for rich in (True, False):
            for b in range(a.banks):
                r = run_bank(100 * K + b + (0 if rich else 50), K, rich, cap_sec=a.cap_sec, move_pref=a.move_pref)
                r['env'] = env
                print(a2_ap.dump(r), flush=True)

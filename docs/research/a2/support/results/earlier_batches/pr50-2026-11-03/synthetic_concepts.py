"""Synthetic typed concepts, cards and Kleene evaluation.

Adapted from the supplied A2 simulations. Labels influence synthetic data
construction only; the perturbation acceptance code never receives labels.
Unknown is encoded as -1 in X and 0.5 in phi.
"""
import numpy as np
TOL = 0.10

def make_bank(rng, rich):
    sizes = dict(cad=7, appr=6 if rich else 4, pat=12 if rich else 6, rhy=8 if rich else 4, mod=6 if rich else 3)
    concepts = []   # dict(block, var, p, m)
    var = 0
    for b, n in sizes.items():
        if b in ('cad', 'appr'):                      # categorical variable: exclusive values
            probs = rng.dirichlet(np.ones(n) * 2)
            m = rng.beta(1, 12)
            for k in range(n):
                concepts.append(dict(block=b, var=var, p=probs[k], m=m))
            var += 1
        else:
            for k in range(n):
                p = rng.beta(1.2, 3) if b != 'mod' else rng.beta(1, 6)
                m = rng.beta(1, 10) if b != 'mod' else rng.beta(1.5, 6)
                concepts.append(dict(block=b, var=var, p=p, m=m)); var += 1
    return concepts


def make_specs(rng, concepts, K):
    idx = {b: [j for j, c in enumerate(concepts) if c['block'] == b] for b in ('cad', 'appr', 'pat', 'rhy', 'mod')}
    specs = []
    cad_vals = rng.choice(idx['cad'], K, replace=True)          # families may share a cadence degree
    for f in range(K):
        R = [int(cad_vals[f])]
        if rng.random() < .5:
            R.append(int(rng.choice(idx['appr'])))
        G = []
        for _ in range(rng.integers(0, 3)):
            pool = idx['pat'] + idx['rhy']
            G.append([int(x) for x in rng.choice(pool, 2, replace=False)])
        E = [int(rng.choice(idx['mod']))] if rng.random() < .6 else []
        specs.append(dict(R=R, G=G, E=E))
    return specs


def simulate_data(rng, concepts, specs, N):
    K = len(specs); J = len(concepts)
    y = rng.choice(K + 1, N, p=np.r_[np.full(K, .9 / K), .1])   # K == unknown family
    X = np.zeros((N, J))
    vars_ = {}
    for j, c in enumerate(concepts):
        vars_.setdefault(c['var'], []).append(j)
    for i in range(N):
        sp = specs[y[i]] if y[i] < K else None
        for v, js in vars_.items():
            if len(js) > 1:                                       # categorical
                req = [j for j in js if sp and j in sp['R']]
                if req and rng.random() < .85:
                    k = req[0]
                else:
                    pr = np.array([concepts[j]['p'] for j in js]); k = rng.choice(js, p=pr / pr.sum())
                X[i, js] = 0; X[i, k] = 1
            else:
                j = js[0]; p = concepts[j]['p']
                if sp:
                    if j in sp['R']: p = .85
                    if j in sp['E']: p = .05
                X[i, j] = rng.random() < p
        if sp:
            for g in sp['G']:
                if rng.random() < .8:
                    X[i, rng.choice(g)] = 1
        for v, js in vars_.items():
            if rng.random() < concepts[js[0]]['m']:
                X[i, js] = -1                                    # unknown
    return y, X


def evaluate(X, spec):
    """X: states x J with values {1,0,-1(?)} -> Q (states x 3), v (states)."""
    def q_req(j):
        c = X[:, j]; return np.where(c < 0, 0, 2 * c - 1)
    def q_exc(j):
        c = X[:, j]; return np.where(c < 0, 0, 1 - 2 * c)
    QR = np.mean([q_req(j) for j in spec['R']], 0) if spec['R'] else np.zeros(len(X))
    QA = np.mean([np.mean([q_req(j) for j in g], 0) for g in spec['G']], 0) if spec['G'] else np.zeros(len(X))
    QE = np.mean([q_exc(j) for j in spec['E']], 0) if spec['E'] else np.zeros(len(X))
    t = lambda j: np.where(X[:, j] < 0, .5, X[:, j])       # Kleene with ? = 0.5
    phi = np.ones(len(X))
    for j in spec['R']: phi = np.minimum(phi, t(j))
    for g in spec['G']: phi = np.minimum(phi, np.max([t(j) for j in g], 0))
    for j in spec['E']: phi = np.minimum(phi, 1 - t(j))
    return np.stack([QR, QA, QE], 1), (phi == 0).astype(float), phi


def apply_tau(spec, tau):
    return dict(R=[int(tau[j]) for j in spec['R']], G=[[int(tau[j]) for j in g] for g in spec['G']], E=[int(tau[j]) for j in spec['E']])


def propose(rng, concepts, used, freq, miss, smart, derange=False):
    J = len(concepts)
    tau = np.arange(J)
    blocks = {}
    for j, c in enumerate(concepts):
        key = (c['block'], c['var']) if c['block'] in ('cad', 'appr') else c['block']
        blocks.setdefault(key, []).append(j)
    for key, js in blocks.items():
        js = np.array(js)
        if not smart:
            tau[js] = rng.permutation(js)
        else:                                                  # random matching within tolerance, with restarts
            for _ in range(50):
                perm = {}; free = set(js.tolist()); okk = True
                order = rng.permutation([j for j in js if j in used])
                for j in order:
                    cand = [k for k in free if abs(freq[k] - freq[j]) <= TOL and abs(miss[k] - miss[j]) <= TOL and not (derange and k == j)]
                    if not cand: okk = False; break
                    k = int(rng.choice(cand)); perm[j] = k; free.remove(k)
                if okk: break
            if not okk:
                tau[js] = rng.permutation(js)  # will fail tolerance check
                continue
            rest_src = [j for j in js if j not in perm]; rest_dst = list(free)
            rng.shuffle(rest_dst)
            for a, b in zip(rest_src, rest_dst): perm[a] = b
            for a, b in perm.items(): tau[a] = b
    return tau


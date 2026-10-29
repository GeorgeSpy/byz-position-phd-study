"""
Test oracle για τις αναδρομές του CLAUDE_A_INDEPENDENT_ARCHITECTURE_GR.md.

Ελέγχει με εξαντλητική απαρίθμηση σε μικρά παραδείγματα:
  O1  ημι-Μαρκοβιανό CRF μηδενικής τάξης με δομική παράλειψη (Z, περιθώρια)
  O2  CRF πρώτης τάξης ως προς τις οικογένειες, με σημαία γειτνίασης b και
      εξάρτηση της μετάβασης από το σημείο τ, μέσω της παραγοντοποίησης β(τ,g)
  O3  προφίλ-κανάλι (M/I/D) ως δυναμικό τμήματος: μία εμπρόσθια διέλευση ανά
      αρχή a δίνει όλα τα p(x_{a:b}|F) για b = a..a+L-1
  O4  περιορισμένος παρονομαστής «ακριβώς μία από τις αποδεκτές αναλύσεις A_o»
  O5  ισοδυναμία: semi-CRF με δυναμικό log-odds = ακριβές posterior γεννητικού
      μοντέλου πολλαπλών τμημάτων (υπόβαθρο p0 + προφίλ)

Εκτέλεση: python3 -I claude_dp_oracle.py   (μόνο numpy)
"""
import itertools
import math
import numpy as np

rng = np.random.default_rng(7)


def logsumexp(v):
    v = np.asarray(v, dtype=float)
    m = np.max(v)
    if not np.isfinite(m):
        return -np.inf
    return m + math.log(np.sum(np.exp(v - m)))


# ---------------------------------------------------------------- outputs
def enumerate_outputs(T, L, K):
    """Όλες οι μη επικαλυπτόμενες έξοδοι: λίστα από (a, b, f), 1-based, a<=b."""
    out = []

    def rec(t, cur):
        if t > T:
            out.append(list(cur))
            return
        rec(t + 1, cur)  # skip event t
        for ell in range(1, L + 1):
            b = t + ell - 1
            if b > T:
                break
            for f in range(K):
                cur.append((t, b, f))
                rec(b + 1, cur)
                cur.pop()

    rec(1, [])
    return out


def score0(y, phi, chi, T):
    covered = set()
    s = 0.0
    for (a, b, f) in y:
        s += phi[a, b, f]
        covered.update(range(a, b + 1))
    s += sum(chi[t] for t in range(1, T + 1) if t not in covered)
    return s


# ---------------------------------------------------------------- O1
def forward0(phi, chi, T, L, K, allowed=None):
    la = np.full(T + 1, -np.inf)
    la[0] = 0.0
    for t in range(1, T + 1):
        terms = [la[t - 1] + chi[t]]
        for ell in range(1, min(L, t) + 1):
            a = t - ell + 1
            for f in range(K):
                if allowed is not None and not allowed(a, t, f):
                    continue
                terms.append(la[a - 1] + phi[a, t, f])
        la[t] = logsumexp(terms)
    return la[T]


def test_O1():
    T, L, K = 6, 3, 2
    phi = rng.normal(size=(T + 2, T + 2, K))
    chi = rng.normal(size=T + 2)
    ys = enumerate_outputs(T, L, K)
    brute = logsumexp([score0(y, phi, chi, T) for y in ys])
    dp = forward0(phi, chi, T, L, K)
    assert abs(brute - dp) < 1e-9, (brute, dp)
    # bijection: no duplicate outputs
    keys = {tuple(y) for y in ys}
    assert len(keys) == len(ys)
    return len(ys), brute, dp


# ---------------------------------------------------------------- O2
def score1(y, phi, chi, psi, T):
    """psi[tau, gprev, g, b]; gprev = K means BOS; b=0 adjacent, 1 gap."""
    s = score0(y, phi, chi, T)
    K = phi.shape[2]
    prev_label, prev_end = K, 0
    for (a, b, f) in sorted(y):
        adj = 0 if a == prev_end + 1 else 1
        s += psi[a - 1, prev_label, f, adj]
        prev_label, prev_end = f, b
    return s


def forward1(phi, chi, psi, T, L, K):
    # alpha[t, g, b], g in 0..K (K=BOS), b in {0,1}
    A = np.full((T + 1, K + 1, 2), -np.inf)
    A[0, K, 0] = 0.0
    beta = np.full((T + 1, K), -np.inf)
    for t in range(0, T + 1):
        if t >= 1:
            # skip event t
            for g in range(K + 1):
                A[t, g, 1] = logsumexp([A[t - 1, g, 0], A[t - 1, g, 1]]) + chi[t]
            # segment ending at t
            for g in range(K):
                terms = [beta[t - ell, g] + phi[t - ell + 1, t, g]
                         for ell in range(1, min(L, t) + 1)]
                A[t, g, 0] = logsumexp(terms)
        # beta(tau=t, g) = logsum_{g',b'} alpha(t,g',b') + psi[t,g',g,b']
        if t <= T - 1:
            for g in range(K):
                beta[t, g] = logsumexp([A[t, gp, bp] + psi[t, gp, g, bp]
                                        for gp in range(K + 1) for bp in (0, 1)])
    return logsumexp(A[T].ravel())


def test_O2():
    T, L, K = 6, 3, 2
    phi = rng.normal(size=(T + 2, T + 2, K))
    chi = rng.normal(size=T + 2)
    psi = rng.normal(size=(T + 1, K + 1, K, 2))
    ys = enumerate_outputs(T, L, K)
    brute = logsumexp([score1(y, phi, chi, psi, T) for y in ys])
    dp = forward1(phi, chi, psi, T, L, K)
    assert abs(brute - dp) < 1e-9, (brute, dp)
    return brute, dp


# ---------------------------------------------------------------- O3
class Profile:
    """Προφίλ μήκους Kp με καταστάσεις M_k, I_k (k=0..Kp), D_k.
    Δεν επιτρέπονται άμεσες μεταβάσεις I->D, D->I (όπως στο Plan7)."""

    def __init__(self, Kp, V, rng):
        self.Kp, self.V = Kp, V
        def simplex(n):
            p = rng.random(n) + 0.1
            return p / p.sum()
        self.eM = [None] + [simplex(V) for _ in range(Kp)]
        self.eI = [simplex(V) for _ in range(Kp + 1)]
        # transitions from M_k / B (k=0): to M_{k+1}, I_k, D_{k+1}
        self.tM = [simplex(3) for _ in range(Kp + 1)]
        # from I_k: to M_{k+1}, I_k
        self.tI = [simplex(2) for _ in range(Kp + 1)]
        # from D_k: to M_{k+1}, D_{k+1}
        self.tD = [None] + [simplex(2) for _ in range(Kp)]

    # ---- brute force: enumerate state paths emitting exactly x
    def brute(self, x):
        Kp = self.Kp
        total = 0.0

        def rec(state, k, i, p):
            nonlocal total
            n = len(x)
            # state in {'B','M','I','D'}; position k; i symbols emitted
            if (state in ('M', 'D') and k == Kp) or (state == 'I' and k == Kp) or (state == 'B' and Kp == 0):
                if i == n:
                    total += p
                # from final column only end (and I_Kp self-loop for insert)
                if state in ('M', 'B') and k == Kp:
                    # insert after last
                    if i < n:
                        rec('I', k, i + 1, p * self.tM[k][1] * self.eI[k][x[i]] / 1.0)
                    return
                if state == 'I' and k == Kp:
                    if i < n:
                        rec('I', k, i + 1, p * self.tI[k][1] * self.eI[k][x[i]])
                    return
                if state == 'D':
                    return
            if state in ('B', 'M'):
                tr = self.tM[k]
                if k + 1 <= Kp and i < n:
                    rec('M', k + 1, i + 1, p * tr[0] * self.eM[k + 1][x[i]])
                if i < n:
                    rec('I', k, i + 1, p * tr[1] * self.eI[k][x[i]])
                if k + 1 <= Kp:
                    rec('D', k + 1, i, p * tr[2])
            elif state == 'I':
                tr = self.tI[k]
                if k + 1 <= Kp and i < n:
                    rec('M', k + 1, i + 1, p * tr[0] * self.eM[k + 1][x[i]])
                if i < n:
                    rec('I', k, i + 1, p * tr[1] * self.eI[k][x[i]])
            elif state == 'D':
                tr = self.tD[k]
                if k + 1 <= Kp and i < n:
                    rec('M', k + 1, i + 1, p * tr[0] * self.eM[k + 1][x[i]])
                if k + 1 <= Kp:
                    rec('D', k + 1, i, p * tr[1])

        rec('B', 0, 0, 1.0)
        return total

    # ---- one forward pass from a start, returning p(x[:n]) for all n
    def forward_all_prefixes(self, xs):
        """End condition identical to brute(): the path finishes in column Kp
        (state M_Kp, D_Kp or I_Kp) having emitted exactly n symbols."""
        Kp, N = self.Kp, len(xs)
        M = np.zeros((N + 1, Kp + 1))  # M[i,k]: emitted i, in M_k (k=0 is B)
        I = np.zeros((N + 1, Kp + 1))
        D = np.zeros((N + 1, Kp + 1))
        M[0, 0] = 1.0  # begin state B == M_0 with transitions tM[0]
        for i in range(0, N + 1):
            for k in range(0, Kp + 1):
                # D_k (no emission) from M_{k-1}, I? (no), D_{k-1} at same i
                if k >= 1:
                    D[i, k] = M[i, k - 1] * self.tM[k - 1][2] + (D[i, k - 1] * self.tD[k - 1][1] if k - 1 >= 1 else 0.0)
                if i >= 1:
                    xi = xs[i - 1]
                    if k >= 1:
                        M[i, k] = (M[i - 1, k - 1] * self.tM[k - 1][0]
                                   + I[i - 1, k - 1] * self.tI[k - 1][0]
                                   + (D[i - 1, k - 1] * self.tD[k - 1][0] if k - 1 >= 1 else 0.0)) * self.eM[k][xi]
                    I[i, k] = (M[i - 1, k] * self.tM[k][1] + I[i - 1, k] * self.tI[k][1]) * self.eI[k][xi]
        return [M[n, Kp] + D[n, Kp] + I[n, Kp] for n in range(N + 1)]


def test_O3():
    Kp, V = 3, 3
    prof = Profile(Kp, V, rng)
    xs = list(rng.integers(0, V, size=6))
    shared = prof.forward_all_prefixes(xs)
    worst = 0.0
    for n in range(1, len(xs) + 1):
        b = prof.brute(xs[:n])
        worst = max(worst, abs(b - shared[n]) / max(b, 1e-300))
    assert worst < 1e-9, worst
    return worst


# ---------------------------------------------------------------- O4
def test_O4():
    T, L, K = 7, 3, 2
    phi = rng.normal(size=(T + 2, T + 2, K))
    chi = rng.normal(size=T + 2)
    A_o = {(2, 4, 0), (3, 4, 0), (2, 5, 0), (3, 5, 1)}  # αποδεκτά (όρια, οικογένεια)
    ys = enumerate_outputs(T, L, K)
    brute = logsumexp([score0(y, phi, chi, T) for y in ys
                       if sum((a, b, f) in A_o for (a, b, f) in y) == 1])
    # DP με σημαία c in {0,1}
    la = np.full((T + 1, 2), -np.inf)
    la[0, 0] = 0.0
    for t in range(1, T + 1):
        for c in (0, 1):
            terms = [la[t - 1, c] + chi[t]]
            for ell in range(1, min(L, t) + 1):
                a = t - ell + 1
                for f in range(K):
                    inA = (a, t, f) in A_o
                    if inA and c == 1:
                        terms.append(la[a - 1, 0] + phi[a, t, f])
                    elif not inA:
                        terms.append(la[a - 1, c] + phi[a, t, f])
            la[t, c] = logsumexp(terms)
    dp = la[T, 1]
    full = forward0(phi, chi, T, L, K)
    assert abs(brute - dp) < 1e-9, (brute, dp)
    assert full >= dp
    return brute, dp, full - dp


# ---------------------------------------------------------------- O5
def test_O5():
    """Γεννητικό μοντέλο: κάθε ακάλυπτο γεγονός ~ p0, κάθε τμήμα ~ πF(ℓ)·p(x_s|F)·w_F,
    με γεωμετρική επιλογή skip/segment. Δείχνει ότι P(y|X) του semi-CRF με
    φ = log w_F + log π(ℓ) + log p(x_s|F) - Σ log p0 - log ρ_seg και χ = 0
    ισούται με το ακριβές posterior P(y|X) = P(X,y)/P(X)."""
    T, L, K, V = 5, 3, 2, 3
    xs = list(rng.integers(0, V, size=T))
    p0 = rng.random(V) + 0.1; p0 /= p0.sum()
    profs = [Profile(2, V, rng) for _ in range(K)]
    w = rng.random(K) + 0.1; w /= w.sum()
    rho_seg = 0.3  # πιθανότητα έναρξης τμήματος σε κάθε θέση
    lenp = rng.random(L) + 0.1; lenp /= lenp.sum()
    # p(x_{a:b}|F) από το Profile (πλήρης κανονικοποίηση δεν απαιτείται για την ταυτότητα)
    def seg_lik(a, b, f):
        return profs[f].forward_all_prefixes(xs[a - 1:b])[b - a + 1]
    ys = enumerate_outputs(T, L, K)

    def joint(y):
        p = 1.0
        covered = set()
        for (a, b, f) in y:
            covered.update(range(a, b + 1))
        t = 1
        segs = {a: (a, b, f) for (a, b, f) in y}
        while t <= T:
            if t in segs:
                a, b, f = segs[t]
                p *= rho_seg * w[f] * lenp[b - a] * seg_lik(a, b, f)
                t = b + 1
            else:
                p *= (1 - rho_seg) * p0[xs[t - 1]]
                t += 1
        return p

    J = np.array([joint(y) for y in ys])
    post_gen = J / J.sum()
    phi = np.full((T + 2, T + 2, K), -np.inf)
    for a in range(1, T + 1):
        for b in range(a, min(T, a + L - 1) + 1):
            for f in range(K):
                phi[a, b, f] = (math.log(rho_seg * w[f] * lenp[b - a] * seg_lik(a, b, f))
                                - sum(math.log((1 - rho_seg) * p0[xs[t - 1]]) for t in range(a, b + 1)))
    chi = np.zeros(T + 2)
    sc = np.array([score0(y, phi, chi, T) for y in ys])
    post_crf = np.exp(sc - logsumexp(sc))
    err = np.max(np.abs(post_gen - post_crf))
    assert err < 1e-12, err
    return err


if __name__ == "__main__":
    n, b, d = test_O1()
    print(f"O1 zero-order semi-CRF: {n} outputs, brute logZ={b:.12f}, DP={d:.12f}  PASS")
    b, d = test_O2()
    print(f"O2 first-order (factorised beta): brute={b:.12f}, DP={d:.12f}  PASS")
    w = test_O3()
    print(f"O3 profile segment potentials, one pass per start: max rel err={w:.2e}  PASS")
    b, d, gap = test_O4()
    print(f"O4 'exactly one of A_o': brute={b:.12f}, DP={d:.12f}, L_j=logZ-logZ^A={gap:.6f}>=0  PASS")
    e = test_O5()
    print(f"O5 log-odds semi-CRF == generative posterior: max abs diff={e:.2e}  PASS")

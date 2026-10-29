"""
claude_ac_ecsi_oracle.py — αριθμητικό oracle για την AC-ECSI (δεύτερος κύκλος, 29/10/2026)

Ελέγχει με ΕΞΑΝΤΛΗΤΙΚΗ απαρίθμηση διαδρομών και αναθέσεων εννοιών:

  O6a  Αναπαραγωγή του παιγνιώδους παραδείγματος Gemini (0,829 έναντι 0,874).
  O6   Ακριβές product trellis: profile HMM (M/I/D, εισαγωγές, διαγραφές)
       × ελάχιστο αυτόματο της προδιαγραφής (σειρά μεταβλητών κατά άγκυρα,
       μεταβλητή ολόκληρου τμήματος στο τέλος). Μία εμπρόσθια διέλευση ανά
       αρχή δίνει A_f(n), B_f(n) για ΟΛΑ τα τέλη n. Πολλαπλοί τυχαίοι σπόροι.
  O6g  Κλίσεις: πεπερασμένες διαφορές του log B_f από το DP έναντι της
       αναλυτικής δεσμευμένης περιθώριας πιθανότητας από απαρίθμηση.
  O6r  Αναγκαιότητα της συνθήκης τοπικότητας L1: αν η q_j εξαρτάται από
       το τέλος n του τμήματος, η επαναχρησιμοποίηση προθέματος ΑΠΟΤΥΓΧΑΝΕΙ
       (αναμενόμενο)· το DP ανά τέλος παραμένει ακριβές.
  O7   Εκφυλισμοί και ταυτότητες: (i) μόνο έννοιες τμήματος ⇒ AC = Add·
       (ii) μονό literal ⇒ AC = Pool· (iii) ντετερμινιστική στοίχιση ⇒
       AC = Pool = Viterbi· (iv) u1∧u2 ⇒ AC − Pool = +Cov, u1∨u2 ⇒ −Cov·
       (v) γενική περίπτωση: AC ≠ Pool ≠ Viterbi ≠ Add.
  O7r  Αναγωγή: για ΚΑΘΕ προδιαγραφή S ⊆ {0,1}^3 (256 προδιαγραφές)
       m_AC(S) = Σ_{u∈S} q*(u|X), q* = μείγμα γινομένων με βάρη p(π|X).
  O7e  Όριο εκφραστικότητας (van Krieken κ.ά. 2024): δύο έννοιες στην ίδια
       άγκυρα με βέβαιη στοίχιση δεν μπορούν να αναπαραστήσουν q(00)=q(11)=1/2.
  O8   Κανονικοποίηση: Z_f = P(u∈S_f | f) με άθροιση εκπομπών μέσα στο
       trellis = άθροισμα B_f(X) σε όλα τα X με |X|≤N (εξαντλητικά).
       Μετατόπιση log(Z_f/r_f) ανά οικογένεια.
  O9   Ταυτότητα εμπεριέχοντος prior (Klugkist κ.ά. 2005): m_f/r_f = Bayes
       factor όταν η q είναι posterior υπό r· αποτυχία όταν η q βαθμονομήθηκε
       με άλλο prior.
  O10  Monte Carlo στοιχίσεων: αμερόληπτη προσέγγιση, όχι ακριβής.
  O11  Πλάτος αυτομάτου: μικρό για τη χρησιμοποιούμενη προδιαγραφή, 2^m για
       m διασταυρούμενες ισότητες ανάμεσα σε μακρινές άγκυρες.

Εκτέλεση:  python3 -I claude_ac_ecsi_oracle.py      (μόνο numpy)
Έξοδος 0 μόνο αν όλοι οι έλεγχοι που ΑΝΑΜΕΝΕΤΑΙ να περάσουν περνούν και ο
έλεγχος O6r-naive αποτυγχάνει όπως αναμένεται.
"""
import itertools
import math
import sys

import numpy as np

TOL = 1e-10
RESULTS = []


def report(name, ok, detail):
    RESULTS.append((name, ok))
    print(f"{name:<8} {'PASS' if ok else 'FAIL'}  {detail}")


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


# ======================================================================
# Profile HMM με M/I/D, κανονικοποιημένο τέλος
# ======================================================================
class Profile:
    """Άγκυρες k=1..K. Αρχή = M_0. Από M_k (k<K): (M_{k+1}, I_k, D_{k+1}).
    Από I_k (k<K): (M_{k+1}, I_k). Από D_k (1<=k<K): (M_{k+1}, D_{k+1}).
    Στήλη K: M_K -> τέλος (endM) ή I_K· I_K -> τέλος (endI) ή I_K· D_K -> τέλος."""

    def __init__(self, K, V, rng, deterministic=False):
        self.K, self.V = K, V

        def simplex(n):
            p = rng.random(n) + 0.15
            return p / p.sum()

        self.eM = [None] + [simplex(V) for _ in range(K)]
        self.eI = [simplex(V) for _ in range(K + 1)]
        self.tM = [simplex(3) for _ in range(K)]
        self.tI = [simplex(2) for _ in range(K)]
        self.tD = [None] + [simplex(2) for _ in range(K - 1)]
        self.endM = float(rng.uniform(0.4, 0.9))
        self.endI = float(rng.uniform(0.4, 0.9))
        if deterministic:
            self.tM = [np.array([1.0, 0.0, 0.0]) for _ in range(K)]
            self.endM = 1.0

    def paths(self, x):
        """Όλες οι διαδρομές που εκπέμπουν ακριβώς το x.
        Επιστρέφει λίστα (p(x,π), events), events[k] = ('M', i) ή ('D', None)."""
        K, n = self.K, len(x)
        out = []

        def rec(st, k, i, p, ev):
            if p == 0.0:
                return
            if k < K:
                if st == 'M':
                    tr = self.tM[k]
                    if i < n:
                        rec('M', k + 1, i + 1, p * tr[0] * self.eM[k + 1][x[i]], ev + ((k + 1, 'M', i + 1),))
                        rec('I', k, i + 1, p * tr[1] * self.eI[k][x[i]], ev)
                    rec('D', k + 1, i, p * tr[2], ev + ((k + 1, 'D', None),))
                elif st == 'I':
                    tr = self.tI[k]
                    if i < n:
                        rec('M', k + 1, i + 1, p * tr[0] * self.eM[k + 1][x[i]], ev + ((k + 1, 'M', i + 1),))
                        rec('I', k, i + 1, p * tr[1] * self.eI[k][x[i]], ev)
                else:  # 'D'
                    tr = self.tD[k]
                    if i < n:
                        rec('M', k + 1, i + 1, p * tr[0] * self.eM[k + 1][x[i]], ev + ((k + 1, 'M', i + 1),))
                    rec('D', k + 1, i, p * tr[1], ev + ((k + 1, 'D', None),))
            else:
                if st == 'M':
                    if i == n:
                        out.append((p * self.endM, ev))
                    elif self.endM < 1.0:
                        rec('I', K, i + 1, p * (1 - self.endM) * self.eI[K][x[i]], ev)
                elif st == 'I':
                    if i == n:
                        out.append((p * self.endI, ev))
                    else:
                        rec('I', K, i + 1, p * (1 - self.endI) * self.eI[K][x[i]], ev)
                else:
                    if i == n:
                        out.append((p, ev))

        rec('M', 0, 0, 1.0, ())
        res = []
        for p, ev in out:
            d = {k: (t, i) for (k, t, i) in ev}
            assert len(d) == K
            res.append((p, d))
        return res


# ======================================================================
# Διαγνωστικές έννοιες
# ======================================================================
class Diagnostics:
    """Έννοιες με κάτοχο άγκυρα (owner=k) ή ολόκληρο τμήμα (owner='span').
    Άγκυρα: q_j(1 | M, i, x) = σ(w0 + w1·x_i + w2·x_{i-1} + w3·i [+ w4·i/n]).
    q_j(1 | D) = d_j (πολιτική απουσίας). Τμήμα: q(1|n) = σ(c0 + c1·n + c2·mean(x_{1:n}))."""

    def __init__(self, owners, rng, end_dependent=False, deterministic=None):
        self.owners = owners
        self.J = len(owners)
        self.w = [rng.normal(size=5) for _ in owners]
        self.d = [float(rng.uniform(0.05, 0.4)) for _ in owners]
        self.end_dependent = end_dependent
        self.deterministic = deterministic   # dict j -> target symbol, q = 1[x_i == target]
        self.override = {}                   # (j, i, u) -> multiplicative factor (κλίσεις)

    def q_anchor(self, j, kind, i, x, n_for_factor):
        if kind == 'D':
            p1 = 0.0 if self.deterministic is not None else self.d[j]
        elif self.deterministic is not None:
            p1 = 1.0 if x[i - 1] == self.deterministic[j] else 0.0
        else:
            w = self.w[j]
            prev = x[i - 2] if i >= 2 else -1
            z = w[0] + w[1] * x[i - 1] + 0.5 * w[2] * prev + 0.3 * w[3] * i
            if self.end_dependent and j == 0:
                z += 2.5 * w[4] * (i / n_for_factor)
            p1 = sigmoid(z)
        q = [1.0 - p1, p1]
        if kind == 'M':
            for u in (0, 1):
                f = self.override.get((j, i, u))
                if f is not None:
                    q[u] *= f
        return q

    def q_span(self, j, x, n):
        w = self.w[j]
        p1 = sigmoid(w[0] + 0.4 * w[1] * n + w[2] * float(np.mean(x[:n])))
        return [1.0 - p1, p1]


# ======================================================================
# Αυτόματο προδιαγραφής (ελάχιστο κατά επίπεδα υπολειπόμενων συναρτήσεων)
# ======================================================================
class SpecAutomaton:
    """Σειρά μεταβλητών: έννοιες άγκυρας 1, ..., άγκυρας K, έπειτα έννοιες τμήματος.
    Κατάσταση στο επίπεδο k = κλάση ισοδυναμίας υπολειπόμενης συνάρτησης
    (ισοδύναμο με επίπεδο OBDD για αυτή τη σειρά)."""

    def __init__(self, spec, diags, K):
        self.spec, self.diags, self.K = spec, diags, K
        self.J = diags.J
        self.by_anchor = {k: [j for j in range(self.J) if diags.owners[j] == k] for k in range(1, K + 1)}
        self.span_vars = [j for j in range(self.J) if diags.owners[j] == 'span']
        self.levels = []          # levels[k] = dict residual_tuple -> id
        self.rep = []             # rep[k][id] = μερική ανάθεση (dict)
        fixed_order = []
        partials = [dict()]
        for k in range(0, K + 1):
            if k >= 1:
                fixed_order += self.by_anchor[k]
                newp = []
                for p in partials:
                    for bits in itertools.product((0, 1), repeat=len(self.by_anchor[k])):
                        q = dict(p)
                        q.update(dict(zip(self.by_anchor[k], bits)))
                        newp.append(q)
                partials = newp
            ids, reps = {}, []
            for p in partials:
                r = self.residual(p)
                if r not in ids:
                    ids[r] = len(reps)
                    reps.append(p)
            self.levels.append(ids)
            self.rep.append(reps)
            partials = reps            # αρκεί ένας εκπρόσωπος ανά κλάση
        self.W = [len(l) for l in self.levels]
        self.w0 = 0
        # μεταβάσεις δ_k(w, u_{J(k)})
        self.delta = {}
        for k in range(1, K + 1):
            for w, p in enumerate(self.rep[k - 1]):
                for bits in itertools.product((0, 1), repeat=len(self.by_anchor[k])):
                    q = dict(p)
                    q.update(dict(zip(self.by_anchor[k], bits)))
                    self.delta[(k, w, bits)] = self.levels[k][self.residual(q)]

    def residual(self, partial):
        rest = [j for j in range(self.J) if j not in partial]
        vals = []
        for bits in itertools.product((0, 1), repeat=len(rest)):
            u = [0] * self.J
            for j, b in partial.items():
                u[j] = b
            for j, b in zip(rest, bits):
                u[j] = b
            vals.append(int(self.spec(tuple(u))))
        return tuple(vals)

    def T(self, k, kind, i, x, n_for_factor):
        Jk = self.by_anchor[k]
        M = np.zeros((self.W[k - 1], self.W[k]))
        qs = [self.diags.q_anchor(j, kind, i, x, n_for_factor) for j in Jk]
        for bits in itertools.product((0, 1), repeat=len(Jk)):
            wgt = 1.0
            for qj, b in zip(qs, bits):
                wgt *= qj[b]
            for w in range(self.W[k - 1]):
                M[w, self.delta[(k, w, bits)]] += wgt
        return M

    def R(self, x, n):
        """R_w = Σ_{u_span} q_span(u_span | n) · residual_w(u_span)."""
        out = np.zeros(self.W[self.K])
        sv = self.span_vars
        qs = [self.diags.q_span(j, x, n) for j in sv]
        for w, p in enumerate(self.rep[self.K]):
            tot = 0.0
            for bits in itertools.product((0, 1), repeat=len(sv)):
                u = [0] * self.J
                for j, b in p.items():
                    u[j] = b
                wgt = 1.0
                for j, b, qj in zip(sv, bits, qs):
                    u[j] = b
                    wgt *= qj[b]
                tot += wgt * self.spec(tuple(u))
            out[w] = tot
        return out


# ======================================================================
# Product-trellis DP (μία διέλευση ανά αρχή, όλα τα τέλη)
# ======================================================================
def product_dp(prof, auto, x, N, n_for_factor=None, sum_emissions=False):
    K = prof.K
    W = auto.W
    fM = [[np.zeros(W[k]) for k in range(K + 1)] for _ in range(N + 1)]
    fI = [[np.zeros(W[k]) for k in range(K + 1)] for _ in range(N + 1)]
    fD = [[np.zeros(W[k]) for k in range(K + 1)] for _ in range(N + 1)]
    fM[0][0][auto.w0] = 1.0
    nf = N if n_for_factor is None else n_for_factor
    for i in range(N + 1):
        for k in range(K + 1):
            if i >= 1:
                if k >= 1:
                    inc = fM[i - 1][k - 1] * prof.tM[k - 1][0] + fI[i - 1][k - 1] * prof.tI[k - 1][0]
                    if k - 1 >= 1:
                        inc = inc + fD[i - 1][k - 1] * prof.tD[k - 1][0]
                    if sum_emissions:
                        acc = np.zeros(W[k])
                        for v in range(prof.V):
                            xx = list(x)
                            xx[i - 1] = v
                            acc += (inc @ auto.T(k, 'M', i, xx, nf)) * prof.eM[k][v]
                        fM[i][k] = acc
                    else:
                        fM[i][k] = (inc @ auto.T(k, 'M', i, x, nf)) * prof.eM[k][x[i - 1]]
                eI = 1.0 if sum_emissions else prof.eI[k][x[i - 1]]
                if k < K:
                    fI[i][k] = (fM[i - 1][k] * prof.tM[k][1] + fI[i - 1][k] * prof.tI[k][1]) * eI
                else:
                    fI[i][k] = (fM[i - 1][k] * (1 - prof.endM) + fI[i - 1][k] * (1 - prof.endI)) * eI
            if k >= 1:
                inc = fM[i][k - 1] * prof.tM[k - 1][2]
                if k - 1 >= 1:
                    inc = inc + fD[i][k - 1] * prof.tD[k - 1][1]
                fD[i][k] = inc @ auto.T(k, 'D', i, x, nf)
    ends = {}
    for n in range(1, N + 1):
        E = fM[n][K] * prof.endM + fI[n][K] * prof.endI + fD[n][K]
        ends[n] = E
    return ends


def dp_AB(prof, auto, x, N, **kw):
    ends = product_dp(prof, auto, x, N, **kw)
    return {n: (float(E.sum()), float(E @ auto.R(x, n))) for n, E in ends.items()}


# ======================================================================
# Εξαντλητική απαρίθμηση
# ======================================================================
def all_u(J):
    return list(itertools.product((0, 1), repeat=J))


def path_Q(diags, spec, ev, x, n, nf):
    """Q_f(X,π) = Σ_{u∈S} Π_j q_j(u_j | π)."""
    tot = 0.0
    qcache = []
    for j in range(diags.J):
        o = diags.owners[j]
        if o == 'span':
            qcache.append(diags.q_span(j, x, n))
        else:
            kind, i = ev[o]
            qcache.append(diags.q_anchor(j, kind, i, x, nf))
    for u in all_u(diags.J):
        if spec(u):
            w = 1.0
            for j, b in enumerate(u):
                w *= qcache[j][b]
            tot += w
    return tot, qcache


def brute_AB(prof, diags, spec, x, n, nf=None):
    nf = n if nf is None else nf
    A = B = 0.0
    for p, ev in prof.paths(x[:n]):
        Q, _ = path_Q(diags, spec, ev, x, n, nf)
        A += p
        B += p * Q
    return A, B


def groundings(prof, diags, spec, x, n):
    """m_AC, m_pool, m_vit, m_add και η μικτή κατανομή q*(u|X)."""
    paths = prof.paths(x[:n])
    A = sum(p for p, _ in paths)
    J = diags.J
    qstar = np.zeros(2 ** J)
    qbar = np.zeros((J, 2))
    best = max(paths, key=lambda t: t[0])
    m_ac = 0.0
    for p, ev in paths:
        w = p / A
        Q, qc = path_Q(diags, spec, ev, x, n, n)
        m_ac += w * Q
        for idx, u in enumerate(all_u(J)):
            pr = 1.0
            for j, b in enumerate(u):
                pr *= qc[j][b]
            qstar[idx] += w * pr
        for j in range(J):
            qbar[j] += w * np.array(qc[j])

    def m_from_product(qc):
        tot = 0.0
        for u in all_u(J):
            if spec(u):
                pr = 1.0
                for j, b in enumerate(u):
                    pr *= qc[j][b]
                tot += pr
        return tot

    m_pool = m_from_product(qbar)
    m_vit, _ = path_Q(diags, spec, best[1], x, n, n)
    K = prof.K
    ev_add = {k: ('M', min(n, max(1, round(k * n / K)))) for k in range(1, K + 1)}
    m_add, _ = path_Q(diags, spec, ev_add, x, n, n)
    return m_ac, m_pool, m_vit, m_add, qstar, paths


# ======================================================================
# Οι έλεγχοι
# ======================================================================
SPEC_MAIN = lambda u: int((u[0] or u[1]) and ((not u[2]) or u[0]) and u[3])   # (u1∨u2)∧(¬u3∨u1)∧u4
OWNERS_MAIN = [1, 2, 3, 'span']


def test_O6a():
    p = np.array([.6, .3, .1]); q1 = np.array([.8, .5, .2]); q2 = np.array([.9, .1, .7])
    m_ac = float(np.sum(p * (1 - (1 - q1) * (1 - q2))))
    a, b = float(p @ q1), float(p @ q2)
    m_naive = 1 - (1 - a) * (1 - b)
    ok = abs(m_ac - 0.829) < 1e-12 and abs(m_naive - 0.874) < 1e-12
    report("O6a", ok, f"Gemini toy: m_AC={m_ac:.3f}, pooled/naive={m_naive:.3f} (μόνο 3 δοσμένες διαδρομές, όχι trellis)")


def test_O6(n_seeds=25):
    worst = 0.0
    n_checks = 0
    widths = None
    for s in range(n_seeds):
        rng = np.random.default_rng(100 + s)
        K, V, N = 3, 3, 6
        prof = Profile(K, V, rng)
        diags = Diagnostics(OWNERS_MAIN, rng)
        auto = SpecAutomaton(SPEC_MAIN, diags, K)
        widths = auto.W
        x = list(rng.integers(0, V, size=N))
        dp = dp_AB(prof, auto, x, N)
        for n in range(1, N + 1):
            A_b, B_b = brute_AB(prof, diags, SPEC_MAIN, x, n)
            A_d, B_d = dp[n]
            for d, b in ((A_d, A_b), (B_d, B_b)):
                if b > 0:
                    worst = max(worst, abs(d - b) / b)
            n_checks += 1
    report("O6", worst < 1e-10,
           f"{n_seeds} σπόροι × 6 τέλη ({n_checks} τμήματα), K=3, V=3, M/I/D· "
           f"max σχετ. σφάλμα A,B = {worst:.1e}· πλάτη αυτομάτου ανά επίπεδο {widths}")


def test_O6g():
    rng = np.random.default_rng(7)
    K, V, N = 3, 3, 5
    prof = Profile(K, V, rng)
    diags = Diagnostics(OWNERS_MAIN, rng)
    auto = SpecAutomaton(SPEC_MAIN, diags, K)
    x = list(rng.integers(0, V, size=N))
    n = N
    worst = 0.0
    eps = 1e-6
    count = 0
    paths = prof.paths(x[:n])
    _, B0 = brute_AB(prof, diags, SPEC_MAIN, x, n)
    for j in range(3):                      # έννοιες άγκυρας
        k = diags.owners[j]
        for i in range(1, n + 1):
            for u in (0, 1):
                # αναλυτικά: P(άγκυρα k στο M,i , u_j=u | X, U∈S)
                num = 0.0
                for p, ev in paths:
                    if ev[k] != ('M', i):
                        continue
                    _, qc = path_Q(diags, SPEC_MAIN, ev, x, n, n)
                    for uu in all_u(diags.J):
                        if uu[j] == u and SPEC_MAIN(uu):
                            pr = 1.0
                            for jj, b in enumerate(uu):
                                pr *= qc[jj][b]
                            num += p * pr
                analytic = num / B0
                vals = []
                for sgn in (+1, -1):
                    diags.override = {(j, i, u): math.exp(sgn * eps)}
                    vals.append(math.log(dp_AB(prof, auto, x, N)[n][1]))
                diags.override = {}
                fd = (vals[0] - vals[1]) / (2 * eps)
                worst = max(worst, abs(fd - analytic))
                count += 1
    report("O6g", worst < 1e-7,
           f"{count} παράγωγοι ∂logB/∂log q_j(u|M,i): DP (κεντρικές διαφορές) έναντι "
           f"δεσμευμένης περιθώριας από απαρίθμηση, max |διαφορά| = {worst:.1e}")


def test_O6r():
    rng = np.random.default_rng(11)
    K, V, N = 3, 3, 6
    prof = Profile(K, V, rng)
    diags = Diagnostics(OWNERS_MAIN, rng, end_dependent=True)
    auto = SpecAutomaton(SPEC_MAIN, diags, K)
    x = list(rng.integers(0, V, size=N))
    naive = dp_AB(prof, auto, x, N, n_for_factor=N)      # επαναχρησιμοποίηση προθέματος
    worst_naive = worst_per_end = 0.0
    for n in range(1, N + 1):
        _, B_b = brute_AB(prof, diags, SPEC_MAIN, x, n, nf=n)
        worst_naive = max(worst_naive, abs(naive[n][1] - B_b) / B_b)
        per_end = dp_AB(prof, auto, x, n, n_for_factor=n)[n][1]   # DP ανά τέλος
        worst_per_end = max(worst_per_end, abs(per_end - B_b) / B_b)
    report("O6r-naive", worst_naive > 1e-3,
           f"(ΑΝΑΜΕΝΟΜΕΝΗ ΑΠΟΤΥΧΙΑ ακρίβειας) q_1 εξαρτάται από i/n: επαναχρησιμοποίηση "
           f"προθέματος δίνει σχετ. σφάλμα έως {worst_naive:.2e}")
    report("O6r-end", worst_per_end < 1e-10,
           f"ίδια μοντέλα, DP ανά τέλος (κόστος ×L): σχετ. σφάλμα {worst_per_end:.1e}")


def test_O7():
    rng = np.random.default_rng(23)
    K, V, n = 3, 3, 5
    prof = Profile(K, V, rng)
    x = list(rng.integers(0, V, size=n))
    owners = [1, 2, 3, 'span']
    diags = Diagnostics(owners, rng)
    # (i) μόνο έννοια τμήματος
    spec_i = lambda u: int(u[3])
    m_ac, m_pool, m_vit, m_add, _, _ = groundings(prof, diags, spec_i, x, n)
    ok_i = abs(m_ac - m_add) < TOL and abs(m_ac - m_pool) < TOL
    # (ii) μονό literal σε άγκυρα
    spec_ii = lambda u: int(u[1])
    a2, p2, v2, ad2, _, _ = groundings(prof, diags, spec_ii, x, n)
    ok_ii = abs(a2 - p2) < TOL
    # (iii) ντετερμινιστική στοίχιση
    prof_det = Profile(K, V, np.random.default_rng(5), deterministic=True)
    xd = list(rng.integers(0, V, size=K))
    a3, p3, v3, _, _, paths3 = groundings(prof_det, diags, SPEC_MAIN, xd, K)
    ok_iii = len(paths3) == 1 and abs(a3 - p3) < TOL and abs(a3 - v3) < TOL
    # (iv) συνδιακυμάνσεις
    spec_and = lambda u: int(u[0] and u[2])
    spec_or = lambda u: int(u[0] or u[2])
    a_and, p_and, _, _, _, paths = groundings(prof, diags, spec_and, x, n)
    a_or, p_or, _, _, _, _ = groundings(prof, diags, spec_or, x, n)
    A = sum(p for p, _ in paths)
    y1 = np.array([path_Q(diags, lambda u: int(u[0]), ev, x, n, n)[0] for _, ev in paths])
    y3 = np.array([path_Q(diags, lambda u: int(u[2]), ev, x, n, n)[0] for _, ev in paths])
    w = np.array([p for p, _ in paths]) / A
    cov = float(w @ (y1 * y3) - (w @ y1) * (w @ y3))
    ok_iv = abs((a_and - p_and) - cov) < TOL and abs((a_or - p_or) + cov) < TOL
    # (v) γενική
    a5, p5, v5, ad5, _, _ = groundings(prof, diags, SPEC_MAIN, x, n)
    distinct = min(abs(a5 - p5), abs(a5 - v5), abs(a5 - ad5)) > 1e-4
    report("O7-i", ok_i, f"μόνο έννοια τμήματος: m_AC={m_ac:.6f} = m_Add={m_add:.6f} = m_Pool")
    report("O7-ii", ok_ii, f"μονό literal: m_AC={a2:.6f} = m_Pool={p2:.6f} (Viterbi={v2:.4f}, Add={ad2:.4f})")
    report("O7-iii", ok_iii, f"βέβαιη στοίχιση: m_AC={a3:.6f} = m_Pool = m_Vit")
    report("O7-iv", ok_iv, f"u1∧u3: AC−Pool={a_and - p_and:+.6f} = Cov={cov:+.6f}· u1∨u3: AC−Pool={a_or - p_or:+.6f} = −Cov")
    report("O7-v", distinct, f"γενική: AC={a5:.4f}, Pool={p5:.4f}, Vit={v5:.4f}, Add={ad5:.4f}")


def test_O7r():
    rng = np.random.default_rng(31)
    K, V, n = 3, 3, 5
    prof = Profile(K, V, rng)
    owners = [1, 2, 3]
    diags = Diagnostics(owners, rng)
    x = list(rng.integers(0, V, size=n))
    _, _, _, _, qstar, _ = groundings(prof, diags, lambda u: 1, x, n)
    U = all_u(3)
    worst = 0.0
    for mask in range(1, 2 ** 8):            # όλες οι μη κενές προδιαγραφές
        spec = (lambda m: (lambda u: (m >> U.index(tuple(u))) & 1))(mask)
        auto = SpecAutomaton(spec, diags, K)
        A, B = dp_AB(prof, auto, x, n)[n]
        m_dp = B / A
        m_mix = sum(qstar[idx] for idx, u in enumerate(U) if (mask >> idx) & 1)
        worst = max(worst, abs(m_dp - m_mix))
    report("O7r", worst < 1e-12,
           f"255 μη κενές προδιαγραφές: m_AC(DP) = Σ_{{u∈S}} q*(u|X), max |διαφορά| = {worst:.1e} "
           f"⇒ AC-ECSI ≡ ECSI-D με q* = μείγμα γινομένων")


def test_O7e():
    # δύο έννοιες στην ίδια άγκυρα, βέβαιη στοίχιση: q* = γινόμενο ⇒ P(u1=u2) ≤ max_{a,b} ab+(1-a)(1-b)
    # με περιθώρια 1/2: P(u1=u2) = 1/2, ενώ ο στόχος q(00)=q(11)=1/2 έχει P(u1=u2)=1.
    rng = np.random.default_rng(3)
    K, V = 2, 3
    prof = Profile(K, V, rng, deterministic=True)
    diags = Diagnostics([1, 1], rng)                 # δύο έννοιες στην άγκυρα 1
    diags.w = [np.zeros(5), np.zeros(5)]             # q_j(1|M,i) = σ(0) = 1/2
    x = [0, 1]
    m_ac, _, _, _, qstar, paths = groundings(prof, diags, lambda u: int(u[0] == u[1]), x, K)
    best = m_ac
    report("O7e", abs(best - 0.5) < 1e-12 and len(paths) == 1,
           f"ίδια άγκυρα, βέβαιη στοίχιση, περιθώρια 1/2: m(u1↔u2) = {best:.3f} ≠ 1 (στόχος) — "
           f"η εξάρτηση της AC προέρχεται ΜΟΝΟ από την αβεβαιότητα στοίχισης")


def test_O8():
    rng = np.random.default_rng(41)
    K, V, N = 3, 3, 5
    spec = lambda u: int((u[0] or u[1]) and ((not u[2]) or u[0]))
    out = []
    worst = 0.0
    for fam in range(2):
        prof = Profile(K, V, rng)
        targets = {0: int(np.argmax(prof.eM[1])), 1: int(np.argmax(prof.eM[2])), 2: int(np.argmin(prof.eM[3]))}
        diags = Diagnostics([1, 2, 3], rng, deterministic=targets)
        auto = SpecAutomaton(spec, diags, K)
        Zb = Ab = 0.0
        for n in range(1, N + 1):
            for x in itertools.product(range(V), repeat=n):
                A, B = brute_AB(prof, diags, spec, list(x), n)
                Zb += B
                Ab += A
        ends = product_dp(prof, auto, [0] * N, N, sum_emissions=True)
        Zd = sum(float(E @ auto.R([0] * N, n)) for n, E in ends.items())
        Ad = sum(float(E.sum()) for E in ends.values())
        worst = max(worst, abs(Zd - Zb) / Zb, abs(Ad - Ab) / Ab)
        out.append((Zb, Ab))
    nS = sum(spec(u) for u in all_u(3))   # αναφορά: ομοιόμορφη r(u) στο {0,1}^3 ⇒ r_f = |S|/8
    r_f = nS / 8
    offs = [math.log((Z / A) / r_f) for Z, A in out]
    report("O8", worst < 1e-10,
           f"Z_f με άθροιση εκπομπών στο trellis = Σ_X B_f(X) (|X|≤5, 363 ακολουθίες), σχετ. σφάλμα {worst:.1e}· "
           f"P(S|f,|X|≤5) = {out[0][0] / out[0][1]:.4f}, {out[1][0] / out[1][1]:.4f} έναντι r_f={r_f:.3f} ⇒ "
           f"μετατόπιση log(Z_f/r_f) = {offs[0]:+.3f}, {offs[1]:+.3f} nats (διαφορετική ανά οικογένεια)")


def test_O9():
    rng = np.random.default_rng(53)
    U = all_u(3)
    r = rng.random(8) + 0.1; r /= r.sum()
    M = 6
    L = rng.random((8, M)) + 0.05                       # ℓ(X | u)
    L /= L.sum(axis=1, keepdims=True)
    worst_ok = 0.0
    worst_bad = 0.0
    r_bad = rng.random(8) + 0.1; r_bad /= r_bad.sum()
    for mask in range(1, 2 ** 8):
        S = np.array([(mask >> i) & 1 for i in range(8)], dtype=float)
        r_f = float(r @ S)
        for X in range(M):
            pr = float(r @ L[:, X])
            q = r * L[:, X] / pr                        # posterior υπό r
            m = float(q @ S)
            p_f = float((r * S) @ L[:, X]) / r_f        # r περικομμένη στο S_f
            worst_ok = max(worst_ok, abs(m / r_f - p_f / pr))
            qb = r_bad * L[:, X] / float(r_bad @ L[:, X])
            worst_bad = max(worst_bad, abs(float(qb @ S) / r_f - p_f / pr))
    report("O9", worst_ok < 1e-12 and worst_bad > 1e-3,
           f"m_f/r_f = Bayes factor p(X|f)/p_r(X) για όλες τις 255 S και 6 X (σφάλμα {worst_ok:.1e})· "
           f"με q βαθμονομημένη σε άλλο prior η ταυτότητα παύει (απόκλιση έως {worst_bad:.2f})")


def test_O10():
    rng = np.random.default_rng(61)
    K, V, n = 3, 3, 6
    prof = Profile(K, V, rng)
    diags = Diagnostics(OWNERS_MAIN, rng)
    x = list(rng.integers(0, V, size=n))
    m_ac, _, _, _, _, paths = groundings(prof, diags, SPEC_MAIN, x, n)
    A = sum(p for p, _ in paths)
    w = np.array([p for p, _ in paths]) / A
    Q = np.array([path_Q(diags, SPEC_MAIN, ev, x, n, n)[0] for _, ev in paths])
    S = 4000
    idx = rng.choice(len(paths), size=S, p=w)
    est = float(Q[idx].mean())
    se = float(Q[idx].std(ddof=1) / math.sqrt(S))
    report("O10", abs(est - m_ac) < 4 * se,
           f"MC με {S} στοιχίσεις από το ακριβές posterior: m̂={est:.4f} ± {se:.4f} (ακριβές {m_ac:.4f}) "
           f"— αμερόληπτο, όχι ακριβές· {len(paths)} διαδρομές για n={n}")


def test_O11():
    class D:
        pass
    rng = np.random.default_rng(1)
    widths = {}
    for m in (1, 2, 3):
        K = 2 * m
        owners = list(range(1, K + 1))
        diags = Diagnostics(owners, rng)
        spec = (lambda mm: (lambda u: int(all(u[t] == u[t + mm] for t in range(mm)))))(m)
        auto = SpecAutomaton(spec, diags, K)
        widths[m] = max(auto.W)
    ok = all(widths[m] == 2 ** m + 1 or widths[m] == 2 ** m for m in widths)
    report("O11", ok,
           f"προδιαγραφή ∧_t (u_t = u_(t+m)) σε 2m άγκυρες: μέγιστο πλάτος {widths} "
           f"(≈2^m) — το μικρό πλάτος ΔΕΝ είναι δεδομένο")


def test_O12(n_inst=300):
    """Περιγραφικό (όχι PASS/FAIL): μέγεθος των διαφορών ανάμεσα στους τρόπους
    γείωσης και συσχέτιση της διαφοράς AC−Pool με την εντροπία του posterior στοίχισης."""
    d_joint, d_align, d_soft, ent = [], [], [], []
    for s in range(n_inst):
        rng = np.random.default_rng(1000 + s)
        K, V, n = 3, 3, int(rng.integers(4, 8))
        prof = Profile(K, V, rng)
        diags = Diagnostics(OWNERS_MAIN, rng)
        x = list(rng.integers(0, V, size=n))
        m_ac, m_pool, m_vit, m_add, _, paths = groundings(prof, diags, SPEC_MAIN, x, n)
        A = sum(p for p, _ in paths)
        w = np.array([p for p, _ in paths]) / A
        ent.append(float(-(w * np.log2(w)).sum()))
        d_joint.append(abs(math.log(m_ac) - math.log(m_pool)))
        d_align.append(abs(math.log(m_pool) - math.log(m_add)))
        d_soft.append(abs(math.log(m_ac) - math.log(m_vit)))
    q = lambda v, p: float(np.quantile(v, p))
    rho = float(np.corrcoef(np.argsort(np.argsort(ent)), np.argsort(np.argsort(d_joint)))[0, 1])
    print(f"O12      INFO  {n_inst} τυχαία στιγμιότυπα, |Δ log m| διάμεσος / 90ό εκατοστημόριο: "
          f"AC−Pool {q(d_joint, .5):.3f}/{q(d_joint, .9):.3f} · Pool−Add {q(d_align, .5):.3f}/{q(d_align, .9):.3f} · "
          f"AC−Vit {q(d_soft, .5):.3f}/{q(d_soft, .9):.3f} nats· Spearman(H(π|X), |AC−Pool|) = {rho:+.2f}")


if __name__ == "__main__":
    test_O6a()
    test_O6()
    test_O6g()
    test_O6r()
    test_O7()
    test_O7r()
    test_O7e()
    test_O8()
    test_O9()
    test_O10()
    test_O11()
    test_O12()
    bad = [n for n, ok in RESULTS if not ok]
    print("-" * 70)
    print(f"Σύνολο: {len(RESULTS)} έλεγχοι· αποτυχίες: {bad if bad else 'καμία'}")
    sys.exit(0 if not bad else 1)

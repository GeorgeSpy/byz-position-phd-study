"""Regression counterexample for sum_emissions=True in claude_ac_ecsi_oracle.py.
Requires numpy and the original oracle script in the same directory.
Run: python -I oracle_Zf_context_counterexample.py
The discrepancy is EXPECTED and proves the original O8 does not cover
anchor diagnostics depending on the previous observed symbol x[i-1].
"""
import importlib.util
import itertools
from pathlib import Path
import numpy as np

src = Path(__file__).with_name('claude_ac_ecsi_oracle.py')
specification = importlib.util.spec_from_file_location('source_oracle',src)
c = importlib.util.module_from_spec(specification)
specification.loader.exec_module(c)

for seed in (60, 61, 62):
    rng = np.random.default_rng(seed)
    K, V, N = 2, 3, 4
    prof = c.Profile(K, V, rng)
    diags = c.Diagnostics([1, 2], rng)
    for w in diags.w:
        w[2] = 7.0  # explicit dependence on x[i-1] used by q_anchor
    rule = lambda u: int(u[0] and u[1])
    autom = c.SpecAutomaton(rule, diags, K)

    Z_brute = A_brute = 0.0
    for n in range(1, N + 1):
        for seq in itertools.product(range(V), repeat=n):
            A, B = c.brute_AB(prof, diags, rule, list(seq), n)
            A_brute += A
            Z_brute += B

    # Original proposed same-trellis sum_emissions implementation.
    ends = c.product_dp(prof, autom, [0]*N, N, sum_emissions=True)
    Z_dp = sum(float(E @ autom.R([0]*N, n)) for n,E in ends.items())
    A_dp = sum(float(E.sum()) for E in ends.values())
    rel_error = abs(Z_dp-Z_brute)/Z_brute
    assert abs(A_dp-A_brute) < 1e-10
    assert rel_error > 0.1, "Counterexample unexpectedly vanished; re-audit implementation"
    print(f"seed={seed}: enumerated Z={Z_brute:.7f}; summed-trellis Z={Z_dp:.7f}; "
          f"relative discrepancy={100*rel_error:.2f}% (EXPECTED)")
print('PASS: uncovered limitation of original O8 reproduced.')

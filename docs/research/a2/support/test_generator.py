"""Regression tests for the acceptance rules of the perturbation generator (protocol v16.5 §K.5).

1. A swap inside one alternative group leaves the family's canonical card unchanged and
   must be rejected even when another family changes.
2. Two permutation keys that give the same canonical bank are the same perturbation.
3. An unknown truth value (phi = ?) is not a satisfaction witness.
4. A positive LP value with unacceptable residuals must be rejected.
5. A genuine perturbation on the full binary cube is accepted with a verified certificate.
"""
from unittest.mock import patch

import numpy as np

import generator_feasibility as g

CUBE = np.array([[i >> j & 1 for j in range(6)] for i in range(64)], float)
CONCEPTS = [dict(block='pat', var=j, p=.5, m=0.) for j in range(6)]
V = [dict(R=[0], A=[[1, 2]], E=[3]), dict(R=[4], A=[], E=[])]


def run_with(tau, lp=None):
    patches = [patch.object(g, 'make_bank', return_value=CONCEPTS),
               patch.object(g, 'make_specs', return_value=V),
               patch.object(g, 'simulate_data', return_value=(np.zeros(len(CUBE)), CUBE)),
               patch.object(g, 'propose', return_value=np.array(tau))]
    if lp is not None:
        patches.append(patch.object(g, 'lp_cert', return_value=lp))
    for p in patches:
        p.start()
    try:
        return g.run_bank(0, 2, True, target=1, cap=1, cap_sec=20.)
    finally:
        for p in patches:
            p.stop()


def test_swap_inside_alternative_group_rejected():
    out = run_with([0, 2, 1, 3, 5, 4])                 # family 1 keeps its card, family 2 changes
    assert out['accepted'] == 0 and out['reasons']['family_unchanged'] == 1, out['reasons']


def test_canonical_duplicate_keys():
    a = g.canonical([dict(R=[4], A=[[1, 2]], E=[3])])
    b = g.canonical([dict(R=[4], A=[[2, 1]], E=[3])])
    assert a == b


def test_unknown_is_not_witness():
    _, phi, v = g.Q_phi(np.array([[-1.], [0.]]), dict(R=[0], A=[], E=[]))
    assert not (phi == 1).any() and list(v) == [0., 1.]


def test_bad_residual_rejected():
    bad = dict(value=.5, status=0, primal_residual=.01, dual_residual=0., duality_gap=.1, dual_bound=.5)
    out = run_with([5, 1, 2, 3, 0, 4], lp=bad)           # a genuine change in both families
    assert out['accepted'] == 0 and out['reasons']['lp_F'] == 1, out['reasons']


def test_genuine_change_accepted_with_certificate():
    out = run_with([5, 1, 2, 3, 0, 4])
    assert out['accepted'] == 1, out['reasons']
    assert out['lp_max_primal_residual'] <= g.LP_TOL and out['lp_max_dual_residual'] <= g.LP_TOL
    assert out['lp_min_dual_bound'] > g.CERT_MIN


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for t in tests:
        t()
    print(f'generator acceptance regression tests: {len(tests)}/{len(tests)} PASS')

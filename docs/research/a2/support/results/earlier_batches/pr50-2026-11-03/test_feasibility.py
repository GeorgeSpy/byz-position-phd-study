"""Regression checks for scientific failure modes of the feasibility tools."""
import unittest
import json
import numpy as np
from sklearn.metrics import average_precision_score
import synthetic_scores as s
from synthetic_concepts import evaluate, apply_tau
from feasibility_generator import canonical, lp_bound, run
from feasibility_stats import holm
from feasibility_heads import ap_fixed


class ScientificChecks(unittest.TestCase):
    def test_AP_tie_blocks_and_absent_family(self):
        rng = np.random.default_rng(17)
        for _ in range(40):
            y = rng.integers(0, 2, (30, 3)).astype(float)
            p = rng.integers(0, 5, (2, 2, 30, 3)).astype(float)
            order, ys, ends = s.prep(p, y)
            actual = s.ap_fam(order, ys, ends, np.ones((1, 30)))[0]
            for c in range(2):
                for r in range(2):
                    for f in range(3):
                        self.assertAlmostEqual(actual[c, r, f], average_precision_score(y[:, f], p[c, r, :, f]))
        y[:, 0] = 0
        order, ys, ends = s.prep(p, y)
        self.assertTrue(np.isnan(s.ap_fam(order, ys, ends, np.ones((1, 30)))[..., 0]).all())
        self.assertIsNone(ap_fixed(np.ones((3, 2))*.5, np.array([0, 0, 0]), 2))

    def test_unknown_is_separate_from_true(self):
        q, v, phi = evaluate(np.array([[-1], [0], [1]]), dict(R=[0], G=[], E=[]))
        np.testing.assert_array_equal(phi, [.5, 0, 1])
        np.testing.assert_array_equal(v, [0, 1, 0])
        np.testing.assert_array_equal(q[:, 0], [0, -1, 1])

    def test_semantically_duplicate_permutations(self):
        V = dict(R=[0], G=[[1, 2]], E=[3])
        a = apply_tau(V, [4, 1, 2, 3, 0]); b = apply_tau(V, [4, 2, 1, 3, 0])
        self.assertEqual(canonical([a]), canonical([b]))

    def test_LP_identity_and_verified_positive_bound(self):
        X = np.array([[i >> j & 1 for j in range(5)] for i in range(32)])
        V = dict(R=[0], G=[[1, 2]], E=[3]); P = dict(V, R=[4])
        q, v, _ = evaluate(X, V); qp, vp, _ = evaluate(X, P)
        for structured in [False, True]:
            identity = lp_bound(q, v, q, v, structured)
            different = lp_bound(q, v, qp, vp, structured)
            self.assertTrue(identity['verified']); self.assertLessEqual(identity['lower'], 0)
            self.assertTrue(different['verified']); self.assertGreater(different['lower'], .19)

    def test_generator_serializes_replayable_certificates(self):
        result = run(seed=400, target=1, cap=100, seconds=30.)
        self.assertEqual(result['stop'], 'target_reached')
        self.assertEqual(len(result['accepted']), 1)
        self.assertTrue(result['witness_sha256'])
        self.assertTrue(result['accepted'][0]['dD']['primal_solution'])
        json.dumps(result, allow_nan=False)

    def test_Holm_hierarchy(self):
        self.assertEqual(holm(np.array([.01, .02])).tolist(), [True, True])
        self.assertEqual(holm(np.array([.02, .02])).tolist(), [False, False])
        self.assertEqual(holm(np.array([.01, .04])).tolist(), [True, False])


if __name__ == '__main__':
    unittest.main()

"""Small, synthetic regression tests for the public A2 knowledge operators."""
import itertools
import unittest

import numpy as np
try:
    from sklearn.metrics import average_precision_score
except ImportError:  # Optional independent cross-check
    average_precision_score = None

from a2_core import (Scores, _and, _or, ap_with_ties, canonical, certify_lp,
                     evaluate, factorial_contrasts, jackknife_t, logits,
                     macro_ap, pooled_seed_ap, propose_perturbations)


class TestCore(unittest.TestCase):
    def test_kleene_complete_truth_tables(self):
        for state in itertools.product((-1, 0, 1), repeat=4):
            ref_and = 0 if 0 in state else -1 if -1 in state else 1
            ref_or = 1 if 1 in state else -1 if -1 in state else 0
            self.assertEqual(_and(list(state)), ref_and)
            self.assertEqual(_or(list(state)), ref_or)

    def test_required_alternative_exclusion_and_missing(self):
        spec = {"F": {"R": ["r"], "A": [["a", "b"]], "E": ["e"]}}
        concepts = ["r", "a", "b", "e"]
        arr = np.array([[1, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 1],
                        [1, 0, 0, 0], [0, 1, 0, 0]], dtype=float)
        mask = np.ones_like(arr)
        mask[3, 1:3] = 0
        s = evaluate(arr, mask, concepts, spec)
        self.assertEqual(s.truth[:, 0].tolist(), [1, 0, 0, -1, 0])
        self.assertEqual(s.penalty[:, 0].tolist(), [0, 1, 1, 0, 1])
        self.assertTrue(np.all(s.q <= 1) and np.all(s.q >= -1))

    def test_all_unobserved_is_unknown_and_unpenalized(self):
        spec = {"F": {"R": ["r"], "A": [["a"]], "E": ["e"]}}
        z = np.zeros((3, 3))
        s = evaluate(z, z, ["r", "a", "e"], spec)
        np.testing.assert_allclose(s.q, 0)
        np.testing.assert_allclose(s.penalty, 0)
        self.assertEqual(s.truth.tolist(), [[-1], [-1], [-1]])

    def test_empty_roles_are_neutral(self):
        spec = {"F": {"R": [], "A": [], "E": []}}
        s = evaluate(np.zeros((2, 1)), np.ones((2, 1)), ["unused"], spec)
        self.assertEqual(s.truth.tolist(), [[1], [1]])
        np.testing.assert_allclose(s.q, 0)

    def test_weight_and_lambda_domains(self):
        spec = {"F": {"R": ["r"], "A": [], "E": []}}
        s = evaluate(np.array([[0.], [1.]]), np.ones((2, 1)), ["r"], spec)
        base = np.zeros((2, 1))
        np.testing.assert_allclose(logits(base, s, np.array([.6, .2, .2]), 0),
                                   np.array([[-.6], [.6]]))
        np.testing.assert_allclose(logits(base, s, np.array([.6, .2, .2]), .5),
                                   np.array([[-1.1], [.6]]))
        with self.assertRaises(ValueError):
            logits(base, s, np.array([1., 0., 0.]), .2)

    def test_lp_identity_and_swap(self):
        qv = np.array([[[1, 1, 1], [-1, -1, 1]], [[-1, 1, 1], [1, -1, 1]]], float)
        vv = np.array([[0, 1], [1, 0]], float)
        x = Scores(qv, vv, np.ones((2, 2), np.int8))
        y = Scores(qv[:, ::-1, :], vv[:, ::-1], np.ones((2, 2), np.int8))
        self.assertLess(certify_lp(x, x, False)["distance"], 1e-9)
        d_f = certify_lp(x, y, False)
        d_d = certify_lp(x, y, True)
        self.assertTrue(d_f["certified"] and d_d["certified"])
        self.assertGreater(d_d["conservative_lower_bound"], 1e-6)
        self.assertLessEqual(d_d["distance"], d_f["distance"] + 1e-8)

    def test_perturbation_immobile_family(self):
        spec = {"F": {"R": ["r"], "A": [], "E": []}}
        got, d = propose_perturbations(spec, ["r"], {"r": "c"},
                np.array([[0], [1]]), np.ones((2, 1)), count=1)
        self.assertEqual(got, [])
        self.assertEqual(d["termination"], "immobile_family")

    def test_generator_certifies_a_real_change(self):
        names = ["r", "e", "a", "b"]
        states = np.array(list(itertools.product((0, 1), repeat=4)), dtype=float)
        spec = {"F1": {"R": ["r"], "A": [["a", "b"]], "E": ["e"]},
                "F2": {"R": ["e"], "A": [["a", "b"]], "E": ["r"]}}
        found, meta = propose_perturbations(spec, names, {x: "pitch" for x in names},
                                            states, np.ones_like(states),
                                            count=1, max_proposals=200, seed=17)
        self.assertEqual(meta["termination"], "target_reached")
        self.assertEqual(len(found), 1)
        self.assertTrue(found[0]["d_F"]["certified"] and found[0]["d_D"]["certified"])

    def test_canonical_reorders_commutative_roles(self):
        a = {"R": ["a", "b"], "A": [["c", "d"], ["e"]], "E": ["f"]}
        b = {"R": ["b", "a"], "A": [["e"], ["d", "c"]], "E": ["f"]}
        self.assertEqual(canonical(a), canonical(b))

    def test_ap_matches_sklearn_with_ties(self):
        if average_precision_score is None:
            self.skipTest("scikit-learn optional reference implementation is not installed")
        rng = np.random.default_rng(91)
        for _ in range(200):
            y = rng.integers(0, 2, size=30)
            if not y.any():
                y[0] = 1
            scores = rng.integers(0, 5, size=30) / 4
            self.assertAlmostEqual(ap_with_ties(y, scores), average_precision_score(y, scores), places=13)

    def test_missing_positive_raises(self):
        with self.assertRaises(ValueError):
            ap_with_ties(np.zeros(5, dtype=int), np.linspace(0, 1, 5))

    def test_pooling_by_seed(self):
        y = np.array(["a", "b", "b", "a"] * 2)
        g = np.array(["g1", "g2", "g3", "g4"] * 2)
        seeds = np.array([0] * 4 + [1] * 4)
        p = np.array([[.9, .1], [.2, .8], [.3, .7], [.8, .2]] * 2)
        self.assertAlmostEqual(pooled_seed_ap(y, g, seeds, p, ["a", "b"]), 1.)
        self.assertAlmostEqual(macro_ap(y[:4], p[:4], ["a", "b"]), 1.)

    def test_jackknife_group_sampling(self):
        labels = np.arange(8)
        groups = np.repeat(np.arange(4), 2)
        val = np.arange(8, dtype=float)
        d = jackknife_t(labels, groups, lambda mask: float(val[mask].mean()))
        self.assertEqual(d["n_groups"], 4)
        self.assertGreater(d["se"], 0)
        self.assertLess(d["ci95"][0], d["estimate"])
        self.assertGreater(d["ci95"][1], d["estimate"])

    def test_factorial_identity(self):
        d = factorial_contrasts(.65, .61, .68, .62)
        self.assertAlmostEqual(d["knowledge"], .05)
        self.assertAlmostEqual(d["logic_valid"], .03)
        self.assertAlmostEqual(d["structure"] + d["interaction"] / 2, d["logic_valid"])


if __name__ == "__main__":
    unittest.main()

"""Deterministic synthetic verification of A2-S3 reference oracles."""
import math
import random
import unittest

from a2s3_reference import (
    Span, admissible_variant, choose_endpoint, enumerate_logprobs,
    exact_length_features, family_balanced_mean, forward_logprobs,
    jackknife_t, shared_window, two_sided_finding,
)


class ProbabilityTests(unittest.TestCase):
    def test_union_matches_independent_enumeration_120_cases(self):
        for seed in range(120):
            rng = random.Random(seed)
            n = rng.randint(2, 7)
            skip = [rng.uniform(-2, 1) for _ in range(n)]
            scores = {(i, j, f): rng.uniform(-2, 2)
                      for i in range(n)
                      for j in range(i, min(n, i + 3))
                      for f in ("a", "b")}
            accepted = {k for k in scores if rng.random() < 0.17}
            if not accepted:
                accepted = {next(iter(scores))}
            dp = forward_logprobs(n, skip, scores, accepted)
            oracle = enumerate_logprobs(n, skip, scores, accepted)
            self.assertAlmostEqual(dp[0], oracle[0], places=11)
            self.assertAlmostEqual(dp[1], oracle[1], places=11)

    def test_singleton_probability_and_log_contrast(self):
        scores = {(0, 1, "f"): -40.0, (0, 2, "f"): -50.0, (1, 2, "f"): -60.0}
        accepted = {(0, 1, "f")}
        x, norm = forward_logprobs(3, [0., 0., 0.], scores, accepted)
        y, norm2 = forward_logprobs(3, [0., 0., 0.], scores, {(0, 2, "f")})
        self.assertAlmostEqual(norm, norm2)
        self.assertAlmostEqual(x - y, 10.0, places=10)

    def test_overlapping_accepted_compatible_union_not_double_counted(self):
        scores = {(0, 1, "f"): 1.0, (0, 2, "f"): 0.5, (2, 3, "f"): 0.1}
        accepted = {(0, 1, "f"), (0, 2, "f")}
        a, _ = forward_logprobs(4, [0.] * 4, scores, accepted)
        self.assertLessEqual(a, 0)
        self.assertAlmostEqual(a, enumerate_logprobs(4, [0.] * 4, scores, accepted)[0])

    def test_invalid_accepted_candidate_rejected(self):
        with self.assertRaises(ValueError):
            forward_logprobs(2, [0., 0.], {}, {(0, 1, "f")})

    def test_nonfinite_scores_rejected(self):
        with self.assertRaises(ValueError):
            forward_logprobs(2, [0., 0.], {(0, 1, "f"): float("nan")}, set())


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.accepted = [Span(2, 4), Span(2, 5)]
        self.roster = ["E1", "E2"]
        self.continuation = {4: {"E1": "continuation", "E2": "continuation"},
                             8: {"E1": "continuation", "E2": "continuation"},
                             9: {"E1": "continuation", "E2": "continuation"}}

    def ok(self, kind, span, opinions=None, **kwargs):
        return admissible_variant(kind=kind, variant=span, accepted=self.accepted,
                                  preferred_start=2, opinions=opinions or self.continuation,
                                  expected_experts=self.roster, **kwargs)

    def test_valid_truncation(self):
        self.assertEqual(self.ok("truncation", Span(2, 3)), (True, "eligible"))

    def test_valid_extension_to_next_formula_gap(self):
        self.assertEqual(self.ok("extension", Span(2, 7), connective_events={6, 7}, next_formula_start=8), (True, "eligible"))

    def test_no_extend_into_next_formula(self):
        self.assertEqual(self.ok("extension", Span(2, 8), connective_events={6, 7, 8}, next_formula_start=8)[1], "overlaps_next_formula")

    def test_missing_expert_even_with_one_continuation(self):
        data = {4: {"E1": "continuation"}}
        self.assertEqual(self.ok("truncation", Span(2, 3), data)[1], "unreviewed_gap")

    def test_abstention_never_counts_as_continuation(self):
        data = {4: {"E1": "continuation", "E2": "abstain"}}
        self.assertEqual(self.ok("truncation", Span(2, 3), data)[1], "abstention_or_mask")

    def test_mask_never_counts_as_continuation(self):
        data = {4: {"E1": "continuation", "E2": "masked"}}
        self.assertEqual(self.ok("truncation", Span(2, 3), data)[1], "abstention_or_mask")

    def test_reviewed_boundary_rejects_candidate(self):
        data = {4: {"E1": "continuation", "E2": "boundary"}}
        self.assertEqual(self.ok("truncation", Span(2, 3), data)[1], "reviewer_identified_boundary")

    def test_reject_non_strict_truncation(self):
        self.assertEqual(self.ok("truncation", Span(2, 5), {6: {"E1": "continuation", "E2": "continuation"}})[1], "accepted_extent")

    def test_reject_unverified_connective(self):
        self.assertEqual(self.ok("extension", Span(2, 7), connective_events={6}, next_formula_start=8)[1], "unverified_connective_material")

    def test_reject_different_start(self):
        self.assertEqual(self.ok("truncation", Span(1, 3))[1], "different_start")

    def test_window_contains_all_alternatives(self):
        self.assertEqual(shared_window(self.accepted, [Span(2, 3), Span(2, 7)], {1, 2, 6, 8, 9}), Span(2, 7))

    def test_window_requires_reviewed_outer_edge(self):
        with self.assertRaises(ValueError):
            shared_window(self.accepted, [Span(2, 7)], {2, 6})

    def test_articulation_strongest_then_nearest(self):
        self.assertEqual(choose_endpoint([3, 6, 7], {4: 3, 7: 4, 8: 4}, 5), 6)

    def test_exact_length_is_family_specific(self):
        a = exact_length_features("f", Span(2, 5), 1, 0)
        b = exact_length_features("f", Span(2, 6), 1, 0)
        c = exact_length_features("g", Span(2, 5), 1, 0)
        self.assertNotEqual(set(a), set(b))
        self.assertNotEqual(set(a), set(c))


class StatisticalTests(unittest.TestCase):
    def test_family_balance_not_micro_average(self):
        data = [("g1", "A", 0.0)] * 10 + [("g2", "B", 1.0)]
        self.assertAlmostEqual(family_balanced_mean(data, ["A", "B"]), 0.5)

    def test_defined_jackknife_interval(self):
        rows = [("g1", "A", 0.), ("g1", "B", 1.), ("g2", "A", 0.5),
                ("g2", "B", 1.5), ("g3", "A", 1.), ("g3", "B", 2.)]
        out = jackknife_t(rows, ["A", "B"], t_critical=4.302652729911275)  # df=2
        self.assertEqual(out.groups, 3)
        self.assertIsNone(out.reason)
        self.assertLess(out.lower, out.estimate)
        self.assertGreater(out.upper, out.estimate)

    def test_fixed_family_absent_after_deletion(self):
        out = jackknife_t([("g1", "A", .5), ("g2", "B", .7)], ["A", "B"], t_critical=12.7)
        self.assertIn("missing family", out.reason)

    def test_near_zero_se_no_interval(self):
        rows = [(str(i), family, 0.5) for i in range(5) for family in ("A", "B")]
        out = jackknife_t(rows, ["A", "B"], t_critical=2.776)
        self.assertEqual(out.reason, "near_zero_jackknife_se")
        self.assertIsNone(out.lower)

    def test_no_interval_without_t_quantile(self):
        rows = [(str(i), family, .1*i) for i in range(4) for family in ("A", "B")]
        self.assertEqual(jackknife_t(rows, ["A", "B"]).reason, "t_critical_not_supplied")

    def test_two_sided_requires_three_contrasts_and_same_sample(self):
        valid = {k: .05 for k in ("valid_vs_perturbed", "valid_vs_knowledge_free", "valid_vs_B_L")}
        self.assertTrue(two_sided_finding({"truncation": valid, "extension": valid},
                                          {"truncation": frozenset({"x"}), "extension": frozenset({"x"})}))
        self.assertFalse(two_sided_finding({"truncation": valid, "extension": valid},
                                           {"truncation": frozenset({"x"}), "extension": frozenset({"y"})}))
        wrong = dict(valid, valid_vs_B_L=-.01)
        self.assertFalse(two_sided_finding({"truncation": valid, "extension": wrong},
                                           {"truncation": frozenset({"x"}), "extension": frozenset({"x"})}))


if __name__ == "__main__":
    unittest.main()

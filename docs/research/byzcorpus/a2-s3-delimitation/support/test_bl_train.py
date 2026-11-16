"""Reproducible checks of frozen-base B_L training, fitting and split integrity."""
import math
import unittest
from dataclasses import replace
from bl_train import (Candidate, Window, FeatureSpec, choose_l2, fit_bl,
                      log_event_and_gradient, endpoint_log_contrast,
                      grouped_objective, make_synthetic, synthetic_report)


class BLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train, cls.dev, cls.test = make_synthetic()
        cls.spec = FeatureSpec(('A', 'B', 'C'), 6, 'exact')

    def test_group_split_is_disjoint(self):
        a, b, c = [{w.group_id for w in rows} for rows in (self.train, self.dev, self.test)]
        self.assertEqual((len(a), len(b), len(c)), (9, 3, 3))
        self.assertFalse(a & b or b & c or a & c)

    def test_no_gold_family_or_true_length_in_candidate_scoring(self):
        for w in self.train + self.dev + self.test:
            self.assertEqual({c.family for c in w.candidates}, {'A', 'B', 'C'})
            for f in ('A', 'B', 'C'):
                self.assertEqual({c.length for c in w.candidates if c.family == f}, {2, 3, 4, 5, 6})

    def test_exact_family_and_length_features(self):
        labels = self.spec.labels
        self.assertIn('length:A:3', labels)
        self.assertIn('length:B:3', labels)
        self.assertIn('length:A:4', labels)
        self.assertNotEqual(self.spec.encode(Candidate(1, 3, 'A', 0, 0, 0)),
                            self.spec.encode(Candidate(1, 3, 'B', 0, 0, 0)))
        self.assertNotEqual(self.spec.encode(Candidate(1, 3, 'A', 0, 0, 0)),
                            self.spec.encode(Candidate(1, 4, 'A', 0, 0, 0)))

    def test_knowledge_criteria_are_not_features(self):
        labels = self.spec.labels
        self.assertFalse(any(x.startswith(('R:', 'A:', 'E:')) for x in labels))
        self.assertTrue(set(labels) >= {'articulation', 'text_boundary'})

    def test_log_event_gradient_finite_difference(self):
        w = self.train[0]
        theta = [0.03 * (j % 4 - 1.5) for j in range(len(self.spec.labels))]
        y, g = log_event_and_gradient(w, self.spec, theta)
        self.assertTrue(math.isfinite(y))
        h = 1e-5
        for j in range(len(theta)):
            a, b = theta.copy(), theta.copy()
            a[j] += h
            b[j] -= h
            ya = log_event_and_gradient(w, self.spec, a)[0]
            yb = log_event_and_gradient(w, self.spec, b)[0]
            self.assertAlmostEqual(g[j], (ya - yb)/(2*h), delta=2e-8)

    def test_objective_gradient_finite_difference(self):
        windows = self.train[:3]
        theta = [0.01 for _ in self.spec.labels]
        z, g = grouped_objective(windows, self.spec, theta, 0.2)
        self.assertTrue(math.isfinite(z))
        h = 1e-5
        for j in range(len(theta)):
            a, b = theta.copy(), theta.copy()
            a[j] += h
            b[j] -= h
            za = grouped_objective(windows, self.spec, a, 0.2)[0]
            zb = grouped_objective(windows, self.spec, b, 0.2)[0]
            self.assertAlmostEqual(g[j], (za - zb)/(2*h), delta=2e-8)

    def test_training_improves_penalised_train_objective(self):
        z0 = grouped_objective(self.train, self.spec, [0.] * len(self.spec.labels), 0.1)[0]
        f = fit_bl(self.train, self.spec, 0.1, max_iter=150)
        self.assertGreater(f.train_objective, z0)
        self.assertGreater(f.iterations, 0)

    def test_holdout_selection_prohibits_shared_groups(self):
        with self.assertRaises(ValueError):
            choose_l2(self.train, self.train[:3], self.spec)

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self.spec.encode(Candidate(1, 3, 'NEW', 0., 0., 0.))

    def test_out_of_domain_length_rejected(self):
        with self.assertRaises(ValueError):
            self.spec.encode(Candidate(1, 7, 'A', 0., 0., 0.))

    def test_invalid_probability_window_rejected(self):
        with self.assertRaises(ValueError):
            Window('a','g',2,(0., 0.),(Candidate(0,1,'A',0.,0.,0.),),frozenset({(0,0,'A')}))

    def test_exact_length_beats_coarse_and_no_length_in_synthetic_controls(self):
        report = synthetic_report()
        x = report['comparison']['exact']
        c = report['comparison']['coarse']
        n = report['comparison']['no_length']
        self.assertGreater(x['test_group_mean_log_probability'], c['test_group_mean_log_probability'])
        self.assertGreater(c['test_group_mean_log_probability'], n['test_group_mean_log_probability'])
        self.assertGreater(x['min_truncation_log_contrast'], 0)
        self.assertGreater(x['min_extension_log_contrast'], 0)
        self.assertEqual(report['split_groups'], {'train':9,'dev':3,'test':3})

    def test_corrupt_variant_disallowed(self):
        model=fit_bl(self.train[:6],self.spec,0.1,max_iter=60)
        w=self.test[0]
        with self.assertRaises(ValueError):
            endpoint_log_contrast(w,model,next(iter(w.accepted)))

    def test_no_predictions_use_gold_family_as_feature(self):
        w=self.test[0]
        theta=[0.0]*len(self.spec.labels)
        # Gold is an evaluation event, while the partition includes every candidate family.
        p,g=log_event_and_gradient(w,self.spec,theta)
        self.assertLess(p,0.0)
        self.assertEqual(len(g),len(self.spec.labels))


    def test_text_and_articulation_coefficients_can_be_trained(self):
        rows = []
        for i in range(6):
            c1 = Candidate(1, 3, 'A', 0., 1., 1.)
            c2 = Candidate(1, 4, 'A', 0., -1., -1.)
            rows.append(Window(f'item-{i}', f'g-{i}', 6, (0.,)*6,
                               (c1, c2), frozenset({c1.key})))
        spec = FeatureSpec(('A',), 5, 'none', True, True)
        fit = fit_bl(rows, spec, .1, max_iter=140)
        self.assertGreater(fit.theta[spec.labels.index('articulation')], 0.1)
        self.assertGreater(fit.theta[spec.labels.index('text_boundary')], 0.1)

    def test_frozen_base_scores_unchanged_after_training(self):
        original = tuple((c.key,c.base_score) for c in self.train[0].candidates)
        _ = fit_bl(self.train[:6], self.spec, 0.1, max_iter=55)
        self.assertEqual(original, tuple((c.key,c.base_score) for c in self.train[0].candidates))

    def test_multiple_accepted_alternatives_have_finite_probabilities(self):
        w = self.train[0]
        a = next(iter(w.accepted))
        b = next(c.key for c in w.candidates if c.family == a[2] and c.key != a)
        w2 = replace(w, accepted=frozenset({a,b}))
        theta=[0.01] * len(self.spec.labels)
        one = log_event_and_gradient(w, self.spec, theta)[0]
        two = log_event_and_gradient(w2, self.spec, theta)[0]
        self.assertGreater(two, one)
        self.assertLessEqual(two, 0)


if __name__ == '__main__':
    unittest.main()

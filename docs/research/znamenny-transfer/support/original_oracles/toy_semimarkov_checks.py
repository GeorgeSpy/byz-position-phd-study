#!/usr/bin/env python3
"""Numerical oracle for the design, with synthetic data only.

Run: python3 toy_semimarkov_checks.py --output toy_check_results.json
Spans use zero-based, half-open (start, end, label) indices.
No corpus, neural model, or trained chant checkpoint is included.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from typing import Callable

Span = tuple[int, int, int]
NEG = float("-inf")


def lse(values):
    values = list(values)
    if not values:
        return NEG
    m = max(values)
    if m == NEG:
        return NEG
    return m + math.log(sum(math.exp(v - m) for v in values))


def paths(t: int, length: int, labels: int, start: int = 0):
    if start == t:
        yield ()
        return
    for end in range(start + 1, min(t, start + length) + 1):
        for f in range(labels):
            for tail in paths(t, length, labels, end):
                yield ((start, end, f),) + tail


def brute(t, length, labels, phi, psi=None, eos=None, accept=None):
    records = []
    for path in paths(t, length, labels):
        if accept is not None and not accept(path):
            continue
        score = 0.0
        prev = None
        for span in path:
            score += phi(span)
            if psi is not None:
                score += psi(prev, span)
            prev = span
        if eos is not None and prev is not None:
            score += eos(prev)
        if score != NEG:
            records.append((score, path))
    if not records:
        return NEG, NEG, (), []
    best = max(records, key=lambda x: x[0])
    return lse(s for s, _ in records), best[0], best[1], records


def zero_dp(t, length, labels, phi):
    a = [NEG] * (t + 1)
    v = [NEG] * (t + 1)
    bp = [None] * (t + 1)
    a[0] = v[0] = 0.0
    for end in range(1, t + 1):
        terms = []
        for span_len in range(1, min(length, end) + 1):
            start = end - span_len
            for f in range(labels):
                span = (start, end, f)
                potential = phi(span)
                terms.append(a[start] + potential)
                candidate = v[start] + potential
                if candidate > v[end]:
                    v[end], bp[end] = candidate, span
        a[end] = lse(terms)
    result = []
    end = t
    while end > 0 and bp[end] is not None:
        span = bp[end]
        result.append(span)
        end = span[0]
    return a[t], v[t], tuple(reversed(result))


def label_dp(t, length, labels, phi, transition, eos):
    """First order in labels: transition(start, previous_label_or_None, f)."""
    if t == 0:
        return 0.0, 0.0, ()
    a = [[NEG] * labels for _ in range(t + 1)]
    v = [[NEG] * labels for _ in range(t + 1)]
    bp = {}
    for end in range(1, t + 1):
        for f in range(labels):
            terms = []
            for span_len in range(1, min(length, end) + 1):
                start = end - span_len
                potential = phi((start, end, f))
                previous = [None] if start == 0 else range(labels)
                for g in previous:
                    av = 0.0 if g is None else a[start][g]
                    vv = 0.0 if g is None else v[start][g]
                    edge = transition(start, g, f)
                    terms.append(av + edge + potential)
                    candidate = vv + edge + potential
                    if candidate > v[end][f]:
                        v[end][f] = candidate
                        bp[(end, f)] = (start, g)
            a[end][f] = lse(terms)
    log_z = lse(a[t][f] + eos(f) for f in range(labels))
    final = max(range(labels), key=lambda f: v[t][f] + eos(f))
    best = v[t][final] + eos(final)
    if best == NEG:
        return log_z, best, ()
    result = []
    end, f = t, final
    while end:
        start, g = bp[(end, f)]
        result.append((start, end, f))
        end, f = start, g
    return log_z, best, tuple(reversed(result))


def pair_dp(t, length, labels, phi, psi, eos):
    """Full adjacent-span dependence; states retain the previous full span."""
    if t == 0:
        return 0.0, 0.0, ()
    states = defaultdict(list)
    a, v, bp = {}, {}, {}
    for end in range(1, t + 1):
        for span_len in range(1, min(length, end) + 1):
            start = end - span_len
            for f in range(labels):
                span = (start, end, f)
                previous = [None] if start == 0 else states[start]
                terms = []
                best, best_prev = NEG, None
                for prev in previous:
                    av = 0.0 if prev is None else a[prev]
                    vv = 0.0 if prev is None else v[prev]
                    edge = psi(prev, span)
                    potential = phi(span)
                    terms.append(av + edge + potential)
                    candidate = vv + edge + potential
                    if candidate > best:
                        best, best_prev = candidate, prev
                a[span], v[span], bp[span] = lse(terms), best, best_prev
                states[end].append(span)
    log_z = lse(a[s] + eos(s) for s in states[t])
    final = max(states[t], key=lambda s: v[s] + eos(s))
    best = v[final] + eos(final)
    if best == NEG:
        return log_z, best, ()
    result = []
    current = final
    while current is not None:
        result.append(current)
        current = bp[current]
    return log_z, best, tuple(reversed(result))


def backward(t, length, labels, phi):
    b = [NEG] * (t + 1)
    b[t] = 0.0
    for start in range(t - 1, -1, -1):
        b[start] = lse(
            phi((start, end, f)) + b[end]
            for end in range(start + 1, min(t, start + length) + 1)
            for f in range(labels)
        )
    return b


def evidence_update(prior, observations):
    """observations[j] is None (unobserved) or a 2-entry likelihood table.

    A likelihood table is indexed by the latent diagnostic value, not by H.
    """
    weights = {}
    for state, p in prior.items():
        weight = p
        for j, likelihood in observations.items():
            if likelihood is not None:
                weight *= likelihood[state[j]]
        weights[state] = weight
    normalizer = sum(weights.values())
    if normalizer <= 0:
        raise ValueError("Evidence has zero probability under the prior.")
    return {s: w / normalizer for s, w in weights.items()}


def semantic_mass(distribution, predicate):
    return sum(p for state, p in distribution.items() if predicate(state))


def assert_split_integrity(records, links=()):
    """Reject any dependency component that crosses splits.

    These IDs must encode relationships appropriate to the declared estimand.
    Witness-wide source holdouts require an additional source-group check.
    """
    by_id = {r["id"]: r for r in records}
    if len(by_id) != len(records):
        raise ValueError("Duplicate record ID")
    parent = {i: i for i in by_id}

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        parent[root(i)] = root(j)

    seen = {}
    for record in records:
        for key in ("work_group", "locus_group", "dependency_group"):
            value = record.get(key)
            if value is not None:
                tag = key, value
                if tag in seen:
                    union(record["id"], seen[tag])
                seen[tag] = record["id"]
    for left, right in links:
        if left not in by_id or right not in by_id:
            raise ValueError("Unknown ID in dependency edge")
        union(left, right)
    split_sets = defaultdict(set)
    for record in records:
        split_sets[root(record["id"])].add(record["split"])
    if any(len(splits) > 1 for splits in split_sets.values()):
        raise ValueError("A dependency component crosses the split")
    return True


def run_checks():
    counts = Counter()
    max_error = 0.0
    rng = random.Random(27102026)

    def close(category, actual, expected, tolerance=1e-9):
        nonlocal max_error
        if actual == expected:
            err = 0.0
        else:
            err = abs(actual - expected)
            if not math.isfinite(err) or err > tolerance:
                raise AssertionError((category, actual, expected))
        max_error = max(max_error, err)
        counts[category] += 1

    def check(category, condition):
        if not condition:
            raise AssertionError(category)
        counts[category] += 1

    for t in range(1, 6):
        for length in range(1, min(3, t) + 1):
            for labels in (1, 2, 3):
                potentials = {
                    (a, b, f): rng.uniform(-3, 3)
                    for a in range(t)
                    for b in range(a + 1, min(t, a + length) + 1)
                    for f in range(labels)
                }
                phi = potentials.__getitem__
                oracle = brute(t, length, labels, phi)
                computed = zero_dp(t, length, labels, phi)
                close("zero_order_partition", computed[0], oracle[0])
                close("zero_order_viterbi", computed[1], oracle[1])
                close("zero_order_path_score", sum(phi(s) for s in computed[2]), oracle[1])
                close("backward_partition", backward(t, length, labels, phi)[0], oracle[0])
                close("normalization", sum(math.exp(s - computed[0]) for s, _ in oracle[3]), 1.0)

    for t in range(1, 6):
        for trial in range(3):
            length, labels = min(3, t), 2
            potentials = {(a, b, f): rng.uniform(-2, 2)
                          for a in range(t)
                          for b in range(a + 1, min(t, a + length) + 1)
                          for f in range(labels)}
            phi = potentials.__getitem__
            transitions = {(start, g, f): rng.uniform(-2, 2)
                           for start in range(t)
                           for g in (None, 0, 1)
                           for f in range(labels)}
            end_scores = [rng.uniform(-1, 1) for _ in range(labels)]
            transition = lambda a, g, f: transitions[(a, g, f)]
            psi_label = lambda previous, current: transition(
                current[0], None if previous is None else previous[2], current[2])
            eos_label = lambda span: end_scores[span[2]]
            oracle = brute(t, length, labels, phi, psi_label, eos_label)
            computed = label_dp(t, length, labels, phi, transition, end_scores.__getitem__)
            close("label_transition_partition", computed[0], oracle[0])
            close("label_transition_viterbi", computed[1], oracle[1])

            def psi_full(previous, current):
                base = psi_label(previous, current)
                if previous is None:
                    return base + 0.07 * (current[1] - current[0])
                return base + 0.17 * (previous[1] - previous[0]) * (current[1] - current[0])

            oracle_pair = brute(t, length, labels, phi, psi_full, eos_label)
            computed_pair = pair_dp(t, length, labels, phi, psi_full, eos_label)
            close("full_span_partition", computed_pair[0], oracle_pair[0])
            close("full_span_viterbi", computed_pair[1], oracle_pair[1])
            recovered = sum(phi(s) + psi_full(None if k == 0 else computed_pair[2][k-1], s)
                            for k, s in enumerate(computed_pair[2])) + eos_label(computed_pair[2][-1])
            close("full_span_path_score", recovered, oracle_pair[1])
            collapsed = label_dp(t, length, labels, phi, lambda a, g, f: 0.0, lambda f: 0.0)
            close("transition_zero_reduction", collapsed[0], zero_dp(t, length, labels, phi)[0])

    phi = lambda span: 0.23 * (span[1] - span[0]) - 0.11 * span[2]
    forced = (1, 3, 1)
    masked = lambda span: phi(span) if (
        span == forced or span[1] <= forced[0] or span[0] >= forced[1]) else NEG
    partial_oracle = brute(4, 3, 2, phi, accept=lambda path: forced in path)
    close("partial_partition", zero_dp(4, 3, 2, masked)[0], partial_oracle[0])
    check("partial_likelihood_bound", partial_oracle[0] <= brute(4, 3, 2, phi)[0])
    close("impossible_path", zero_dp(3, 2, 2, lambda span: NEG)[0], NEG)
    close("large_potential_stability", zero_dp(3, 2, 2, lambda span: 1000.0)[0],
          brute(3, 2, 2, lambda span: 1000.0)[0])
    close("empty_sequence", zero_dp(0, 2, 2, phi)[0], 0.0)

    states = list(itertools.product((0, 1), repeat=3))
    uniform = {state: 1.0 / len(states) for state in states}
    branch_a = lambda state: bool(state[0])
    branch_b = lambda state: bool(state[1])
    mass_union = semantic_mass(uniform, lambda state: branch_a(state) or branch_b(state))
    close("overlap_union_once", mass_union, 0.75)
    check("naive_branch_sum_is_wrong", mass_union !=
          semantic_mass(uniform, branch_a) + semantic_mass(uniform, branch_b))
    missing = evidence_update(uniform, {0: None})
    close("unknown_is_identity", max(abs(missing[s] - uniform[s]) for s in states), 0.0)
    false_evidence = evidence_update(uniform, {0: (0.9, 0.1)})
    check("false_differs_from_unknown", semantic_mass(false_evidence, branch_a) <
          semantic_mass(missing, branch_a))
    close("evidence_normalization", sum(false_evidence.values()), 1.0)
    correlated = {(0, 0): 0.5, (1, 1): 0.5}
    independent = {state: 0.25 for state in itertools.product((0, 1), repeat=2)}
    equivalent = lambda state: state[0] == state[1]
    close("joint_semantics", semantic_mass(correlated, equivalent), 1.0)
    close("factorization_counterexample", semantic_mass(independent, equivalent), 0.5)
    try:
        evidence_update(uniform, {0: (0.0, 0.0)})
        raise AssertionError("Zero probability evidence should fail")
    except ValueError:
        counts["zero_evidence_rejected"] += 1

    close("ambiguity_bayes_top1", max(0.5, 0.5), 0.5)
    close("ambiguity_entropy_bits", -sum(p * math.log2(p) for p in (0.5, 0.5)), 1.0)
    counts_m = (94, 85, 40, 59, 66, 83, 34, 50)
    found = (54, 41, 25, 32, 38, 33, 27, 28)
    close("metallov_catalogue_count", sum(counts_m), 511)
    close("metallov_recovered_count", sum(found), 278)
    close("metallov_coverage_arithmetic", 8600 / 29217, 0.2943491802717596)

    records = [
        {"id": "a", "locus_group": "l1", "split": "train"},
        {"id": "b", "locus_group": "l1", "split": "train"},
        {"id": "c", "locus_group": "l2", "split": "test"},
    ]
    check("valid_grouped_split", assert_split_integrity(records))
    bad = [dict(r) for r in records]
    bad[1]["split"] = "test"
    for data, links, category in (
        (bad, (), "same_locus_leak_rejected"),
        (records, (("b", "c"),), "transitive_dependency_leak_rejected"),
    ):
        try:
            assert_split_integrity(data, links)
            raise AssertionError("Leakage should fail")
        except ValueError:
            counts[category] += 1

    return {
        "status": "passed",
        "data": "synthetic_oracle_and_published_table_arithmetic_only",
        "random_seed": 27102026,
        "total_checks": sum(counts.values()),
        "checks_by_category": dict(sorted(counts.items())),
        "max_absolute_numeric_error": max_error,
        "claims": {
            "zero_order_dp": "checked_against_exhaustive_enumeration",
            "first_order_label_dp": "checked_against_exhaustive_enumeration",
            "full_adjacent_span_dp": "checked_against_exhaustive_enumeration",
            "chant_model_training": "not_run",
            "corpus_validation": "requires_real_data",
            "architecture_novelty": "not_established_by_numerical_checks",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Write the complete JSON check report")
    args = parser.parse_args()
    result = run_checks()
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as stream:
            stream.write(payload + "\n")
    print(payload)

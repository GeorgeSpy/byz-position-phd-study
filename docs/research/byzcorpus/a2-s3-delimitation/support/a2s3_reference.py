"""Small exact oracles for A2-S3 design checks.

This module tests mathematical and annotation invariants on synthetic cases.
It is not an implementation of trained A2 models or the historical S3 runs.
Uses only Python's standard library, except for optional scipy in intervals.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, sqrt, ulp
from typing import Mapping, Sequence


@dataclass(frozen=True, order=True)
class Span:
    start: int
    end: int  # Inclusive atomic event indices.

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid inclusive event span")

    @property
    def length(self) -> int:
        return self.end - self.start + 1


def logadd(a: float, b: float) -> float:
    """Stable log(exp(a)+exp(b)), including -inf."""
    if a == float("-inf"):
        return b
    if b == float("-inf"):
        return a
    if b > a:
        a, b = b, a
    from math import log1p
    return a + log1p(exp(b - a))


def _check(n: int, skip: Sequence[float], scores: Mapping[tuple[int, int, str], float]) -> None:
    if n < 1 or len(skip) != n or not all(isfinite(x) for x in skip):
        raise ValueError("finite skip scores required for each event")
    for (start, end, family), weight in scores.items():
        if not (0 <= start <= end < n and family and isfinite(weight)):
            raise ValueError("invalid segment score")


def forward_logprobs(
    n: int,
    skip: Sequence[float],
    scores: Mapping[tuple[int, int, str], float],
    accepted: set[tuple[int, int, str]],
) -> tuple[float, float]:
    """Log P(any accepted labeled span occurs), log partition.

    The path is a left-to-right tiling of non-overlapping labeled segments
    and single-event skips. The two-state DP records if a labeled accepted
    span was emitted. Overlapping alternatives are counted once per path.
    Scores are unnormalised log potentials; window boundary constraints
    must already be encoded in the supplied scores.
    """
    _check(n, skip, scores)
    if not accepted.issubset(scores):
        raise ValueError("accepted labeled spans must be candidates")
    by_start: dict[int, list[tuple[int, str, float]]] = {}
    for (a, b, f), score in scores.items():
        by_start.setdefault(a, []).append((b, f, score))
    dp = [[float("-inf"), float("-inf")] for _ in range(n + 1)]
    dp[0][0] = 0.0
    for i in range(n):
        for state in (0, 1):
            current = dp[i][state]
            if current == float("-inf"):
                continue
            dp[i + 1][state] = logadd(dp[i + 1][state], current + skip[i])
            for end, family, score in by_start.get(i, []):
                next_state = int(bool(state) or ((i, end, family) in accepted))
                dp[end + 1][next_state] = logadd(
                    dp[end + 1][next_state], current + score
                )
    partition = logadd(*dp[n])
    return dp[n][1] - partition, partition


def enumerate_logprobs(
    n: int,
    skip: Sequence[float],
    scores: Mapping[tuple[int, int, str], float],
    accepted: set[tuple[int, int, str]],
) -> tuple[float, float]:
    """Independent exhaustive-path oracle, suitable only for small cases."""
    _check(n, skip, scores)
    if not accepted.issubset(scores):
        raise ValueError("accepted labeled spans must be candidates")
    all_paths: list[float] = []
    marked_paths: list[float] = []

    def walk(i: int, current: float, hit: bool) -> None:
        if i == n:
            all_paths.append(current)
            if hit:
                marked_paths.append(current)
            return
        walk(i + 1, current + skip[i], hit)
        for (a, b, f), score in scores.items():
            if a == i:
                walk(b + 1, current + score, hit or ((a, b, f) in accepted))

    walk(0, 0.0, False)

    def reduce_log(xs: Sequence[float]) -> float:
        result = float("-inf")
        for x in xs:
            result = logadd(result, x)
        return result

    den = reduce_log(all_paths)
    num = reduce_log(marked_paths)
    return num - den, den


def shared_window(
    accepted: Sequence[Span], variants: Sequence[Span], agreed_boundary_gaps: set[int]
) -> Span:
    """Smallest eligible reviewed common event window, if it exists."""
    if not accepted or not variants:
        raise ValueError("accepted extents and variants required")
    all_spans = list(accepted) + list(variants)
    minimum_start = min(s.start for s in all_spans)
    farthest_end = max(s.end for s in all_spans)
    left = [g for g in agreed_boundary_gaps if g <= minimum_start]
    right = [g for g in agreed_boundary_gaps if g > farthest_end]
    if not left or not right:
        raise ValueError("missing agreed enclosing boundary")
    return Span(max(left), min(right) - 1)


def admissible_variant(
    *,
    kind: str,
    variant: Span,
    accepted: Sequence[Span],
    preferred_start: int,
    opinions: Mapping[int, Mapping[str, str]],
    expected_experts: Sequence[str],
    connective_events: set[int] | None = None,
    next_formula_start: int | None = None,
) -> tuple[bool, str]:
    """Conservative endpoint eligibility audit with explicit expert coverage.

    Opinions are keyed by gap (right boundary = end+1), then expert ID.
    Values: 'continuation', 'boundary', 'abstain', or 'masked'.
    The expert roster is fixed before inspecting candidate opinions.
    """
    if kind not in ("truncation", "extension"):
        raise ValueError("unrecognised variant kind")
    if not accepted or not expected_experts or len(set(expected_experts)) != len(expected_experts):
        raise ValueError("accepted extents and a unique reviewer roster required")
    if variant.start != preferred_start:
        return False, "different_start"
    matching = [s for s in accepted if s.start == preferred_start]
    if not matching:
        return False, "no_accepted_extent_with_preferred_start"
    gap = variant.end + 1
    judgements = opinions.get(gap, {})
    if any(x not in judgements for x in expected_experts):
        return False, "unreviewed_gap"
    if any(judgements[x] in ("abstain", "masked") for x in expected_experts):
        return False, "abstention_or_mask"
    if any(judgements[x] not in ("boundary", "continuation") for x in expected_experts):
        return False, "invalid_judgement"
    if any(judgements[x] != "continuation" for x in expected_experts):
        return False, "reviewer_identified_boundary"
    if variant in accepted:
        return False, "accepted_extent"
    if kind == "truncation":
        if variant.end >= min(s.end for s in matching):
            return False, "not_strict_truncation"
        return True, "eligible"
    farthest = max(s.end for s in accepted)
    if variant.end <= farthest:
        return False, "not_beyond_all_accepted_extents"
    if next_formula_start is not None and variant.end >= next_formula_start:
        return False, "overlaps_next_formula"
    connective = connective_events or set()
    if not set(range(farthest + 1, variant.end + 1)).issubset(connective):
        return False, "unverified_connective_material"
    return True, "eligible"


def choose_endpoint(
    candidate_endpoints: Sequence[int],
    articulation_by_end_gap: Mapping[int, int],
    accepted_end: int,
) -> int:
    """Prespecified articulation-first choice; nearest to accepted end on ties."""
    if not candidate_endpoints or any((end + 1) not in articulation_by_end_gap for end in candidate_endpoints):
        raise ValueError("complete articulation information required")
    return max(candidate_endpoints, key=lambda b: (articulation_by_end_gap[b + 1], -abs(b - accepted_end), -b))


def exact_length_features(family: str, span: Span, articulation: float, text_boundary: float) -> dict[str, float]:
    """S3 B_L audit features: distinguish exact lengths, even in one coarse bin."""
    if not family or not all(isfinite(x) for x in (articulation, text_boundary)):
        raise ValueError("invalid exact-length features")
    return {
        f"family_length::{family}::{span.length}": 1.0,
        "articulation": float(articulation),
        "text_boundary": float(text_boundary),
    }


def family_balanced_mean(rows: Sequence[tuple[str, str, float]], families: Sequence[str]) -> float:
    """Each fixed family gets equal weight, regardless of occurrence frequency."""
    family_set = set(families)
    if not families or len(family_set) != len(families):
        raise ValueError("fixed unique family catalogue required")
    result = []
    for f in families:
        values = [v for _, family, v in rows if family == f]
        if not values or not all(isfinite(v) for v in values):
            raise ValueError("missing family or nonfinite contrast")
        result.append(sum(values) / len(values))
    return sum(result) / len(result)


@dataclass(frozen=True)
class JackknifeResult:
    estimate: float | None
    se: float | None
    lower: float | None
    upper: float | None
    groups: int
    reason: str | None


def jackknife_t(
    rows: Sequence[tuple[str, str, float]],
    families: Sequence[str],
    *,
    t_critical: float | None = None,
) -> JackknifeResult:
    """Group-deletion jackknife; t-quantile is supplied explicitly.

    t_critical must be the two-sided 0.975 Student t quantile at G-1 df.
    A caller can use scipy.stats.t.ppf(0.975, G-1). This routine itself
    has no optional dependency and never silently substitutes normal CI.
    """
    groups = sorted({g for g, _, _ in rows})
    G = len(groups)
    if G < 2:
        return JackknifeResult(None, None, None, None, G, "fewer_than_two_groups")
    try:
        theta = family_balanced_mean(rows, families)
        leave_one = [family_balanced_mean([r for r in rows if r[0] != g], families) for g in groups]
    except ValueError as exc:
        return JackknifeResult(None, None, None, None, G, str(exc))
    bar = sum(leave_one) / G
    se = sqrt((G - 1) / G * sum((x - bar) ** 2 for x in leave_one))
    eps = 32 * ulp(1.0) * sqrt(G) * max(1.0, abs(theta), *(abs(x) for x in leave_one))
    if se <= eps:
        return JackknifeResult(theta, se, None, None, G, "near_zero_jackknife_se")
    if t_critical is None:
        return JackknifeResult(theta, se, None, None, G, "t_critical_not_supplied")
    if not isfinite(t_critical) or t_critical <= 0:
        raise ValueError("invalid t critical value")
    return JackknifeResult(theta, se, theta - t_critical * se, theta + t_critical * se, G, None)


def two_sided_finding(
    contrasts: Mapping[str, Mapping[str, float]],
    sample_ids: Mapping[str, frozenset[str]],
) -> bool:
    """Reportable directional decision, without inferential claims.

    Requires identical occurrence IDs and three positive comparisons on
    each side: valid-vs-perturbed, valid-vs-knowledge-free, valid-vs-B_L.
    """
    keys = ("valid_vs_perturbed", "valid_vs_knowledge_free", "valid_vs_B_L")
    if set(contrasts) != {"truncation", "extension"} or set(sample_ids) != set(contrasts):
        return False
    if not sample_ids["truncation"] or sample_ids["truncation"] != sample_ids["extension"]:
        return False
    return all(all(k in contrasts[v] and isfinite(contrasts[v][k]) and contrasts[v][k] > 0 for k in keys) for v in contrasts)

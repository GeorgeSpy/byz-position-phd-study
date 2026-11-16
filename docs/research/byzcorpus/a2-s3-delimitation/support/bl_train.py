"""B_L: L2-regularized family-specific exact-length semi-CRF reference head.

Fixed base segment potentials are supplied as inputs. This module fits only
length, articulation, and text-boundary coefficients on grouped development
windows; no R/A/E knowledge features or gold family oracle enter scoring.
Pure Python 3.10+; synthetic reference implementation for A2-S3.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log1p, sqrt
from typing import Sequence


@dataclass(frozen=True)
class Candidate:
    start: int
    end: int
    family: str
    base_score: float
    articulation: float
    text_boundary: float

    @property
    def key(self) -> tuple[int, int, str]:
        return self.start, self.end, self.family

    @property
    def length(self) -> int:
        return self.end - self.start + 1


@dataclass(frozen=True)
class Window:
    occurrence_id: str
    group_id: str
    n_events: int
    skip_scores: tuple[float, ...]
    candidates: tuple[Candidate, ...]
    accepted: frozenset[tuple[int, int, str]]

    def __post_init__(self) -> None:
        if not self.occurrence_id or not self.group_id or self.n_events < 1:
            raise ValueError('missing ID or invalid event count')
        if len(self.skip_scores) != self.n_events or not all(map(isfinite, self.skip_scores)):
            raise ValueError('all skip scores must be finite')
        keys = [c.key for c in self.candidates]
        if len(keys) != len(set(keys)):
            raise ValueError('duplicate labeled span')
        for c in self.candidates:
            if not (0 <= c.start <= c.end < self.n_events and c.family):
                raise ValueError('invalid candidate')
            if not all(isfinite(x) for x in (c.base_score, c.articulation, c.text_boundary)):
                raise ValueError('nonfinite candidate feature')
        if not self.accepted or not self.accepted.issubset(set(keys)):
            raise ValueError('accepted spans must be candidate spans')


@dataclass(frozen=True)
class FeatureSpec:
    families: tuple[str, ...]
    max_length: int
    length_mode: str = 'exact'  # exact | coarse | none
    add_articulation: bool = True
    add_text: bool = True

    def __post_init__(self) -> None:
        if not self.families or len(self.families) != len(set(self.families)):
            raise ValueError('fixed, unique family catalogue required')
        if self.max_length < 1 or self.length_mode not in ('exact', 'coarse', 'none'):
            raise ValueError('unknown feature specification')

    @property
    def labels(self) -> tuple[str, ...]:
        tags = []
        if self.length_mode != 'none':
            for fam in self.families:
                for length in range(1, self.max_length + 1):
                    tag = length if self.length_mode == 'exact' else length // 3
                    key = f'length:{fam}:{tag}'
                    if key not in tags:
                        tags.append(key)
        if self.add_articulation:
            tags.append('articulation')
        if self.add_text:
            tags.append('text_boundary')
        return tuple(tags)

    def encode(self, c: Candidate) -> dict[int, float]:
        if c.family not in self.families or c.length > self.max_length:
            raise ValueError('candidate family or exact length out of declared domain')
        keys = self.labels
        feats = {}
        if self.length_mode != 'none':
            tag = c.length if self.length_mode == 'exact' else c.length // 3
            feats[keys.index(f'length:{c.family}:{tag}')] = 1.0
        if self.add_articulation:
            feats[keys.index('articulation')] = c.articulation
        if self.add_text:
            feats[keys.index('text_boundary')] = c.text_boundary
        return feats


@dataclass(frozen=True)
class Fit:
    theta: tuple[float, ...]
    spec: FeatureSpec
    l2: float
    iterations: int
    train_objective: float


def _join(left: tuple[float, list[float]] | None,
          right: tuple[float, list[float]]) -> tuple[float, list[float]]:
    if left is None:
        return right
    a, ua = left
    b, ub = right
    if a < b:
        a, b = b, a
        ua, ub = ub, ua
    factor = exp(b - a)
    prob_b = factor / (1.0 + factor)
    return a + log1p(factor), [u + prob_b * (v - u) for u, v in zip(ua, ub)]


def log_event_and_gradient(window: Window, spec: FeatureSpec,
                           theta: Sequence[float],
                           accepted: frozenset[tuple[int, int, str]] | None = None
                           ) -> tuple[float, tuple[float, ...]]:
    """Exact log P(at least one accepted span) and its score derivative.

    Two-state forward calculation propagates a log path mass and the
    conditional expectation of each feature count, which differentiates
    the log partition exactly. Paths combine non-overlapping segments and
    single-event skips. Gold labels are used solely to specify the training
    event, never to determine test candidate scores.
    """
    if len(theta) != len(spec.labels) or not all(map(isfinite, theta)):
        raise ValueError('wrong parameter dimension or nonfinite coefficient')
    accepted = window.accepted if accepted is None else accepted
    if not accepted or not accepted.issubset({c.key for c in window.candidates}):
        raise ValueError('nonempty accepted candidate set required')
    k = len(theta)
    starts: list[list[Candidate]] = [[] for _ in range(window.n_events)]
    for c in window.candidates:
        starts[c.start].append(c)
    dp: list[list[tuple[float, list[float]] | None]] = [[None, None] for _ in range(window.n_events + 1)]
    dp[0][0] = (0.0, [0.0] * k)
    for i in range(window.n_events):
        for hit in (0, 1):
            current = dp[i][hit]
            if current is None:
                continue
            mass, count = current
            dp[i + 1][hit] = _join(dp[i + 1][hit], (mass + window.skip_scores[i], count))
            for c in starts[i]:
                feats = spec.encode(c)
                score = c.base_score + sum(theta[p] * x for p, x in feats.items())
                new_count = count.copy()
                for p, x in feats.items():
                    new_count[p] += x
                next_hit = int(bool(hit) or c.key in accepted)
                dp[c.end + 1][next_hit] = _join(
                    dp[c.end + 1][next_hit], (mass + score, new_count))
    hit = dp[-1][1]
    if hit is None:
        raise ValueError('accepted event has zero path mass')
    all_states = dp[-1][0]
    total = hit if all_states is None else _join(all_states, hit)
    return hit[0] - total[0], tuple(a - b for a, b in zip(hit[1], total[1]))


def grouped_objective(windows: Sequence[Window], spec: FeatureSpec,
                      theta: Sequence[float], l2: float
                      ) -> tuple[float, tuple[float, ...]]:
    """Maximise mean log event probability, with each independent group equal."""
    if not windows or l2 < 0 or not isfinite(l2):
        raise ValueError('nonempty windows and finite L2 >= 0 required')
    groups: dict[str, list[Window]] = {}
    for w in windows:
        groups.setdefault(w.group_id, []).append(w)
    k = len(theta)
    objective = 0.0
    gradient = [0.0] * k
    for items in groups.values():
        weight = 1.0 / (len(groups) * len(items))
        for item in items:
            value, grad = log_event_and_gradient(item, spec, theta)
            objective += weight * value
            for j, v in enumerate(grad):
                gradient[j] += weight * v
    objective -= 0.5 * l2 * sum(v * v for v in theta)
    return objective, tuple(g - l2 * t for g, t in zip(gradient, theta))


def fit_bl(windows: Sequence[Window], spec: FeatureSpec, l2: float,
           max_iter: int = 180, tolerance: float = 1e-7) -> Fit:
    """Deterministic full-batch ascent with monotone backtracking."""
    if max_iter <= 0 or tolerance <= 0:
        raise ValueError('invalid optimisation settings')
    theta = [0.0] * len(spec.labels)
    objective, grad = grouped_objective(windows, spec, theta, l2)
    steps = 0
    for _ in range(max_iter):
        norm_sq = sum(g * g for g in grad)
        if norm_sq <= tolerance * tolerance:
            break
        step = 8.0
        accepted = False
        for _ in range(40):
            candidate = [v + step * g for v, g in zip(theta, grad)]
            new_objective, new_grad = grouped_objective(windows, spec, candidate, l2)
            if new_objective >= objective + 1e-5 * step * norm_sq:
                theta, objective, grad = candidate, new_objective, new_grad
                accepted = True
                steps += 1
                break
            step *= 0.5
        if not accepted:
            break
    return Fit(tuple(theta), spec, l2, steps, objective)


def mean_group_log_probability(windows: Sequence[Window], model: Fit) -> float:
    return grouped_objective(windows, model.spec, model.theta, 0.0)[0]


def choose_l2(train: Sequence[Window], dev: Sequence[Window], spec: FeatureSpec,
              grid: Sequence[float] = (0.01, 0.1, 1.0)) -> Fit:
    """Select regularisation on held-out development GROUPS only."""
    train_groups = {x.group_id for x in train}
    dev_groups = {x.group_id for x in dev}
    if not dev or not train or train_groups.intersection(dev_groups):
        raise ValueError('group-overlapping or empty training/development split')
    if not grid or len(grid) != len(set(grid)) or any(x <= 0 for x in grid):
        raise ValueError('positive, unique L2 grid required')
    candidates = [fit_bl(train, spec, x) for x in grid]
    # On ties prefer the STRONGER regularisation; the evaluation set is untouched.
    return max(candidates, key=lambda model: (mean_group_log_probability(dev, model), model.l2))


def endpoint_log_contrast(window: Window, model: Fit,
                          variant: tuple[int, int, str]) -> float:
    """D_i = log P(accepted union) - log P(selected labeled variant)."""
    if variant in window.accepted:
        raise ValueError('variant must differ from all accepted extents')
    log_gold, _ = log_event_and_gradient(window, model.spec, model.theta)
    log_var, _ = log_event_and_gradient(window, model.spec, model.theta, frozenset({variant}))
    return log_gold - log_var


def make_synthetic(seed: int = 20261116) -> tuple[list[Window], list[Window], list[Window]]:
    """Deterministic, explicitly synthetic 3-family/15-group endpoint experiment.

    One occurrence per family per independent group. All scored candidates
    include all three families, so true family cannot enter the scoring head.
    Length target is per family (3,4,5); endpoint articulation/text are shared.
    """
    from random import Random
    rng = Random(seed)
    preferred = {'A': 3, 'B': 4, 'C': 5}
    all_windows = []
    for g in range(15):
        group = f'work-{g:02}'
        for family, gold_length in preferred.items():
            n = 8
            candidates = []
            for candidate_family in preferred:
                for length in range(2, 7):
                    start = 1
                    end = start + length - 1
                    # Frozen base scores know candidate identity, not the gold choice.
                    baseline = 0.035 * (rng.random() - 0.5)
                    candidates.append(Candidate(start, end, candidate_family,
                                                baseline, 0.0, 0.0))
            target = (1, gold_length, family)
            all_windows.append(Window(f'{group}-{family}', group, n,
                                      tuple(0.0 for _ in range(n)),
                                      tuple(candidates), frozenset({target})))
    return all_windows[:27], all_windows[27:36], all_windows[36:]


def synthetic_report() -> dict:
    """Executable control comparison; no musicological effectiveness claim."""
    train, dev, test = make_synthetic()
    specs = {
        'exact': FeatureSpec(('A', 'B', 'C'), 6, 'exact'),
        'coarse': FeatureSpec(('A', 'B', 'C'), 6, 'coarse'),
        'no_length': FeatureSpec(('A', 'B', 'C'), 6, 'none'),
    }
    out = {'split_groups': {s: len({x.group_id for x in w}) for s, w in
                            (('train', train), ('dev', dev), ('test', test))},
           'comparison': {}}
    for key, spec in specs.items():
        fit = choose_l2(train, dev, spec)
        deltas = {'truncation': [], 'extension': []}
        for window in test:
            start, end, family = next(iter(window.accepted))
            deltas['truncation'].append(endpoint_log_contrast(window, fit,
                                                              (start, end - 1, family)))
            deltas['extension'].append(endpoint_log_contrast(window, fit,
                                                             (start, end + 1, family)))
        out['comparison'][key] = {
            'selected_l2': fit.l2,
            'iterations': fit.iterations,
            'test_group_mean_log_probability': mean_group_log_probability(test, fit),
            'mean_truncation_log_contrast': sum(deltas['truncation']) / len(test),
            'mean_extension_log_contrast': sum(deltas['extension']) / len(test),
            'min_truncation_log_contrast': min(deltas['truncation']),
            'min_extension_log_contrast': min(deltas['extension']),
        }
    return out


if __name__ == '__main__':
    import json
    print(json.dumps(synthetic_report(), ensure_ascii=False, indent=2, sort_keys=True))

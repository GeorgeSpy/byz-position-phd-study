"""Musical-family knowledge operators, perturbations and evaluation utilities.

All inputs are symbolic and supplied by the caller.  The module contains no corpus
records, trained parameters, or family rules from third-party annotations.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.optimize import linprog
from scipy.stats import t as student_t


@dataclass(frozen=True)
class Scores:
    q: np.ndarray           # (occurrences, families, 3): R, A, E
    penalty: np.ndarray     # (occurrences, families): 1 for observed violation
    truth: np.ndarray       # (occurrences, families): 1, 0, -1 (unknown)


def _and(values: list[int]) -> int:
    return 0 if 0 in values else -1 if -1 in values else 1


def _or(values: list[int]) -> int:
    return 1 if 1 in values else -1 if -1 in values else 0


def validate(spec: dict, concepts: list[str]) -> None:
    known = set(concepts)
    if len(known) != len(concepts):
        raise ValueError("Concept identifiers must be unique")
    if not spec:
        raise ValueError("At least one family is required")
    for family, card in spec.items():
        if set(card) != {"R", "A", "E"}:
            raise ValueError(f"{family}: expected R, A, E")
        if not all(isinstance(g, list) and g for g in card["A"]):
            raise ValueError(f"{family}: each alternative group must be nonempty")
        used = card["R"] + [x for group in card["A"] for x in group] + card["E"]
        if any(x not in known for x in used):
            raise ValueError(f"{family}: unknown concept")


def evaluate(values: np.ndarray, observed: np.ndarray, concepts: list[str], spec: dict) -> Scores:
    """Evaluate Q and strong-Kleene R/AND(A groups)/NOT(E) on binary cues.

    Unknown literals contribute zero to Q; an unknown expression is not penalized.
    """
    values, observed = np.asarray(values), np.asarray(observed)
    if values.ndim != 2 or values.shape != observed.shape or values.shape[1] != len(concepts):
        raise ValueError("Values and observation masks must have shape (n, concepts)")
    if not np.isin(observed, [0, 1]).all() or not np.isin(values[observed == 1], [0, 1]).all():
        raise ValueError("Observed cues must be binary")
    validate(spec, concepts)
    idx = {name: j for j, name in enumerate(concepts)}
    n = values.shape[0]
    families = list(spec)
    q = np.zeros((n, len(families), 3), dtype=float)
    truth = np.ones((n, len(families)), dtype=np.int8)
    for fi, family in enumerate(families):
        card = spec[family]
        r = [idx[x] for x in card["R"]]
        a = [[idx[x] for x in g] for g in card["A"]]
        e = [idx[x] for x in card["E"]]
        if r:
            q[:, fi, 0] = np.where(observed[:, r], 2 * values[:, r] - 1, 0).mean(axis=1)
        if a:
            q[:, fi, 1] = np.column_stack([
                np.where(observed[:, group], 2 * values[:, group] - 1, 0).mean(axis=1)
                for group in a
            ]).mean(axis=1)
        if e:
            q[:, fi, 2] = np.where(observed[:, e], 1 - 2 * values[:, e], 0).mean(axis=1)
        for i in range(n):
            def literal(j: int) -> int:
                return int(values[i, j]) if observed[i, j] else -1
            terms = ([literal(j) for j in r]
                     + [_or([literal(j) for j in group]) for group in a]
                     + [(-1 if (v := literal(j)) == -1 else 1 - v) for j in e])
            truth[i, fi] = _and(terms)
    return Scores(q=q, penalty=(truth == 0).astype(float), truth=truth)


def logits(base: np.ndarray, scores: Scores, weights: np.ndarray, lam: float = 0.0) -> np.ndarray:
    """Add the knowledge head to the target-family columns of base scores.

    Model-specific class mappings, temperature fitting and training are external.
    """
    base = np.asarray(base, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if base.shape != scores.penalty.shape or weights.shape != (3,):
        raise ValueError("Expected base (N,F) and weights (3,)")
    if np.any(weights < .1 - 1e-10) or np.any(weights > .8 + 1e-10) or not np.isclose(sum(weights), 1):
        raise ValueError("Weights must belong to W: sum=1, each in [0.1,0.8]")
    if not 0 <= lam <= 2:
        raise ValueError("Lambda must lie in [0,2]")
    return base + np.einsum("nfc,c->nf", scores.q, weights) - lam * scores.penalty


def certify_lp(valid: Scores, changed: Scores, structured: bool, tolerance: float = 1e-8) -> dict:
    """Minimax separation of score families on a fixed, unlabeled state set.

    The recorded lower bound incorporates dual-stationarity residuals. For
    certification the state set must cover the intended admissible domain.
    """
    if valid.q.shape != changed.q.shape or valid.penalty.shape != changed.penalty.shape:
        raise ValueError("Valid and perturbed score matrices must have matching shapes")
    qv, qp = valid.q.reshape(-1, 3), changed.q.reshape(-1, 3)
    vv, vp = valid.penalty.reshape(-1, 1), changed.penalty.reshape(-1, 1)
    n = len(qv)
    if n == 0 or not np.isfinite(qv).all() or not np.isfinite(qp).all():
        raise ValueError("Finite nonempty state set required")
    if structured:
        a = np.hstack([qv, -qp, -vv, vp])
        bounds = [(0.1, 0.8)] * 6 + [(0., 2.)] * 2
    else:
        a = np.hstack([qv, -qp])
        bounds = [(0.1, 0.8)] * 6
    max_coeff = np.array([b[1] for b in bounds], dtype=float)
    cap = float(np.max(np.abs(a) @ max_coeff) + 1e-6)
    bounds.append((0.0, cap))
    a_ub = np.vstack([np.c_[a, -np.ones(n)], np.c_[-a, -np.ones(n)]])
    b_ub = np.zeros(2 * n)
    a_eq = np.zeros((2, len(bounds)))
    a_eq[0, :3] = 1
    a_eq[1, 3:6] = 1
    b_eq = np.ones(2)
    c = np.zeros(len(bounds))
    c[-1] = 1
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq,
                  bounds=bounds, method="highs")
    if not res.success:
        return {"certified": False, "reason": str(res.message)}
    x = res.x
    lb, ub = np.array(bounds).T
    primal = max(float(np.max(np.maximum(a_ub @ x - b_ub, 0))),
                 float(np.max(abs(a_eq @ x - b_eq))),
                 float(np.max(np.maximum(lb - x, 0))),
                 float(np.max(np.maximum(x - ub, 0))))
    y_ub = np.minimum(np.asarray(res.ineqlin.marginals), 0)
    y_eq = np.asarray(res.eqlin.marginals)
    s_lo = np.maximum(np.asarray(res.lower.marginals), 0)
    s_hi = np.minimum(np.asarray(res.upper.marginals), 0)
    stationarity = c - a_ub.T @ y_ub - a_eq.T @ y_eq - s_lo - s_hi
    dual = float(b_ub @ y_ub + b_eq @ y_eq + lb @ s_lo + ub @ s_hi)
    gap = abs(float(res.fun) - dual)
    resid = float(np.max(abs(stationarity)))
    conservative = float(dual - abs(stationarity) @ ub)
    certified = bool(primal <= tolerance and resid <= tolerance and gap <= tolerance and conservative > 1e-6)
    return {"certified": certified, "distance": float(res.fun),
            "conservative_lower_bound": conservative, "primal_residual": primal,
            "dual_residual": resid, "duality_gap": gap, "n_state_rows": int(n)}


def canonical(card: dict) -> tuple:
    return (tuple(sorted(card["R"])),
            tuple(sorted(tuple(sorted(group)) for group in card["A"])),
            tuple(sorted(card["E"])))


def propose_perturbations(spec: dict, concepts: list[str], cue_classes: dict[str, str],
                          values: np.ndarray, observed: np.ndarray, *, count: int = 10,
                          max_proposals: int = 100000, seed: int = 17, tolerance: float = .1) -> tuple[list[dict], dict]:
    """Constrained globally injective concept mappings from unlabeled development cues.

    Every accepted proposal changes each family, has satisfying and violated
    observed witnesses, differs functionally, and passes both LP certificates.
    Expert review of semantic non-synonymy remains a separate requirement.
    """
    validate(spec, concepts)
    if set(cue_classes) != set(concepts):
        raise ValueError("Every concept requires a cue class")
    values, observed = np.asarray(values), np.asarray(observed)
    if values.shape != observed.shape or values.ndim != 2 or values.shape[1] != len(concepts):
        raise ValueError("Cue matrix shapes do not match concepts")
    rng = np.random.default_rng(seed)
    pi = {name: float(np.mean(values[observed[:, j] == 1, j])) if np.any(observed[:, j] == 1) else 0.
          for j, name in enumerate(concepts)}
    mu = {name: float(np.mean(observed[:, j] == 0)) for j, name in enumerate(concepts)}
    used = sorted({name for c in spec.values() for name in c["R"] + c["E"] + sum(c["A"], [])})
    eligible = {name: [cand for cand in concepts if cue_classes[cand] == cue_classes[name]
                       and abs(pi[name] - pi[cand]) <= tolerance and abs(mu[name] - mu[cand]) <= tolerance]
                for name in used}
    immobile = [fam for fam, card in spec.items() if not any(len(eligible[x]) > 1
                       for x in card["R"] + card["E"] + sum(card["A"], []))]
    if immobile:
        return [], {"termination": "immobile_family", "families": immobile, "proposals": 0}
    families = list(spec)
    original = evaluate(values, observed, concepts, spec)
    first = tuple(canonical(spec[f]) for f in families)
    seen_cards = {first}
    seen_functions = {np.concatenate([original.q.reshape(-1), original.penalty.reshape(-1)]).tobytes()}
    accepted, rejected = [], Counter()
    for k in range(max_proposals):
        if len(accepted) >= count:
            break
        mapping, taken = {}, set()
        for name in sorted(used, key=lambda x: len(eligible[x])):
            opts = [x for x in eligible[name] if x not in taken]
            if not opts:
                break
            choice = opts[int(rng.integers(len(opts)))]
            mapping[name] = choice
            taken.add(choice)
        if len(mapping) != len(used):
            rejected["bijection"] += 1
            continue
        changed = {f: {role: [[mapping[x] for x in g] for g in card[role]] if role == "A"
                        else [mapping[x] for x in card[role]] for role in ("R", "A", "E")}
                   for f, card in spec.items()}
        if any(canonical(changed[f]) == canonical(spec[f]) for f in families):
            rejected["family_unchanged"] += 1
            continue
        cards = tuple(canonical(changed[f]) for f in families)
        if cards in seen_cards:
            rejected["duplicate_card"] += 1
            continue
        result = evaluate(values, observed, concepts, changed)
        if np.any(~np.any(result.truth == 1, axis=0)) or np.any(~np.any(result.truth == 0, axis=0)):
            rejected["witness"] += 1
            continue
        signature = np.concatenate([result.q.reshape(-1), result.penalty.reshape(-1)]).tobytes()
        if signature in seen_functions:
            rejected["duplicate_function"] += 1
            continue
        flat = certify_lp(original, result, structured=False)
        structured = certify_lp(original, result, structured=True)
        if not flat["certified"] or not structured["certified"]:
            rejected["lp"] += 1
            continue
        seen_cards.add(cards)
        seen_functions.add(signature)
        accepted.append({"id": f"P{len(accepted)+1:02d}", "spec": changed,
                         "mapping": mapping, "d_F": flat, "d_D": structured})
    return accepted, {"termination": "target_reached" if len(accepted) == count else "proposal_limit",
                      "accepted": len(accepted), "proposals": k+1 if max_proposals else 0,
                      "rejected": dict(rejected)}


def ap_with_ties(y: np.ndarray, scores: np.ndarray) -> float:
    """Uninterpolated binary AP; insert all tied scores simultaneously."""
    y, scores = np.asarray(y, dtype=int), np.asarray(scores, dtype=float)
    if y.ndim != 1 or y.shape != scores.shape or not np.isfinite(scores).all() or not np.isin(y, [0, 1]).all():
        raise ValueError("Expected finite binary labels and scores of equal length")
    positive = int(y.sum())
    if positive == 0:
        raise ValueError("AP undefined without positive examples")
    order = np.argsort(-scores, kind="stable")
    yy, ss = y[order], scores[order]
    ends = np.r_[np.flatnonzero(ss[1:] != ss[:-1]) + 1, len(ss)]
    tp = np.cumsum(yy)[ends-1]
    precisions = tp / ends
    delta_recall = np.diff(np.r_[0, tp]) / positive
    return float(delta_recall @ precisions)


def macro_ap(y: np.ndarray, probabilities: np.ndarray, families: list[str]) -> float:
    """Each target family is evaluated against all remaining annotated elements."""
    y, probabilities = np.asarray(y), np.asarray(probabilities, dtype=float)
    if probabilities.shape != (len(y), len(families)):
        raise ValueError("Expected one column per target family")
    return float(np.mean([ap_with_ties((y == f).astype(int), probabilities[:, j])
                          for j, f in enumerate(families)]))


def pooled_seed_ap(labels: np.ndarray, groups: np.ndarray, seeds: np.ndarray,
                   probabilities: np.ndarray, families: list[str]) -> float:
    """Compute AP per seed on pooled folds, then average the seed results.

    Each seed must have exactly one prediction per (group,item) provided by caller;
    folds are already pooled. The caller is responsible for that record-level check.
    """
    labels, groups, seeds, probabilities = map(np.asarray, (labels, groups, seeds, probabilities))
    if not (len(labels) == len(groups) == len(seeds) == len(probabilities)):
        raise ValueError("Length mismatch")
    return float(np.mean([macro_ap(labels[seeds == r], probabilities[seeds == r], families)
                          for r in np.unique(seeds)]))


def jackknife_t(labels: np.ndarray, groups: np.ndarray, estimator: Callable[[np.ndarray], float],
                alpha: float = .05) -> dict:
    """Leave-one-independent-group-out jackknife-t confidence interval.

    estimator(mask) must repeat the *entire* estimand on the retained records.
    Failure to retain a positive target family is reported as undefined.
    """
    labels, groups = np.asarray(labels), np.asarray(groups)
    if labels.shape != groups.shape or labels.ndim != 1:
        raise ValueError("labels and groups must be parallel vectors")
    uniq = np.unique(groups)
    g = len(uniq)
    if g < 3:
        raise ValueError("At least three independent groups required")
    full = float(estimator(np.ones(len(groups), dtype=bool)))
    excluded = np.array([estimator(groups != group) for group in uniq], dtype=float)
    if not np.isfinite(excluded).all() or not np.isfinite(full):
        raise ValueError("Undefined replicate (e.g. missing positive family)")
    center = float(excluded.mean())
    se = float(np.sqrt((g-1)/g * np.sum((excluded-center)**2)))
    critical = float(student_t.ppf(1-alpha/2, g-1))
    return {"estimate": full, "se": se, "ci95": [full-critical*se, full+critical*se],
            "n_groups": g, "degrees_of_freedom": g-1}


def factorial_contrasts(fv: float, fp: float, dv: float, dp: float) -> dict:
    """Contrasts from scores, not from averaged raw probabilities."""
    return {"knowledge": .5*((dv-dp)+(fv-fp)), "logic_valid": dv-fv,
            "structure": .5*((dv-fv)+(dp-fp)),
            "interaction": (dv-fv)-(dp-fp)}

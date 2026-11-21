"""Simple example with invented cue values; no music from a corpus is included."""
import itertools
import json
import numpy as np

from a2_core import evaluate, certify_lp, logits, factorial_contrasts


def run():
    concepts = ["r", "a", "b", "e"]
    spec = {"Family_A": {"R": ["r"], "A": [["a", "b"]], "E": ["e"]},
            "Family_B": {"R": ["e"], "A": [["a", "b"]], "E": ["r"]}}
    states = np.array(list(itertools.product((0, 1), repeat=4)), dtype=float)
    mask = np.ones_like(states)
    valid = evaluate(states, mask, concepts, spec)
    modified = {"Family_A": {"R": ["e"], "A": [["a", "b"]], "E": ["r"]},
                "Family_B": {"R": ["r"], "A": [["a", "b"]], "E": ["e"]}}
    changed = evaluate(states, mask, concepts, modified)
    flat = certify_lp(valid, changed, False)
    structured = certify_lp(valid, changed, True)
    baseline = np.zeros((len(states), 2))
    raw_flat = logits(baseline, valid, np.array([.5, .3, .2]), 0)
    raw_structured = logits(baseline, valid, np.array([.5, .3, .2]), .7)
    out = {"n_synthetic_states": len(states),
           "valid_satisfying_states": (valid.truth == 1).sum(axis=0).tolist(),
           "flat_lp": flat, "structured_lp": structured,
           "example_flat_scores": raw_flat[:3].tolist(),
           "example_structured_scores": raw_structured[:3].tolist(),
           "factorial_identity_example": factorial_contrasts(.6, .4, .65, .35)}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    run()

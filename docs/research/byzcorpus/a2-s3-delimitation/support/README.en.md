# A2–S3 · Executable reference checks

**Language / Γλώσσα:** [Ελληνικά](README.md) · **English**

[Research overview](../README.md) · [Technical protocol](../protocol.md) · [Evidence and planned work](../evidence-and-next-steps.md)

## Scope

This directory contains two small Python files implementing **exact computational and annotation-invariant checks for A2–S3**:

- `a2s3_reference.py`: stable log-space union probabilities using a two-state forward recurrence; an independent exhaustive enumeration oracle; candidate eligibility and shared-window checks; family-specific exact-length features; family-balanced estimates; group-deletion jackknife.
- `test_a2s3_reference.py`: 25 `unittest` tests, including **120 deterministically seeded synthetic cases** comparing the dynamic program with exhaustive enumeration.

**Requirements:** Python 3.10 or later; no third-party dependencies for the tests. Run in this directory:

`python -m unittest -v test_a2s3_reference.py`

Local execution on 16 November 2026 with Python 3.13.5 passed **25/25 tests**. The maximum absolute difference in log probability or log partition function across the 120 numeric cases was **5.51 × 10⁻¹⁴**.

## Verified contracts

| Component | Verified contract |
|---|---|
| Probability | Normalisation over complete legal nonoverlapping span-and-skip paths; the union of accepted spans is counted once for each full analysis. |
| Shared window | All accepted extents and eligible variants fit the same expert-agreed local window. |
| Eligibility | Common start, accepted right endpoints, complete annotation roster, abstentions/masks, documented connective material, and next-formula start. |
| $B_L$ | **Exact family-specific length feature encoding** and articulation/text features. Full training of the regularised $B_L$ heads is reserved for a subsequent implementation. |
| Aggregation and inference | Fixed family set, equal weight across families, delete-one-independent-group jackknife, near-zero numerical standard error, and explicit interval non-issuance. |
| Two-sided result | Identical occurrence IDs and positive differences against all three prespecified reference comparisons for both truncation and extension. |

All data in these tests are **synthetic**. Segment potentials are supplied as numerical inputs; these scripts do not train or load a neural model. The verification concerns exact calculations for a specified legal segmentation space, as defined in the [research protocol](../protocol.md).

The jackknife method requires an externally supplied Student critical value with $G-1$ degrees of freedom for issuing a full 95% interval, for example `scipy.stats.t.ppf(0.975, G - 1)`. Missing critical values are explicitly reported.

## Status of previously recorded numerical results

The [A2–S3 evidence register](../evidence-and-next-steps.md) records 18 targeted checks, 17,556 stored variant slots, 20 historical result files, and 488 decision comparisons. **The original inputs, programs and complete result files for these runs are not yet part of this directory.** They are tracked separately in the [evidence matching register](verification-manifest.json) as pending independent replay.

These executable tests establish the core numerical and eligibility invariants. Replaying the original synthetic series, training the full L2-regularised $B_L$ comparators, integrating trained FV/FP/DV/DP scores, and evaluating Byzantine music are separate reproducibility and empirical stages.

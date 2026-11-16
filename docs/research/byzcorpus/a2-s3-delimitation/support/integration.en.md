# A2–S3 · Connecting verified annotations and frozen A2 scores

**Language / Γλώσσα:** [Ελληνικά](integration.md) · **English**

[A2–S3 protocol](../protocol.md) · [Reference checks](README.en.md) · [B_L training](bl-training.en.md) · [ByzCorpus data model (Greek)](../../data-model.md)

## Research objective

The [a2s3_ingest.py](a2s3_ingest.py) gateway aligns source-reviewed formula occurrences with **frozen A2 model scores**. It ingests **FV, FP, DV and DP** conditions, fits the **B_L** comparator on appropriate development groups, and evaluates **paired full-extent versus truncation/extension contrasts**. The probability numerator uses accepted spans sharing the preferred start; the full set of accepted delimitations is preserved to check the legal candidate space.

The gateway prepares the empirical workflow. Current executed checks rely on **synthetic fixtures**. The real Byzantine evaluation requires source-verified annotations and segment potentials exported from the actual trained A2 models.

## Three input files

| File | Required fields |
|---|---|
| `manifest.json` | Dataset identity, rights status, family catalogue, explicit index convention, split groups and their relation clusters, base/model IDs by replication and condition, SHA-256 of exported inputs |
| `annotations.json` | `occurrence_id`, work, witness, group, family, common window, all accepted start–end pairs, preferred start, truncation/extension, reviewer-level judgements, articulation, connective events and exclusion reasons |
| `scores.json` | Fixed per-replication base scores, segment scores for every legal candidate in every FV/DV/FP/DP cell and perturbation, shared skip potentials and model provenance |

Annotation boundaries use **global zero-based inclusive atomic-event indices**. Exported segment candidates use **window-local zero-based inclusive indices**. Every candidate span receives scores for **all families** in the prespecified catalogue.

The frozen base exports contain **temperature-calibrated, unnormalised segment log potentials** (`b_r/T_r`). A2 FV/FP/DV/DP exports likewise supply unnormalised segment potentials. A shared legal full-path normaliser is computed during evaluation.

## Integrity and scientific consistency

1. Identical candidate spaces across conditions and replications, with every accepted delimitation and both eligible variants represented.
2. Disjoint `base_train`, `head_train`, `development` and `holdout` groups, enforcing work-, witness- and historically related cluster-level separation.
3. One frozen base per replication; each A2 head declares the matching base, training groups and tuning groups.
4. Complete designated reviewer coverage, eligible right endpoints, source-confirmed connective material and the declared articulation selection rule.
5. Complete **5-replication × (2 valid + 2×10 perturbed cells)** export for the study. A reduced **1×(2+2)** configuration serves strictly as an interface pilot.
6. SHA-256 input integrity, finite numeric values, legal indexing and explicit rejection of missing or mismatched cells.

## Reproducing the checks

From the `support/` directory, with Python 3.10 or later:

```bash
python -m unittest -v test_a2s3_ingest.py
python make_demo_export.py /tmp/a2s3_demo
python a2s3_ingest.py /tmp/a2s3_demo/manifest.json /tmp/a2s3_demo/annotations.json /tmp/a2s3_demo/scores.json
# Complete synthetic five-replication / ten-perturbation export layout:
python make_demo_export.py /tmp/a2s3_full --full
python a2s3_ingest.py /tmp/a2s3_full/manifest.json /tmp/a2s3_full/annotations.json /tmp/a2s3_full/scores.json
```

The result includes per-occurrence, per-replication truncation and extension contrasts for FV, DV, FP, DP, **B_L** and the common **knowledge-free BASE**. Family-balanced summaries expose **`delta_know_S3`** and **`delta_logic_valid_S3`** as secondary log-contrast outcomes, distinct from the primary A2 family-AP estimands. `two_sided_directional_only` indicates the direction of the matched descriptive comparisons; uncertainty estimation follows the standalone S3 protocol.

## Evidence status and empirical next steps

On 16 November 2026, **24/24 new ingestion tests** and **66/66 combined tests** passed locally. A full-format synthetic export also ran successfully with five replications, ten perturbations and eight synthetic occurrences (880 condition records).

Empirical execution requires verified atomic-event transcriptions, rights assessment, final WP0/M3a judgements, a fixed family catalogue, grouped splits and the actual frozen A2 checkpoints and score exports. Inputs can remain in a permission-controlled local environment in accordance with source and annotation rights.

Earlier S3 synthetic reports of 17,556 variant slots, 20 result files and 488 decisions remain in the separate [historical evidence register](verification-manifest.json) pending access to their original inputs and scripts for independent replay.

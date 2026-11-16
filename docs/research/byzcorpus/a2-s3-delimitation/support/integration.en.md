# A2–S3 · Connecting Verified Annotations with Frozen A2 Model Scores

**Language / Γλώσσα:** [Ελληνικά](integration.md) · **English**

[A2–S3 protocol](../protocol.md) · [Reference checks](README.en.md) · [B_L training](bl-training.en.md) · [ByzCorpus data model (Greek)](../../data-model.md)

## Objective

The [a2s3_ingest.py](a2s3_ingest.py) mechanism aligns musicologically verified formula occurrences with **frozen A2 model scores**. It ingests the **FV, FP, DV and DP** conditions, fits the **B_L** comparator on the appropriate development groups, and computes **paired full-extent versus truncation and extension contrasts**. The numerator uses exclusively the accepted spans sharing the preferred start; all accepted delimitations are retained to verify the legal candidate space.

The infrastructure prepares the ingestion of real empirical data. Current executions use **synthetic examples**; the empirical evaluation requires verified sources, annotations and stored scores exported from trained A2 models.

## Three input files

| File | Content |
|---|---|
| `manifest.json` | Dataset identity, rights status, family catalogue, explicit index convention, split groups, correlated clusters, model IDs by replication/condition, SHA-256 checksums of the two exported files |
| `annotations.json` | `occurrence_id`, work, witness, group, family, common window, all accepted boundary pairs, preferred start, truncation/extension, judgements of designated specialists, articulation, connective material, exclusion reasons |
| `scores.json` | Fixed per-replication base scores, scores of all legal candidate spans for every FV/DV/FP/DP condition and perturbation, shared skip potentials, identifiers of the corresponding trained models |

Annotated boundaries and candidate extension points use **global zero-based inclusive atomic-event indices**. Score exports use **window-local indices `0…n−1` (inclusive) within the common window**. Every candidate span is scored across **all families** in the declared catalogue.

Base scores are provided as **unnormalised log-potentials, already calibrated via temperature scaling** (`b_r/T_r`). Scores for the FV/FP/DV/DP conditions are likewise provided as unnormalised span potentials (*segment potentials*). Normalisation is performed over the shared space of complete legal parses.

## Integrity checks

1. Identical candidate space across all conditions and replications, covering all accepted delimitations and both variants.
2. Disjoint `base_train`, `head_train`, `development` and `holdout` groups, checking work, witness and historically linked clusters so that dependent information follows a unified split.
3. One shared frozen base per replication; A2 head metadata are verified against the base, training groups and tuning groups.
4. Complete coverage by the preregistered specialists, eligibility of alternative delimitations, appropriate connective material and right-endpoint selection according to the articulation scale.
5. Expected layout of **5 replications × (2 valid + 2×10 perturbed conditions)** per occurrence. The minimal **1×(2+2)** layout serves exclusively for interface testing.
6. SHA-256 verification of the exact exports and rejection of incomplete, non-finite or incompatible scores.

## Execution

From the `support/` directory, with Python 3.10 or later:

```bash
python -m unittest -v test_a2s3_ingest.py
python make_demo_export.py /tmp/a2s3_demo
python a2s3_ingest.py /tmp/a2s3_demo/manifest.json /tmp/a2s3_demo/annotations.json /tmp/a2s3_demo/scores.json
# Complete synthetic five-replication and ten-perturbation layout:
python make_demo_export.py /tmp/a2s3_full --full
python a2s3_ingest.py /tmp/a2s3_full/manifest.json /tmp/a2s3_full/annotations.json /tmp/a2s3_full/scores.json
```

The mechanism outputs per-occurrence and per-replication truncation/extension contrasts for the FV, DV, FP and DP conditions, **B_L**, and the **shared knowledge-free base** (`BASE`). It computes equally weighted family means and separate **`delta_know_S3`** and **`delta_logic_valid_S3`** quantities, keeping them clearly distinct from the primary AP metrics of A2. The `two_sided_directional_only` flag refers exclusively to the sign/direction of the differences; statistical evaluation follows the separate S3 protocol.

## Evidence status and next empirical application

On 16 November 2026, **24/24 new interface tests** and **66/66 total tests** passed, including the probability and B_L checks. The `--full` exports were verified across 5 replications, 10 perturbations and eight synthetic occurrences (880 condition entries).

The empirical study requires verified atomic-event transcriptions, usage licences, final M3a/PE0 judgements, a fixed family catalogue, grouped splits, and score exports drawn directly from the trained A2 checkpoints. Ingestion can be performed from a restricted-access local directory; primary sources and individual specialist judgements retain their own distribution policies.

Older synthetic S3 records covering 17,556 variants, 20 files and 488 decisions remain in the [primary evidence register](verification-manifest.json) until the corresponding files are made available and re-executed.
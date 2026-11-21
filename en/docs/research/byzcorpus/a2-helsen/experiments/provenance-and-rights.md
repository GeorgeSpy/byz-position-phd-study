# A2–Helsen — Provenance, Reproducibility and Rights

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../../docs/research/byzcorpus/a2-helsen/experiments/provenance-and-rights.md) · **English**
<!-- language-switch:end -->

[Experimental register](README.md) · [A2–Helsen](../README.md) · [Repository licensing](../../../../../../LICENSING.md)

## Provenance and checksums

The seven entries in [`sources.csv`](../../../../../../docs/research/byzcorpus/a2-helsen/experiments/manifests/sources.csv) identify **private research snapshots** with stable identifiers `A`, `B`, `C`, `D`, `E`, `F0` and `F1`. Each SHA-256 value identifies the exact source object kept in the research archive.

For stage C, SHA-256 refers specifically to `results_summary.json`; for other stages, it refers to the corresponding complete research package. The source manifest supports **content identification**; independent re-execution of the neural training also requires authorized source data, the original software dependencies and computational configurations.

The [claims register](../../../../../../docs/research/byzcorpus/a2-helsen/experiments/manifests/claims.csv) maps statements to explicit [experiment records](../../../../../../docs/research/byzcorpus/a2-helsen/experiments/manifests/experiments.csv). Evidence tags distinguish recalculated OOF results, checked aggregate reports, reported intervals and source-inventory findings.

## Verification scope

| Component | Completed check | Public evidence |
|---|---|---|
| Corpus and folds | Element counts, disjoint melodic groups, label-frequency coverage | Aggregate census and split protocol |
| Factorial stage C | CSV/JSON consistency, contrast identities, executable tests | Condition-specific outcomes and intervals |
| Semi-CRF stages D/F0 | Precision–recall–F1 agreement, LP certificates, ten-perturbation comparisons | Target-family and overall decoded outcomes |
| Matched-access stage E | Hidden-suffix invariance tests and aggregate agreement | Separate encoder/knowledge visibility conditions |
| Diagnostic stage F0 | Estimand consistency and information-access decomposition | Fixed-head and respecified-head comparisons |
| Stage F1 | Main AP and paired group jackknife recalculated from individual OOF predictions | Aggregate sequence-order and gap-masking contrasts |

F1 OOF exports were rounded to eight decimal places. A small number of secondary DeepSets AP results are sensitive to ties introduced by that rounding; full numerical reproduction calls for full-precision `float64` predictions. The distinction between pooled OOF AP and averages of per-fold AP also remains explicit throughout the register.

## Primary sources and publication policy

| Material | Handling |
|---|---|
| CantusCorpus pitch sequences and texts | Governed by the terms of the primary source; the study cites CC BY-NC-SA 4.0 for its dataset version. Only aggregate results are published here. |
| Helsen dissertation, appendices and analytical annotations | The primary source is cited. Redistribution of individual analysis records, transcriptions or work-level labels requires a separate rights review. |
| Private `helsen.json` and `folds.json` | Retained in the local research archive with extraction and transformation history. |
| Individual OOF predictions and work identifiers | Retained for numerical reproducibility in private storage. |
| Expert review forms and blinded matching key | Stored separately until the independent judgments have been completed. |
| Model checkpoints, GPU logs and runnable research code | Retained as research outputs. Public software distribution follows review of dependencies, licenses and reproducibility requirements. |
| Aggregate tables and original report text/figures | Published according to the repository's relevant text and code licenses. |

## Full reproduction procedure

1. Obtain authorized access to the musical source materials and annotations.
2. Verify the private snapshots against `sources.csv` and each package's own checksum manifest.
3. Reproduce the stage-A inventory, group-disjoint folds and stage-B family mappings.
4. Retrain the matched neural backbones with the specified folds and seeds; export predictions at full precision.
5. Compute four-family macro AP from pooled out-of-fold predictions **within each seed**, then average across five seeds.
6. Recompute knowledge-validity and logical-integration contrasts, using the matching perturbation set for each experiment.
7. Decode complete works using the semi-CRF and report both target-family and overall exact span/family F1.
8. Repeat matched-access, fixed-specification and gap-aware masking comparisons; calculate paired intervals at the independent melodic-group level.

The principal [A2 technical protocol](../../../../../../docs/appendices/k.md) defines the planned Byzantine study. Confirmatory evaluation will use **new independent musical materials** after musicological adjudication of the family specifications and prospective statistical calibration.

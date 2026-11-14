# 8. Architectural decisions and evidence register

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/08-decisions-and-evidence.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Models](01-research-questions-and-models.md) · [Byzantine protocol](07-byzantine-protocol.md) · [Experiment register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv)

Architectural decisions bring together findings from synthetic series S1 and S2, the exploratory Gregorian application H1 and numerical verification. Experiment conditions and identifiers are documented in the [experiment register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv).

## Architectural decisions

| Code | Decision | Evidence | Status |
|---|---|---|---|
| D-PA-01 | The variable-length formula and its family form the prediction unit; F is the reference model for validation on real data. | S1-*, S2-F, H1-F-TEXT, H1-F-MEL | In force |
| D-PA-02 | F–C_comp preserves a single family across the parent formula and its internal sub-segments. The A–C_fac contrast of M1-X remains separate. | S1-G0-48-EXT … S1-G2-48, S2-CCOMP | In force; C_comp as evaluated is not the selected candidate architecture |
| D-PA-03 | LASM is the first extension to examine with required controls for length, shuffled bases, marginals and matched capacity. | S1-BI-*, S2-LASM, H1-LASM-* | In force; positive indication in melody-only conditions |
| D-PA-04 | A contextual base uses joint history-aware $`Q_0`$; local A1 remains an explicitly separate approximation. | N1-NHP-128, N1-A1-MULTICUT | In force |
| D-PA-05 | The family mechanism (RM, DBC) is evaluated in a subsequent stage, with $`R^{\mathrm{id}}`$ / $`\bar R`$, duration weighting, a direct family head and capacity-matched F controls. | S2-RM, N1-CORE-25 | Planned real-data evaluation |
| D-PA-06 | Helsen results are exploratory; the identified protocol issues are addressed before new training. | H1-* | In force |
| D-PA-07 | All executed outcomes are documented, including negative and withdrawn runs. DBC and the Byzantine application remain at the specified-design stage until executed. | All | In force |
| D-PA-09 | Certified re-ranking requires an explicit upper bound for the next unexamined analysis. | N1-KBEST | In force |

## Negative and neutral findings

- C_comp scores below F in every synthetic condition, including the one designed to favour composition, and varies substantially across random initialisations.
- The F+C_comp hybrid does not outperform F.
- With text features, LASM does not provide a gain; in the Gregorian study it decreases exact-element F1 slightly (−0.021).
- In series S2, LASM and RM comparisons against capacity-matched F both have confidence intervals containing zero.
- Gregorian family recognition remains challenging (accuracy 0.448 on reference elements).
- The initial Helsen batch was withdrawn after early stopping terminated training prematurely (7–8 epochs; [Section 5](05-gregorian-benchmark.md#chronology-of-experiments)).

## Next experiments

Applying the architectures to the **Byzantine corpus** is the primary research direction. The extended Helsen evaluation proceeds in parallel as comparative research.

| Code | Experiment | Prerequisite |
|---|---|---|
| P-BYZ-INITIAL | First training and evaluation on complete, annotated Byzantine works using F and joint formula–family recognition | First eligible ByzCorpus release; validated annotations |
| P-BYZ-FC | F–C_comp with common family identity, matched capacity, annotation-learning curve and a separate C_fac reference | P-BYZ-INITIAL |
| P-BYZ-LASM | F, length/count, multigram, exact global NHPYLM probability, shuffled base and marginal controls on identical data | P-BYZ-INITIAL; frozen fold-specific bases |
| P-BYZ-DBC | Factorial evaluation of family contribution, duration and complete-span scoring with identical family supervision | Independently evaluable families and eligible historical examples |
| P-BYZ-GENERALIZATION | Generalisation to new works, sources, modes and genres, distinguishing analytical family from historical identity | P-BYZ-INITIAL |
| P-REAL-CORE-6 | Parallel Helsen comparison: six scoring configurations of the same F, with and without text, across available modes | New grouped splits, label and long-span checks, exact $`Q_0`$ |
| P-REAL-FC | F versus C_comp on real Gregorian data, including a label-learning curve | Shared folds and held-out groups |

## Reproducibility and data access

Experiment identifiers, metric definitions and aggregate measurements are available in the accompanying [experiment register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv) and [metrics register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/metrics.json). Source code for synthetic S2 training and NHPYLM extraction is scheduled for release in a separate code-reproducibility phase, together with dependencies and source result files in JSON format. Helsen's melodies and detailed analytical annotations remain governed by the terms of their respective sources.

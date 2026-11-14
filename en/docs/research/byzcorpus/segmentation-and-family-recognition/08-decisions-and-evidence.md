# Decisions and evidence register

[Summary](README.md) · [Greek decision register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/08-decisions-and-evidence.md) · [Experiment register (CSV)](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv)

Each decision refers to experiment identifiers in the [experiment register](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/support/manifests/experiments.csv). Decisions may be revised with new data.

| Code | Decision | Evidence | Status |
|---|---|---|---|
| D-PA-01 | The variable-length formula and its family are the prediction unit; F is the reference model for real-data validation. | S1-*, S2-F, H1-F-TEXT, H1-F-MEL | In force |
| D-PA-02 | The F–C_comp contrast keeps the same family in the formula and all internal sub-segments. The F–C_fac contrast of M1-X stays separate. | S1-G0-48-EXT … S1-G2-48, S2-CCOMP | In force; C_comp, as tested, is not a candidate architecture |
| D-PA-03 | LASM is the first extension to test, with mandatory length, shuffled-base, marginal and capacity controls. | S1-BI-*, S2-LASM, H1-LASM-* | In force; evidence only without text |
| D-PA-04 | For a context-dependent base, the global $`Q_0`$ with carried history is used; the local A1 is a separate approximation. | N1-NHP-128, N1-A1-MULTICUT | In force |
| D-PA-05 | The family term (RM, DBC) is a second stage, controlled by $`R^{\mathrm{id}}`$ / $`\bar R`$, duration weighting, a direct family head and capacity-matched F. | S2-RM, N1-CORE-25 | Planned for real-data evaluation |
| D-PA-06 | Helsen results are exploratory; the known pipeline problems are fixed before new training. | H1-* | In force |
| D-PA-07 | All executed results are published, positive, negative and withdrawn. DBC and the Byzantine application remain planned until run. | All | In force |
| D-PA-08 | Centring $`\log Z_0`$ does not improve performance; the reported +0.027 came from an unpaired comparison. | S1-CENTER-04 | Correction |
| D-PA-09 | Certified re-ranking requires an explicit bound for the next unexamined analysis. | N1-KBEST | Correction |

## Negative and uncertain results

- C_comp falls behind F in every synthetic cell, including the one designed to favour it, and is unstable across seeds.
- The F+C_comp hybrid does not exceed F.
- With text input LASM does not improve performance; on Gregorian data it lowers it slightly (−0.021).
- In the matched synthetic series neither LASM nor RM is distinguishable from a capacity-matched F.
- Family recognition on Gregorian elements remains weak (0.448 on reference units).
- A first batch of Helsen runs was withdrawn because early stopping produced an artefact.

## Next experiments

The primary research programme develops architectures for Byzantine chant formulae. The Gregorian experiments constitute a parallel comparative workstream.

| Code | Experiment | Prerequisite |
|---|---|---|
| P-BYZ-INITIAL | Initial F training and evaluation on complete annotated Byzantine works | First eligible ByzCorpus release and independently verified annotations |
| P-BYZ-FC | F versus C_comp with the same family ontology, matched capacity and a label-learning curve; C_fac as a separate reference | P-BYZ-INITIAL |
| P-BYZ-LASM | Compare F, length/count, multigram, exact NHPYLM boundary event, shuffled-base and boundary-marginal scores | Frozen training-only bases and paired evaluation |
| P-BYZ-DBC | Factorial assessment of family composition, duration weighting and full-span modelling | Family-labelled Byzantine data and verified identity criteria |
| P-BYZ-GENERALIZATION | Held-out works, sources, modes and repertorial genres | P-BYZ-INITIAL |
| P-REAL-CORE-6 | Parallel Helsen comparison: six scores of the same F with and without text | Corrected splits, labels, span lengths and exact NHPYLM $`Q_0`$ |
| P-REAL-FC | F versus C_comp on Gregorian data, including a label curve | Common held-out groups |

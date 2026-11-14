# 5. Exploratory Gregorian benchmark: complete Helsen elements

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/05-gregorian-benchmark.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Boundary information](03-multiscale-boundary-information.md) · [Comparative NHPYLM–Helsen pilot](../gregorian-nhpylm-helsen-pilot.md)

This exploratory study evaluates the models on real Gregorian responsories using Helsen's analytical segmentation into melodic elements. The family ontology of this material is independent of the Byzantine formula-family ontology. Training and evaluation on annotated Byzantine works constitute the next application phase.

## Material

Melodies from Paris, BnF, lat. 12044 in CantusCorpus v0.2 were aligned with the melodic-element analysis of responsories in Helsen (2008). The earlier [pilot](../gregorian-nhpylm-helsen-pilot.md) uses 148 mode-1 responsories with alignment distance at most 0.05 in its principal analysis (from 214 in Helsen: 55 above the distance threshold and 11 unmatched) and, exploratorily, 626 responsories across all modes. This experiment retains **123 of those 148** mode-1 responsories after excluding 25 works with incomplete element-to-melody projection:

- 123 responsories, 121 melodic groups, 916 elements, 793 internal boundaries;
- 18 labels: 16 standardised elements occurring at least 12 times, one category for rare standardised elements and one for non-standardised elements;
- three folds grouped by melody; per fold, approximately 60 training responsories, 17–23 for development and 40–42 for testing.

Only aggregate measurements are published here; melodies, texts and detailed analytical annotations remain with their respective sources.

## Protocol

- F with a bidirectional recurrent encoder; maximum element length $`L_2=36`$ events; melody input with or without syllable and word indicators.
- Fixed training length of 30 epochs × 16 updates, using random initialisations 0 and 1.
- LASM base: a zero-order multigram model with sub-segments of up to seven events, trained without family labels on the 995 responsories in Phase A of the pilot. Two melodic-group folds are used for the unsupervised base, and each work is scored by the model from the other fold.
- Control base: the same model trained on melodies whose note order has been shuffled.
- Heuristic baselines: word-final boundaries when the final pitch is C, D, F or a; and boundaries from the earlier NHPYLM pilot restricted to word endings.

## Results

| System | Initialisations | Boundary F1 | Predicted boundaries | Exact-element F1 | Joint F1 |
|---|---:|---:|---:|---:|---:|
| Cadence rule | — | 0.582 | 1616 | 0.173 | — |
| NHPYLM cuts at word endings | — | 0.550 | 1783 | 0.139 | — |
| F, melody and text | 2 | **0.828** | 723 | **0.684** | 0.319 |
| F + LASM, melody and text | 2 | 0.808 | 726 | 0.663 | 0.311 |
| F + LASM with shuffled base, melody and text | 1 | 0.804 | 705 | 0.649 | 0.291 |
| F, melody only | 2 | 0.524 | 691 | 0.329 | 0.149 |
| F + LASM, melody only | 2 | 0.572 | 688 | 0.373 | 0.170 |
| F + LASM with shuffled base, melody only | 2 | 0.517 | 688 | 0.327 | 0.140 |

Exact-element F1 by initialisation (0 and 1): F with text 0.659 / 0.708; F+LASM with text 0.652 / 0.674; F melody only 0.294 / 0.364; F+LASM melody only 0.346 / 0.401; shuffled-base melody only 0.283 / 0.372.

Family accuracy **at reference boundaries** is 0.448 for F with text (18 labels). Joint F1 (0.319) is substantially below exact-element F1 (0.684), reflecting the additional challenge of predicting family identity. The two measures quantify distinct requirements.

| Contrast (exact-element F1) | Difference [95% work groups] |
|---|---:|
| F, melody and text − cadence rule | +0.511 [+0.466, +0.557] |
| F, melody only − cadence rule | +0.157 [+0.108, +0.208] |
| Text: F with melody and text − F with melody only | +0.354 [+0.311, +0.398] |
| LASM − F, with text | −0.021 [−0.040, −0.001] |
| Real − shuffled base, with text (initialisation 0) | +0.003 [−0.028, +0.035] |
| LASM − F, melody only | +0.044 [+0.025, +0.063] |
| Real − shuffled base, melody only | +0.046 [+0.026, +0.065] |
| Shuffled base − F, melody only | −0.002 [−0.017, +0.014] |

With initialisations also resampled: LASM − F with text −0.021 [−0.050, +0.011]; melody only +0.044 [+0.015, +0.071]. The estimate of training variability uses just two initialisations; a later phase will include additional paired repetitions.

**Principal findings.** (1) With approximately 60 training responsories, F identifies complete elements more accurately than the cadence rule while predicting fewer than half as many boundaries. (2) Text features provide strong information about elements in this repertory. (3) LASM produces a positive difference in melody-only input (+0.044) that is absent for the shuffled base; with text the difference is −0.021. (4) Family recognition remains a substantive target for architectural development.

## Chronology of experiments

1. **Initial exploratory batch (withdrawn).** Early stopping based on development joint F1 terminated training at 7–8 epochs in several folds. It produced an apparent LASM benefit with text (boundary F1 0.798 versus 0.594), which disappeared when training length was fixed. This batch was excluded from the comparative tables; its outcomes are retained in the experiment records.
2. **Protocol chronology.** The fixed training length was chosen **after inspection of the initial batch's test results**. The second initialisation and shuffled-base condition for melody-only input were added after initialisation 0 had been evaluated. The decision rule had been defined earlier, but repetitions used the same works and folds. The resulting estimates establish exploratory feasibility and motivate a subsequent independent evaluation.
3. **LASM weight.** These runs did not restrict $`\lambda_b`$ to nonnegative values, and its final fitted values were not saved.

## Technical findings and changes for the next phase

| Issue | Consequence | Correction before new training |
|---|---|---|
| Elements longer than $`L_2=36`$ (maximum 48; 99% at most 35) | Three to four works per fold were excluded from training. The corresponding test elements cannot be predicted and count as errors. A boundary-gap loss was calculated with an implicit index clamp, so bits-per-gap values for those works are unreliable; F1 metrics are unaffected. | Validate lengths before training; determine $`L_2`$ from training data; report coverage. |
| Label vocabulary constructed from all 123 works | Label frequency thresholds were defined before splitting into folds. | Build vocabulary on the training fold only; distinguish rare, unknown and non-standardised categories. |
| Unsupervised-base data | Base folds differ from supervised folds; the base may have seen unlabelled melodies from supervised test works. | Train the main-condition base exclusively on training groups; explicitly define and report any *transductive* evaluation separately. |
| Family accuracy at reference boundaries | The calculation omits elements that cannot be represented with $`L_2=36`$. | Report coverage alongside accuracy. |

## Next experiment

All modes in the aligned corpus, new grouped splits incorporating these corrections, a label-learning curve, at least three initialisations, NHPYLM as a base and the six scoring configurations from [Section 3](03-multiscale-boundary-information.md#next-experiment). The primary hypothesis will be registered before training: without text, LASM exceeds F and the shuffled base in exact-element F1.

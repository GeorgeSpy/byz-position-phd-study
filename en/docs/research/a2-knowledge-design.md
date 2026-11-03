# A2 — Testing the value of musicological knowledge

**Language / Γλώσσα:** [Ελληνικά](../../../docs/research/a2-knowledge-design.md) · English

[Research programme](../../README.md) · [Full methodology — Appendix K](../appendices/k.md) · [Executable feasibility studies](../../../docs/research/a2/support/README.md)

## From the musical question to the experiment

A2 examines whether documented relations defining a family of melodic formulae help recognise new occurrences, and what logical composition of those relations contributes. M1 supplies the selected representation R⋆ and architecture A. A2 applies a controlled knowledge intervention to that shared base.

The **content question** compares valid specifications with specifications perturbed under controlled structural and distributional constraints. The **composition question** compares additive summaries with an additional logical violation penalty. Both address a particular operational model and a declared panel of perturbations.

## Family specifications

Each musicological card records sources, scope, examples, disagreements and three computational roles:

| Role | Musical interpretation | Logical use |
|---|---|---|
| R — requirements | Properties required for the formation under study | Conjunction |
| A — alternative groups | Admissible internal forms | Disjunction within each group, conjunction across groups |
| E — exclusions | Incompatible properties | Negation of each excluded property |

Supportive observations have their own metadata field. Their computational role requires musicological validation. In the provisional *kylisma* pilot, supportive neumatic patterns remain outside Q and φ pending PE0 review; extractable features can remain in the common concept bank.

Independent specialists judge boundaries and family membership before applying the tested rule, without access to it or model predictions. A common bank of observed concepts and missingness masks serves every condition. Specification changes affect role assignments and composition while the underlying extracted values remain shared.

## Four conditions

| Use of knowledge | Valid V | Perturbed P |
|---|---|---|
| F — additive summaries | FV | FP |
| D — logical penalty | DV | DP |

$$
\ell_{F,K}=b_{\widehat\psi}+w^\top Q_f^K,\qquad
\ell_{D,K}=b_{\widehat\psi}+w^\top Q_f^K-\lambda v_f^K.
$$

F uses three summaries Q_R,Q_A,Q_E in [−1,1]. D adds a penalty when the full rule is false. Kleene logic distinguishes true, false and unknown; unknown incurs no main penalty. Weights are shared across families, sum to one and are at least 0.1. Lambda is fitted in [0,2]. F's fixed compression into Q is part of the experimental comparison.

The B_K comparator fits a free family-specific linear head to the full concept bank without a specification. B⋆ adds neural capacity, supervised contrastive learning, family prototypes and matched concept supervision. Its capacity and cost are reported separately.

## A small example

Consider one required cadence c₁, one alternative group {c₂,c₃}, and exclusion c₄. Actual concepts filling these roles require musicological review. For values (1,1,0,0), Q=(1,0,1): the group's additive mean is zero and its logical disjunction is true.

With base score 0.4 and weights (0.4,0.3,0.3), both F and D score 1.1. Suppose a permitted global permutation replaces the requirement with a different concept of the same type that is false here. Then Q=(−1,0,1), F scores 0.3, and D scores −0.5 when λ=0.8. This displays the separate contributions of content and penalty. The numerical example holds weights fixed; every experimental head is refitted under the common constraints. Evaluation uses family probabilities with a shared normalisation.

## Outcomes and interpretation

Occurrences are ranked separately for each family. AP_fam averages family AP over the fixed evaluation family set, weighting occurrences equally and using independently judged accepted boundary pairs. Tied scores enter together. S averages the five fitted repetitions; S̄ averages the ten perturbed specifications.

$$
\Delta_{\mathrm{know}}=\tfrac12\{S(D,V)-\overline S(D,P)+S(F,V)-\overline S(F,P)\},
$$
$$
\Delta_{\mathrm{logic},V}=S(D,V)-S(F,V).
$$

The first contrast concerns valid content relative to the selected perturbation panel. The second concerns the particular logical mechanism under valid knowledge. B_K helps assess practical benefit alongside perturbation-induced deterioration. Interaction, difficult examples and joint boundary–family recognition are supplementary outcomes.

| Finding | Interpretation, with uncertainty and meaningful-effect thresholds |
|---|---|
| Both contrasts positive | Valid knowledge and this logical composition contribute to ranking. |
| Knowledge positive, logic near zero | Content helps; lambda and violation activation clarify the penalty's contribution. |
| Logic near zero and fitted λ<0.1 | Training makes little use of the penalty. |
| Wide uncertainty or frequent undefined analyses | The result guides additional groups, family coverage and annotation. |

## Training and cost

Each repetition has its own trained A(R⋆) base. Within a repetition, one frozen checkpoint serves every FV/DV/FP/DP condition and B_K. The five bases share data and settings.

Development groups are divided into base training D_base and held-out calibration/head-fitting D_head. A common temperature is fitted first on D_head; the base and temperature are then frozen while fitting heads. H is evaluated once after all choices and gates. Grouped cross-fitting is a separately costed sensitivity.

The main budget is 120 fits per final split: 10 valid, 100 perturbed and 10 external-comparator fits. Base fitting, tuning and sensitivities add to that count.

## Feasibility

| Question | Synthetic check | Corpus-dependent check |
|---|---|---|
| Can ten distinct perturbations be generated? | Compatible permutations, canonical cards, observed Q/φ support and LP bounds | Musical applicability, non-synonymy and real development support |
| Can a small number of groups support inference? | Exact null constructions, coverage, FWER and probability of a valid analysis | Calibration using the dependence and family composition measured in PE0 |
| Where should heads be fitted? | Base-training versus held-out groups; grouped cross-fit sensitivity | Full pilot with the actual A and extractors |
| Is the logical term used? | Lambda distribution, boundary contact and violation activation | Same diagnostics by family, repetition and perturbation |

The candidate primary procedure uses delete-one-group jackknife standard errors, a Student t(G−1) reference and one-sided Holm at 0.025. Confirmatory activation depends on successful pilot calibration; full bootstrap-t is a sensitivity. Report valid-analysis probability, error and power separately. Synthetic evidence supports computational feasibility under declared conditions. Sparse family coverage can substantially reduce the probability of an analysable result. The [support guide](../../../docs/research/a2/support/README.md) describes the executable evidence and its scope.

A2 is a core study alongside M1 and M2. Q_real belongs to M2a and the separate ECSI protocol. ECSI studies probabilistic concept composition with its own design. M3a supplies independent musicological validation; M5-min applies the evaluated recognition system to complete works.

The score-minus-penalty form connects to Chang, Ratinov & Roth, *Structured learning with constrained conditional models* (2012), [DOI](https://doi.org/10.1007/s10994-012-5296-5). Raman et al., *Learning to Deceive Knowledge Graph Augmented Models via Targeted Perturbation* (2021), [paper](https://openreview.net/pdf?id=b7g3_ZMHnT0), motivate examining semantic use of perturbed knowledge. [Appendix K](../appendices/k.md) specifies the proposed experiment.

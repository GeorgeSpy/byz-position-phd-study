# M2 — Revised design of family-based and historical supervision

**Methodological documentation · 3 November 2026**

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/research/m2-eise-research-design.md) · **English**
<!-- language-switch:end -->

> **Status:** Revised research specification. The available algorithmic and synthetic checks support individual design decisions. Evaluation of the full architecture on annotated musical works, assessment of historical-pair sufficiency, and final calibration of the statistical procedure are planned for WP0/WP1 and the subsequent experimental stages.
>
> **Related documents:** [M1 revision](m1-selection-decision.md) · [Core research programme](../../README.md) · [Detailed Chapter 6 (Greek)](../../../docs/full/06-eise.md) · [Appendix G (Greek)](../../../docs/appendices/g.md) · [Appendix F (Greek)](../../../docs/appendices/f.md) · [Data partitioning (Greek)](../../../docs/appendices/d.md).

## 1. Why the M2 design was revised

A melodic formula retains its family identity even when its particular realisation varies substantially. M1 investigates how a formula can be recognised in continuous notation by identifying its boundaries and the family to which it belongs. M2 builds on this foundation. It examines how a model learns relationships among different occurrences and which properties of each individual realisation remain accessible in the resulting representation.

Developing the architecture revealed the need to distinguish learned neural representations from direct symbolic baselines. The revision therefore separates architecture A from the two B0 baselines and ensures that neural comparisons start from matched weights in each replicate. It also assigns distinct roles to two sources of supervision: independently validated membership in the same family, and a historically documented co-exegesis of the same passage.

This distinction leads to two connected studies. **M2a** investigates relational learning of family identity while assessing preservation of realisation-specific information. **M2b** evaluates the contribution of historical supervision in the shared domain of verified exegeses and independent performances. The historically supervised **EISE condition** (*Exegesis-Invariant Segmental Encoder*) uses verified co-exegeses of the same passage, trained with the common architecture A.

## 2. From M1 to M2: architecture and initialisation

M1 compares twelve representations in the $`U\times\Phi`$ grid and selects one operational $`R^\star`$ using rule J. Selection is performed with the prespecified architecture A, which combines a trainable neural encoder with a segmental semi-CRF of zero order with respect to label transitions between adjacent segments. M1's architectures B and C are evaluated across the complete grid as separate, descriptive comparisons.

M2 carries forward the **selected input representation** and **architecture configuration**, recorded as `A_M1_selected`. The identifier `m1_checkpoint_id` records the trained M1 weights for reproducibility. B1, B2, and EISE are **trained from scratch using identical initial weights in each replicate with matched random initialisation**; their shared starting point is recorded as `m2_init_checkpoint_id`.

If self-supervised pretraining is selected, it uses only the eligible training data within the corresponding partition. The same pretrained initial state is supplied to all compared conditions. Works and related-source groups are partitioned before training, with common passages and historical dependencies documented separately. The main historical comparison uses the single operational $`R^\star`$. The set $`\mathcal R^\star`$ represents selection uncertainty, and at most one additional $`R_{\mathrm{sens}}`$ may be used for a prespecified descriptive sensitivity analysis.

Matching the architecture, initialisation, data partitions, and computational budget enables a controlled investigation of the contribution made by the source of relational supervision.

## 3. Common neural architecture A and representations of a melodic formula

**Architecture A**, shared by B1, B2, and EISE, receives a symbolic sequence of melodic events $`X=(e_1,\ldots,e_T)`$ and produces local states:

```math
h_t=g_\theta(X,t).
```

These states encode information about each event and its musical context. For a candidate segment $`[s,e]`$, the encoder aggregates the relevant states and computes a family-identity representation $`z_{\mathrm{id}}`$. This representation supports family classification and relational attraction between occurrences.

Information about the particular realisation is assessed primarily through the local states $`h_t`$. An auxiliary reconstruction objective aims to keep differences between realisations of the same family accessible. A separate projection $`z_{\mathrm{real}}`$, if used, will be evaluated as an additional architectural choice. Because the relational loss also affects the shared encoder, preservation of realisation-specific information requires independent tests.

The semi-Markov model scores complete variable-length segments and jointly predicts their boundaries and family labels. Zero order denotes the absence of family-label transition terms between adjacent segments. The principal decoding pathway produces a globally non-overlapping analysis. Ambiguous boundaries, unknown families, and abstention retain their separate evaluation specifications.

## 4. Symbolic baselines and neural conditions

The conditions differ in how they use symbolic descriptions and supervisory relationships.

| Condition | Purpose |
| --- | --- |
| $`\mathrm{B0}_{\mathrm{sym}}`$ | Supervised symbolic semi-CRF with fixed features and trainable heads. Assesses symbolic recognition without learned neural representations. |
| $`\mathrm{B0}_{\mathrm{profile}}`$ | Direct symbolic profile of historical variation for external comparison with performance variability. |
| $`\mathrm{B1}`$ | Neural encoder A with segmental and family supervision and an objective that preserves realisation-specific information. |
| $`\mathrm{B2}_{\mathrm{fam}}`$ | B1 supplemented with family-based relational supervision from independently validated occurrences in M2a. |
| $`\mathrm{B2}_{\mathrm{main}}`$ | Family-based condition with matched pairs for the common historical evaluation domain in M2b. |
| $`\mathrm{EISE}`$ | The same neural architecture, using verified historical co-exegeses of a specific passage as positive pairs. |

The $`\mathrm{B0}_{\mathrm{sym}}`$ baseline measures the contribution of fixed symbolic features to recognition. The $`\mathrm{B0}_{\mathrm{profile}}`$ baseline supplies a direct historical profile for comparison with performance. These baselines address distinct questions. B1, B2, and EISE share a trainable neural backbone and a matched experimental protocol.

## 5. M2a — Family relationships as supervision

M2a asks whether learning from realisations of the same family improves recognition on held-out works. Positive pairs connect occurrences with independently validated family membership and controlled provenance. Performance on difficult examples, including superficially similar occurrences from different families, is evaluated separately.

The shared training loss is:

```math
\mathcal L_m=\mathcal L_{\mathrm{seg}}+
\lambda_f\mathcal L_{\mathrm{fam}}+
\lambda_r\mathcal L_{\mathrm{rec}}+
\lambda_p^{(m)}\mathcal L_{\mathrm{pair}}^{(m)}.
```

The terms respectively represent segmental likelihood, family classification, reconstruction of local information, and attraction of positive pairs in $`z_{\mathrm{id}}`$ space. For B1, $`\lambda_p^{(\mathrm{B1})}=0`$. Weights and exposure of realisations are selected on the development data under a shared computational budget. Positive-pair attraction is considered separately from full contrastive alternatives using negative examples.

M2a's primary measure is:

```math
\Delta_{\mathrm{famrel}}=
\mathrm{AP}_{\mathrm{fam}}(\mathrm{B2}_{\mathrm{fam}})
-
\mathrm{AP}_{\mathrm{fam}}(\mathrm{B1}).
```

Estimation uses the same held-out occurrences and paired uncertainty intervals. M2a has a **descriptive and estimation-focused status**. Recognition performance must be interpreted jointly with preservation of realisation-specific information, assessed through $`Q_{\mathrm{real}}`$.

### Preserving realisation-specific information

$`Q_{\mathrm{real}}`$ examines three prespecified aspects on held-out data: reconstruction of masked symbolic features; discrimination between two realisations of the same family that differ in melodic or temporal organisation; and prediction of local properties using a low-capacity linear probe. An acceptable margin of degradation relative to B1 is defined in advance. Additional diagnostics examine the identity branch without the textual feature layer $`L`$, difficult negatives, and the relationship between the geometry of $`z_{\mathrm{id}}`$ and information retained in the local states $`h_t`$.

$`Q_{\mathrm{real}}`$ governs the validity of the descriptive interpretation of $`\Delta_{\mathrm{famrel}}`$ and remains outside the family of confirmatory hypotheses.

## 6. M2b — What historical co-exegeses contribute

The historical study considers pairs of exegeses documenting **the same specific passage**. Each relationship is associated with its source, historical witness, passage correspondence, and independent judgement of family membership. Theoretical modal evidence remains a separate category, subject to its own eligibility rules.

EISE is compared with $`\mathrm{B2}_{\mathrm{main}}`$. In the latter, positive pairs are drawn from different works belonging to the same family, without a directly documented co-exegetical relationship. EISE pairs instead derive from historically verified relationships concerning the same passage. The two sets are matched for family, provenance, graph structure and degree, surface distance, node exposure, and computational budget. Feasibility of this matching is established before the main training stage.

The comparison uses identical initial weights and the same segmental and family supervision. The systematic difference lies in the provenance of the positive pairs. This experimental variable connects musicological evidence of exegesis with learned representations of variation.

## 7. Independent evaluation against performance

Historical occurrences are aligned to corresponding internal musical regions $`u`$, using symbolic notation and documented melodic relationships. A historical profile of within-family variation is obtained from the local states $`h(u)`$ for each family and training condition. The basic form of the measure is:

```math
\widehat{\tau}_{f,m}(u)=
\sqrt{\frac{\operatorname{tr}\widehat{\Sigma}_{f,m}(u)}{d_h}},
```

where $`\widehat{\Sigma}`$ is the weighted covariance matrix and $`d_h`$ the dimensionality of the local states. Correlated historical witnesses and multiple exegeses receive weights that respect the independence structure of the source groups.

M4-min defines the external $`\Gamma_f(u)`$ as **the variability of normalised timing between chanters** in corresponding musical regions. $`S_m`$ summarises rank agreement between historical and performance-variation profiles in the shared eligible domain. M2b has **one primary historical contrast**:

```math
\Delta_{\mathrm{hist}}=
S_{\mathrm{EISE}}-
S_{\mathrm{B2}_{\mathrm{main}}}.
```

The comparison is **two-sided**. A positive difference indicates greater agreement with the independent criterion under EISE; a negative difference favours the family-supervised condition. Family weights, matched graphs, replication, and the final estimation procedure are specified before the historical test set is accessed.

The secondary diagnostic difference is defined as

```math
\Delta_{\mathrm{learn}}=
S_{\mathrm{EISE}}-
S_{\mathrm{B0}_{\mathrm{profile}}}
```

and compares EISE with the direct symbolic historical profile. Individual $`S_m`$ values and the direct historical–performance correlation are reported separately. Regions with undefined or constant profiles are documented and handled under prespecified abstention rules.

## 8. Learning from partial annotations

Sources may support several admissible boundaries or alternative analyses of the same region. Semi-CRF training preserves these alternatives through exact summation over compatible analyses:

```math
\mathcal L_{\mathrm{seg}}(X,C)=
\log Z_\theta(X)-
\log Z_\theta(X;C),
```

where $`Z_\theta(X)`$ sums the weights of all globally legal analyses, and $`Z_\theta(X;C)`$ those satisfying the available annotation $`C`$.

The revised annotation contract separately records **which families were checked** within an explicit scope (`checked_families`), **which logical obligations apply** (`obligations`), and **which background regions were explicitly observed** (`observed_background`). Missing labels are interpreted using documented annotation coverage. Obligations may specify exactly one of several alternatives, at least one admissible occurrence, or a set of complete alternative analyses.

The final implementation will require identical semantics in the exhaustive enumeration of small examples and in the symbolic constraint compiler. Their equivalence must be tested against the legal-analysis set, boundary compatibility, loss gradients, and dynamic programming.

## 9. Weighting unique annotation obligations

The **proposed D1 correction**, pending integration into the active Appendix G and implementation, addresses duplicate counting of annotation evidence in overlapping windows. It specifies an immutable registry of unique obligations and cluster-level weighting. Acceptance requires exact checks against exhaustive examples and corresponding gradients.

M2 adopts **M1's shared complete-formula evaluation protocol**. When reference annotation permits alternative complete analyses, the compatible reference analysis is selected at corpus level to maximise the single ratio $`2M/(P+X)`$, using the actual total numbers of predictions and reference occurrences. The mathematical definition and its tests belong to the [M1 evaluation specification](m1-selection-decision.md).

The final implementation will be checked for partial-annotation semantics, unique obligations, globally legal reference analyses, and gradient correctness. Synthetic checks are documented separately from real-data performance.

## 10. Conditions for the confirmatory historical comparison

Confirmatory evaluation in M2b depends on three adequacy gates:

| Gate | Purpose |
| --- | --- |
| **G-PAIR** | Sufficient independent historical pairs, reliable historical documentation, and feasible $`\mathrm{B2}_{\mathrm{main}}`$–EISE matching. |
| **G-PERF** | Sufficient reliable independent performances in the corresponding musical regions. |
| **G-STAT** | Adequate precision, power, and calibration of the particular statistical procedure under the corpus's dependence structure. |

$`\Delta_{\mathrm{hist}}`$ is **M2's sole primary confirmatory contrast**, evaluated using a two-sided test and joint resampling over independent work–source groups and chanters. The exact significance level and interval procedure are finalised consistently with historical protocol Γ2–Γ8 before the held-out test set is accessed. M2a retains its estimation-focused status, and $`Q_{\mathrm{real}}`$ assesses the validity of its interpretation.

When the shared domain is limited, findings are reported with their actual coverage bounds. Where historical or performance evidence is insufficient, the design documents the available evidence, estimable quantities, and reasons why confirmatory historical evaluation is not activated.

## 11. Sequence of validation and experiments

Implementation is organised into distinct, reproducible stages:

1. **WP0 — source inventory.** Works, sources, family specifications, historical pairs, witness independence, access rights, and performance coverage.
2. **Mathematical implementation checks (G-ORACLE).** Following the initial source inventory and before the main training runs, exhaustive enumeration, segmental decoding, partial annotations, obligation weighting, and gradients are verified.
3. **M1.** Architecture A is fixed, $`R^\star`$ is selected, and architectural comparators are evaluated.
4. **M2a — family-relational learning.** Paired B1–$`\mathrm{B2}_{\mathrm{fam}}`$ evaluation using $`\Delta_{\mathrm{famrel}}`$ and $`Q_{\mathrm{real}}`$.
5. **M2b — historical supervision.** Historical and performance adequacy gates, $`\mathrm{B2}_{\mathrm{main}}`$–EISE matching, common initialisation, and external evaluation.
6. **Reproducibility and reporting.** Recording sources, annotations, initial weights, checks, protocol versions, and statistical uncertainty.

Independent musicological assessment in M3a provides the reference for formula boundaries and families. M4-min supplies the performance criterion when confirmatory M2b is activated. Empirical evaluation on real data will examine the performance and limitations of these comparisons.

## 12. What the revised M2 design contributes

M2 connects formula recognition to learning the relationships that structure variation. M2a estimates the contribution of family supervision alongside preservation of realisation-specific characteristics. M2b examines the contribution of historically documented identity of a particular passage to representations of variation and to agreement with an independent performance criterion.

The methodological contribution lies in combining a musicologically documented source of supervision with clearly separated symbolic baselines, a shared neural architecture, controlled initialisation, segmental learning from incomplete annotations, and independent statistical evaluation. The historical relationship becomes a controlled experimental variable whose additional information can be assessed in the domain supported by the evidence.

**Documentation and versioning.** [Chapter 6](../../../docs/full/06-eise.md) and [Appendices E](../../../docs/appendices/e.md), [F](../../../docs/appendices/f.md), and [G](../../../docs/appendices/g.md) retain the earlier extended treatment. This page sets out the revised methodological decision. Full technical harmonisation of the active mathematical sources, protocol Γ2–Γ8, and final implementation remains a separate stage.

[Home](../../README.md) · [Revised M1](m1-selection-decision.md) · [Method map](../current/index.md) · [Sources and versions](../reference.md)

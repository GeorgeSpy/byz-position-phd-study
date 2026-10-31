# M1 — Evolution of the representation design and the selection criterion $R^\star$

**Methodological design note · mathematical formulation and synthetic design-sensitivity analysis · 31 October 2026**

> **Status:** Finalized specification of selection rule J. Its application to annotated data, the final construction of the musicological reference annotations, and the calibration of statistical coverage belong to work packages PE0/PE1. The numerical tables below report synthetic design simulations.
>
> **Related material:** [M1 analytical chapter (Greek)](../../../docs/full/05-m1.md) · [Research core](../../README.md) · [Greek version of this note](../../../docs/research/m1-selection-decision.md).

## Summary

Study M1 examines how symbolic representation affects the joint segmentation and family recognition of Byzantine melodic formulae (*theseis*). The design retains twelve input conditions, evaluated against a common sequence of atomic melodic events. Representation selection is tied to a precisely defined task: recognizing **a complete formula occurrence with its correct family identity** using architecture A, which also supplies the shared segmental infrastructure for the subsequent studies.

The methodological development considered three successive rules: **O**, prioritizing boundary F1; **N**, averaging full-recognition F1 across architectures A/B/C; and **J**, evaluating full recognition under the prespecified architecture A subject to a separate family-adequacy requirement. Synthetic studies investigated the mechanisms through which the rules select different representations. The final specification is:

$$
\widehat J(R)=\frac{1}{n_{\mathrm{rep}}}\sum_{r=1}^{n_{\mathrm{rep}}} F_{1,\mathrm{seg+fam}}^{(r)}(R,A),
$$

$$
\widehat{\mathcal A}_{\mathrm{dec}}=\{R\in U\times\Phi:\widehat G_A(R)\ge g_{\min}\},
\qquad
R^\star=\underset{R\in\widehat{\mathcal A}_{\mathrm{dec}}}{\arg\max}\,\widehat J(R).
$$

Here $\widehat G_A$ is macro-averaged recall across known families on externally specified segments, and $g_{\min}$ is established through a specialist assessment and a pilot reference model before comparing the twelve representations. One operational $R^\star$ is accompanied by a separate statistical uncertainty set $\mathcal R^\star$ and at most one prespecified sensitivity representation $R_{\mathrm{sens}}$. Architectures B and C remain independent comparators across the entire grid.

The development is supported by three complementary **synthetic design-sensitivity studies**: A addresses the operational decision and statistical uncertainty; B examines the coupling of detection and family labeling; and C examines complete segments across all twelve representations. A separate algorithmic analysis then checks the validity of alternative segmentation analyses.

## 1. Research questions underlying the design

A melodic formula is modeled as a variable-length segment with a family identity. The computational task jointly addresses the detection of its start and end, the discrimination of related realizations, and the preservation of musicologically substantiated distinctions between families. Representations are evaluated in **continuous musical material**, where formula boundaries may differ from syllable, word, or individual notation-symbol boundaries.

M1 addresses three connected questions:

1. How does the symbolic input unit affect formula recognition?
2. What additional notational, temporal, modal, and textual features contribute to the joint task?
3. Which representation provides a reproducible, prespecified input for A2 and M2 without multiplying the principal historical comparisons?

The third requirement connects M1 representation selection with the historical contrast

$$
\Delta_{\mathrm{hist}}=S_{\mathrm{EISE}}-S_{\mathrm{B2}}.
$$

B2 and EISE are compared under a fixed input representation, a shared segmental mechanism, and matched protocols. Their supervision source is the variable investigated by the main historical experiment.

## 2. Representation grid: input units and cumulative feature layers

The candidate space is

$$
\mathcal R=U\times\Phi,\qquad |U|=3,\quad |\Phi|=4,\quad |\mathcal R|=12.
$$

Earlier material denoted the feature set by `F`; the current repository reader uses **`Φ`**, reserving **`F`** for a family of formulae. This is a change in notation; the twelve conditions remain identical.

| Factor | Levels | Research purpose |
| --- | --- | --- |
| Input unit `U` | `u1`: graphic sign · `u2`: atomic melodic event · `u3`: composite neumatic unit formed by a fixed grouping rule | Compares the information content and structural granularity of the input. |
| Feature set `Φ` | `N` · `N+T` · `N+T+M` · `N+T+M+L` | Measures the successive inclusion of temporal (`T`), modal (`M`), and textual/prosodic (`L`) information in the baseline notational/melodic description `N`. |

The **u3** unit is defined by a prespecified grouping rule independent of family labels and model predictions. The shared output space is the atomic event sequence: even when larger units are used as input, candidate boundaries are projected onto the same atomic coordinates. The protocol therefore checks this projection explicitly, together with grouping reproducibility and retention of permitted information.

The four feature sets form a **cumulative sequence**. Each adjacent comparison estimates the incremental contribution of a particular layer within the existing input context. The design tests successive additions, interpreting each contrast conditional on the features already present. The initial sensitivity analysis retained the **twelve** main conditions. A full factorial extension or an additional syllabic input unit can be explored diagnostically while preserving the main design. [Detailed M1 discussion (Greek)](../../../docs/full/05-m1.md).

The comparison also checks indirect information leakage: the identifier of a sign or composite unit could reveal a feature supposedly removed from a condition. Model capacity, repetitions, hyperparameter budgets, and data partitions are kept comparable.

## 3. Timeline of the methodological decision

The progression of the selection criterion reflects a refinement of the target task: from boundary detection to joint boundary-and-family recognition, and finally to selecting the input representation used by the principal architecture. The dates refer to successive design formulations and studies.

| Period | Stage | Methodological development |
| --- | --- | --- |
| Through analytical draft v8.68i | Initial selection | Priority to boundary F1 and simultaneous statistical superiority as a condition for identifying a single input. When the candidates could not be distinguished, several representations were to be carried into M2. |
| **7 October 2026** | **Simulation Study A** | Adoption of one operational choice by constrained argmax, a separate uncertainty set, and at most one sensitivity analysis; examination of family adequacy and non-inferiority conditions. |
| October 2026, analytical draft v8.71e | Rule **O** | Boundary micro-F1 as the primary endpoint, family criterion $G$, simultaneous uncertainty region, and separate reporting of family-performance loss. |
| 22–26 October 2026 | Intermediate core drafts | Greater emphasis on the shared semi-Markov architecture and complete-formula evaluation, while retaining the earlier selection criterion. |
| **30 October 2026** | Rule **N** | Introduction of the three architectures A/B/C and their mean full-formula F1 as the selection objective, subject to family adequacy in all three. |
| **31 October 2026** | **Simulation Studies B and C** | Systematic examination of representation–architecture interactions, detection–label dependence, and limited independent-group counts; formulation of rule **J**. |
| **31 October 2026** | Algorithmic and statistical verification | Definition of admissible complete boundary pairs $B_x$, compatible matching, verification of $\mathcal R^\star$, treatment of families absent from bootstrap resamples, and alignment of architecture A across A2/M2. |

Earlier versions retain their role in tracing the decision. The active specification is given in §§9–11 and is to be incorporated into the main proposal during the next consolidation of the source documents.

## 4. Three selection rules and their estimands

### 4.1 Rule O — priority to segmentation boundaries

$$
R_O^\star=\underset{R:\widehat G_{e_0}(R)\ge g_{\min}}{\arg\max}\widehat M_{\mathrm{bnd}}(R,e_0).
$$

$M_{\mathrm{bnd}}$ is boundary micro-F1, with the prespecified tolerance where applicable, and $G$ is macro recall of known families on externally delimited occurrences. In the initial specification, the common estimator $e_0$ was to be defined in a later stage; the final design sets $e_0=A$ explicitly. Rule O directly evaluates segmentation accuracy. It measures boundary correctness, with complete recognition reported separately.

### 4.2 Rule N — mean performance across A/B/C

$$
R_N^\star=\underset{R:\min_{a\in\{A,B,C\}}\widehat{\mathrm{Rec}}_{\mathrm{fam}}(R,a)\ge r_{\min}}{\arg\max}\frac{1}{3}\sum_{a\in\{A,B,C\}}\widehat F_{1,\mathrm{seg+fam}}(R,a).
$$

Rule N measures average complete-formula recognition across three architectures. It is a coherent objective when equal transferability of the representation across A/B/C is intended. In this research design, B/C are **comparators**, whereas A2/M2 use A. Selection based on the A/B/C mean can consequently diverge from the representation best suited to the main architecture. The minimum criterion also requires adequate performance from B/C and was additionally underspecified as to whether recall was measured on known or predicted boundaries.

### 4.3 Rule J — complete recognition under A

Rule J retains the constrained argmax and the family threshold of O, while adopting the primary endpoint of complete recognition:

$$
R_J^\star=\underset{R:\widehat G_A(R)\ge g_{\min}}{\arg\max}\widehat F_{1,\mathrm{seg+fam}}(R,A).
$$

This combination defines one operational input for A2/M2. The architectural comparison is conducted independently over all representations. Architecture A remains the shared segmental infrastructure for A2/M2, while B/C serve as dedicated comparators.

| Property | O | N | J |
| --- | --- | --- | --- |
| Primary metric | F1 of individual boundaries | Mean complete-formula F1 across A/B/C | Complete-formula F1 under A |
| Family adequacy | Macro G from one estimator | Minimum across A/B/C | Macro G under A |
| Role of B/C | Additional architectural comparison | Also influence representation selection | Independent comparators for all representations |
| Input to principal M2 | One representation | One representation | One representation |
| Alignment with the joint task under A | Indirect | Through an average | Direct |

## 5. Numerical counterexamples motivating the endpoint

The following examples are **mathematically constructed** to isolate particular selection mechanisms. Their numerical values illustrate those mechanisms; actual performance will be estimated on annotated data.

### 5.1 Correct boundaries and correct complete segments may rank representations differently

Consider 100 reference occurrences, 100 predicted segments, and correct family labels, with two alternative predictions:

| Representation | Both boundaries correct | Only one boundary correct | Neither boundary correct | Boundary F1 | Joint segment-family F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| R1 | 80 | 20 | 0 | **0.90** | 0.80 |
| R2 | 85 | 0 | 15 | 0.85 | **0.85** |

O selects R1, whereas J selects R2. The reversal occurs even with exact boundaries and a shared family filter. Joint F1 measures completion of the full task defined in M1.

### 5.2 Averaging A/B/C may disadvantage the primary architecture A

| Representation | A | B | C | Mean A/B/C |
| --- | ---: | ---: | ---: | ---: |
| R1 | **0.92** | 0.60 | 0.60 | 0.707 |
| R2 | 0.85 | 0.85 | 0.85 | **0.850** |

With adequate G under both representations, N selects R2. Performance under A is then 0.07 below the available R1. J selects R1. The example highlights the representation–architecture interaction `R × a`, which is itself the subject of the separate architectural comparison.

### 5.3 The minimum condition transfers weak B/C performance to A

If macro family recall for one representation is `(A, B, C) = (0.90, 0.60, 0.60)` and the threshold is `0.70`, N excludes that representation even though A meets the requirement. If all candidate representations show similar weakness under B/C, N may produce an empty admissible set. J measures family adequacy in architecture A, which is the architecture retained for subsequent studies.

### 5.4 Joint recognition depends on the coincidence of correct boundaries and labels

A case was examined with two representations exhibiting high boundary performance and high G, but different **associations between successful detection and correct family labeling on the same occurrences**. In case O-b, R1 yields boundary F1 `0.905` and joint F1 `0.478`, while R2 yields boundary F1 `0.853` and joint F1 `0.558`. Family recall on known boundaries is `0.800` and `0.779`, respectively. The complete-recognition endpoint captures the concurrence of the two successes within the same occurrence, as demonstrated by the example.

## 6. Simulation Study A: selection policy and statistical uncertainty set (7 October 2026)

The first study evaluated decision policies on a grid of twelve representations using synthetic marginal scores for boundaries and family recall. Its central aim was to determine how to choose **one operational representation** when several candidates show statistically similar performance.

The protocol distinguished (a) operational selection through a point-estimate admissibility criterion and maximization of the primary endpoint, (b) construction of the uncertainty set $\mathcal R^\star$ representing statistically compatible population optima, and (c) execution of the main historical comparison at one $R^\star$, with at most one additional representation for descriptive sensitivity analysis.

The simulation covered **148 parameter configurations** and seven primary scenarios. Under synthetic settings with a moderate number of independent groups, requiring a certified lower bound $L_G(R)\ge g_{\min}$ for admissibility often produced an empty set. For example, in a specific setting with 16 groups and threshold `0.70`, the probability of an empty $\widehat{\mathcal A}^{-}$ was approximately `0.673`. Operational selection therefore uses the point-estimate criterion $\widehat G(R)\ge g_{\min}$, while the simultaneous uncertainty region is evaluated separately.

The direction of the statistical non-inferiority condition was also examined. For a difference of `-0.10`, standard error `0.05`, and multiplier `1.645`, the **lower** bound is `-0.18225`. Certifying non-inferiority against a margin of `0.04` requires a lower bound of at least `-0.04`. Operational selection and non-inferiority certification have distinct roles in the protocol.

Study A generated **marginal counts**. It did not include the joint event comprising both boundaries and the family label for each occurrence, nor did it model A/B/C. The next two synthetic studies were therefore developed to examine complete recognition and architecture interactions. The size of $\mathcal R^\star$ is treated as a scenario-dependent random outcome, without a universal prespecified range.

## 7. Simulation Study B: occurrence-level modeling and detection–family coupling

The second study used a synthetic generator operating at the **occurrence level**. For each family, representation, and architecture, it simulated complete-segment detection and correct family labeling, permitting positive or negative dependence within the Fréchet bounds. The design included $R\times a$ interactions and shared random effects for work–source groups.

Four representative representations, three architectures, eight families, 16 groups, and approximately 290 occurrences per synthetic sample were used. The comparison comprised **2,000 Monte Carlo repetitions**. The population reference was the best eligible representation according to complete-segment and correct-family F1 under A. $P(\text{target})$ denotes the probability of selecting that representation, while the *expected loss* (*regret*) is the shortfall from the population optimum for the same endpoint.

| Scenario | O: probability / loss | N: probability / loss | J: probability / loss | Mechanism examined |
| --- | --- | --- | --- | --- |
| S1 | `0.452 / 0.012` | **`0.612 / 0.007`** | `0.496 / 0.011` | Shared ranking of representations across A/B/C: averaging reduces variance. |
| S2 | `0.692 / 0.015` | `0.000 / 0.062` | **`0.744 / 0.012`** | Representation–architecture interaction: selecting by the A/B/C mean diverges from the best input for A. |
| S3 | `0.006 / 0.178` | `0.336 / 0.001` | `0.347 / 0.001` | Near-miss boundaries and negative detection–label dependence: segmentation alone favors poorer complete recognition. |
| S4 | `0.742 / 0.017` | `0.618 / 0.025` | **`0.803 / 0.013`** | Performance near the family-adequacy threshold: taking the minimum across A/B/C increases the risk of excluding a suitable input. |

In S1, the A/B/C average reduces selection noise. In S2, differing architecture behavior changes representation rankings, favoring direct evaluation under A. S3 demonstrates the role of detection–label dependence in complete recognition. Together, the four cases provide targeted tests of the selection rules under specified synthetic assumptions.

## 8. Simulation Study C: complete segments across twelve representations

The third study extends synthetic generation to **complete segments**, with start–end coordinates, family predictions, and admissible pairs $B_x$. It covers all twelve $U\times\Phi$ representations in eight scenarios S0–S7, with **100 Monte Carlo repetitions per scenario** and **199 bootstrap resamples** per synthetic dataset. The common evaluation endpoint is population complete-formula-and-family F1 under A, estimated from a large independent synthetic reference sample.

| Scenario | Mechanism | O under A | N | J |
| --- | --- | ---: | ---: | ---: |
| S0 | One clearly superior representation | 0.7936 | 0.7936 | 0.7936 |
| S1 | Reversal between boundary quality and exact complete segments | 0.2808 | 0.5961 | 0.5961 |
| S2 | Rare families and unequal occurrence frequencies | 0.6269 | 0.6269 | 0.6269 |
| S3 | Representation–architecture interaction | 0.7183 | 0.5347 | 0.7183 |
| S4 | Adequate A but weaker B/C | 0.7227 | empty admissible set | 0.7227 |
| S5 | Six nearly tied representations | 0.5883 | 0.5881 | 0.5880 |
| S6 | Six independent groups with strong within-group correlation | 0.4874 | **0.4899** | 0.4794 |
| S7 | Best boundaries and best complete segments occur under different representations | 0.5590 | 0.6364 | 0.6364 |

S1 and S7 motivate a primary metric defined on complete segments. S3 and S4 examine the consequences of averaging across A/B/C and imposing N's stricter family-adequacy condition. In S6, N achieves the highest expected performance under the common target: aggregating three architectures reduces selection noise when few independent groups are available.

Specifically, S6 yielded empirical coverage of the simultaneous region of **0.67 for J**, **0.81 for N**, and **0.73 for O**, against a nominal level of $0.95$. Assessing resampling adequacy is therefore a separate PE1 task. In S5, where six representations have very similar performance, the uncertainty set contains roughly six candidates on average, while only one operational representation is selected for subsequent analyses.

The generator produces controlled synthetic outputs and dependence structures. Empirical evaluation will measure the same quantities on real annotated works and sources, including evidence of family identity, relational historical supervision, and the independent A2/M2 criteria.

## 9. Evaluation specification: complete boundary pairs, families, and admissible analyses

### 9.1 The set of admissible boundary pairs

Every reference occurrence `x` has a family `f_x` and a fixed, documented set of **complete admissible start–end pairs**:

$$
B_x=\{(s_1,e_1),\ldots,(s_k,e_k)\}.
$$

Starts and ends remain paired: the admissible alternatives `(4,11)` and `(6,13)` do **not** license the additional pair `(4,13)`. A prediction `y` with $(\hat s_y,\hat e_y,\hat f_y)$ is matched correctly to `x` precisely when $(\hat s_y,\hat e_y)\in B_x$ **and** $\hat f_y=f_x$. The additional tolerance for the primary metric is **$\tau=0$**; musicologically accepted alternatives have already been recorded in $B_x$.

The $B_x$ sets are constructed before access to predictions from the compared models. The sources supporting each alternative pair, the independently recorded assessments, and the procedure for resolving disagreements are retained. The tolerance $\tau_b$ is used for diagnostic boundary F1 and a separate tolerant segment F1, without affecting J.

PE0 verifies the $B_x$ sets through inter-annotator agreement and common atomic-event coordinates. Exact F1 and diagnostic tolerance-based F1 using $\tau_b$ are reported side by side to assess small boundary discrepancies.

### 9.2 Maximum-cardinality matching with correct family identity

The primary matching procedure uses **edges jointly compatible in boundaries and family**, one-to-one, maximizing the number of successful matches with deterministic tie-breaking. The earlier geometric matching that ignores the label is retained separately **for diagnostic boundary F1**.

If $P$ is the number of predictions, $X$ is the number of reference occurrences, and $m$ is the maximum number of correct matches, then, for a fixed reference count,

$$
TP=m,\qquad FP=P-m,\qquad FN=X-m,\qquad F_{1,\mathrm{seg+fam}}=\frac{2m}{P+X}.
$$

For corpus-level micro-F1, TP/FP/FN are summed before calculating the ratio. An empty region with $P=X=0$ creates no artificial success in the numerator of corpus-level micro-F1. A fully empty standalone case is handled by a prespecified convention.

**Exhaustively annotated scoring regions.** Representation selection and confirmatory complete-recognition evaluation use prespecified, non-overlapping scoring cores $C$, exhaustively annotated for occurrences under the declared annotation scheme. Each core has fully annotated contextual margins covering the prespecified maximum segment length $L_{\max}$. Predictions and reference occurrences count toward $P$ and $X$, respectively, when they start within $C$; complete boundaries are assessed even when extending into the annotated context. Predictions starting outside $C$ are excluded from its score. A prediction beginning within $C$ that exceeds $L_{\max}$ is recorded as invalid and as a false positive. Partially annotated material remains available for training under the separate partial-supervision objective.

### 9.3 When bipartite matching suffices and when global compatibility optimization is necessary

When the number of reference occurrences is fixed and local segmentation alternatives can coexist independently, maximum **bipartite matching** over family-compatible edges is sufficient. When musicological evidence imposes additional constraints linking neighboring choices, scoring must consider the space of **globally admissible complete analyses** $\mathcal C_{\mathrm{legal}}$. For fixed X, the objective is:

$$
m^\star=\max_{c\in\mathcal C_{\mathrm{legal}}}m(c),\qquad F_1=\frac{2m^\star}{P+X}.
$$

When alternative analyses contain **different numbers of occurrences**, the more general definition applies:

$$
F_{1,\mathrm{seg+fam}}^\star=\max_{c\in\mathcal C_{\mathrm{legal}}}\frac{2m(c)}{P+X(c)}.
$$

The constraint structure determines whether bipartite matching, dynamic programming, or integer programming is sufficient. The general formula with variable `X(c)` requires a separate, prespecified evaluation regime and musicological validation of alternative **occurrences**, beyond alternative boundaries for the same occurrence.

Along the standard non-overlapping semi-CRF decoding path, predicted segments do not overlap. Examples with overlapping predictions test the evaluator's response to outputs invalid under that standard semi-CRF path, providing input-validation cases. **Non-overlapping** predictions can also coexist with coupled reference alternatives, in which case global compatibility remains necessary.

## 10. Family adequacy and statistical uncertainty

### 10.1 Known boundaries and known families

$G_A(R)$ is macro recall across known families **on complete gold-reference segments**, with forced-choice labeling from the common vocabulary of known families. Abstention and unknown-family output are disabled for this test so that representation-specific rejection thresholds do not change the admissibility criterion. Open-set recognition, abstention, coverage, and calibration are evaluated separately in the studies where they are targets.

$$
\widehat G_A(R)=\frac{1}{n_{\mathrm{rep}}}\sum_{r=1}^{n_{\mathrm{rep}}}\frac{1}{|\mathcal F|}\sum_{f\in\mathcal F}\frac{TP_{f,r}^{\mathrm{gold}}(R,A)}{n_f}.
$$

**Alternative gold segments for $G_A$.** For every occurrence $x$ with multiple admissible pairs in $B_x$, the primary family-adequacy test uses one musicologically prespecified pair $b_x^0\in B_x$. All selected pairs jointly form a globally admissible analysis and are finalized before examining model predictions. Each occurrence contributes weight one to family recall. A separate sensitivity analysis considers other admissible boundaries using prespecified aggregation with total weight one per occurrence.

**Pilot threshold.** The two specialists record their assessments independently. Pilot medoid performance is measured on groups separate from those used for the main representation ranking and external evaluation, with a common known-family vocabulary and documented uncertainty.

$g_{\min}$ is determined before ranking from independent expert assessments and a pilot medoid model:

$$
g_{\min}=\max\{g_{\mathrm{use}},\widehat G_0^{\mathrm{pilot}}+\delta_{\mathrm{use}}\}.
$$

An empty admissible set triggers the specified re-examination of corpus and annotation readiness. Exact ties are resolved by fewer additional feature layers, followed by a fixed, prespecified order of input units U.

### 10.2 One operational representation and one uncertainty set

Only one representation is operationally selected. The simultaneous statistical region uses **66** pairwise J differences among the twelve representations and **12** G values, for **78** jointly covered quantities. With `L` and `U` denoting lower and upper bounds, define:

$$
\widehat{\mathcal A}^{-}=\{R:L_G(R)\ge g_{\min}\},\qquad
\widehat{\mathcal A}^{+}=\{R:U_G(R)\ge g_{\min}\},
$$

$$
\mathcal R^\star=\left\{R\in\widehat{\mathcal A}^{+}:L_{iR}\le0\quad\text{for every }i\in\widehat{\mathcal A}^{-}\setminus\{R\}\right\}.
$$

$L_{iR}$ is the lower bound for $J(R_i)-J(R)$. If $\widehat{\mathcal A}^{-}$ is empty, the uncertainty set equals $\widehat{\mathcal A}^{+}$. Provided the simultaneous region covers the population quantities, every truly admissible population optimum belongs to $\mathcal R^\star$. This theoretical property depends on the **actual joint coverage** achieved by the computational procedure.

Sensitivity analysis selects at most **one** $R_{\mathrm{sens}}$ among admissible members of the uncertainty set, preferably with a different U and then a higher J. It is descriptive; the primary $\Delta_{\mathrm{hist}}$ is calculated using the unique $R^\star$. The family-performance loss $\Delta_G^{\mathrm{loss}}$ is also reported.

### 10.3 Bootstrap with a small number of independent groups

The unit of independence is the prespecified work–source group, with common draws across representations and training initializations. Resampling retains the pairing structure across the entire grid. The short proposal specifies **five shared training initializations**; any increase is decided and fixed before the main ranking.

If a bootstrap draw has $n_f^{(b)}=0$ for any family, its recall is **undefined** in that draw. The draw is flagged as unsuitable for the simultaneous region involving $G_A$: recall is neither replaced by zero nor recalculated on a reduced family set. PE1 records missing-family frequency and the number of independent groups per family, and tests alternative resampling schemes for coverage of the same population estimand. Resampling conditioned on every family being present requires separate calibration. If coverage is inadequate or missing-family draws occur too often, the conservative fallback reports **the whole grid as the uncertainty set**, retaining one operational $R^\star$. PE1 prespecifies activation criteria (for example, coverage below `0.90` against nominal `0.95`, or missing-family draws above `5%`) and Monte Carlo precision for estimated coverage. This fallback concerns the selection set and does not automatically establish coverage of individual intervals.

Nested group-wise evaluation repeats training, tuning, and selection within each external validation fold, thereby measuring **generalization of the selection procedure**. The final single representation is then selected on the full development corpus and fixed before independent A2/M2 evaluation. Closed historical and performance-based cases do not enter representation selection.

## 11. Architectural comparisons and continuity from M1 to A2 and M2

M1 retains **36 architecture–representation conditions** (`12 representations × 3 architectures`), before training repetitions and any shared classifier adjustments. A/B/C provide an independent test of how joint family information influences segmentation.

The primary architectural contrast compares A against C, averaged across all representations:

$$
\Delta_{A-C}=\frac{1}{12}\sum_{R\in U\times\Phi}\left[F_{1,\mathrm{seg+fam}}(R,A)-F_{1,\mathrm{seg+fam}}(R,C)\right].
$$

It is accompanied by $\Delta_{A-B}$ and a separate boundary-F1 contrast $\Delta_{A-C}^{\mathrm{bnd}}$. Joint resampling operates on the **complete paired profile** for each group because the twelve contrasts share works and random initializations.

B/C results at the selected $R^\star$ are descriptive because the representation was selected using A's performance. The primary architecture comparison uses the entire grid.

For A2, A's baseline segment score remains the reference. In M2, **$B0=A(R^\star)$**, while B1/B2/EISE are compared using the same input and compatible shared segmental infrastructure. The earlier analytical draft allowed **replacing A with B/C at a later stage** if practical equivalence was found; this belongs to an earlier design decision. The final specification retains A as the common infrastructure and B/C as comparators.

$G$ isolates family discrimination with known boundaries. By contrast, M5-min operates on complete works with predicted boundaries, open-set recognition, and possible abstention. The corresponding metrics are reported separately.

## 12. Reproducibility and technical evidence

### 12.1 Registry of synthetic studies

Each synthetic study has a separate code-and-results package. The table records the **exact SHA-256 hashes** of the original archives, reverified when preparing this note. The filenames in the first column are proposed publication names. Changing only the external archive filename leaves its digital fingerprint unchanged.

| Study and proposed archive | Contents | SHA-256 |
| --- | --- | --- |
| **A** — `m1_sim_marginal_gate.zip` | Marginal model, 148 settings, seven principal scenarios, checks of decision regions | `12129537468fb7e8280b615c4f7adf8cdfe6764b5727b7ccfb9d239bf8e076df` |
| **B** — `m1_sim_occurrence_4R.zip` | Occurrence generator, numerical examples, scenarios S1–S4 | `346d5828f157aac444d8fbfc9ede90eef1af9ed45a8b51355f16592e75b87e4e` |
| **C** — `m1_sim_segment_12R.zip` | Complete segment generator, scenarios S0–S7, CSV results, and checks | `55b9ee74ae305dda289fcec7c5cf9e04e4e59007a3fc0219ed9208a0ee0c84a6` |

Publication of the reproducibility packages is conditional on a final review of their contents and metadata. If internal files are edited or the packages are repackaged, new digital fingerprints will be computed and the table updated for the published artifacts. Until then, the filenames identify **proposed archives**, not live repository download links.

### 12.2 Reproduction checks and interpretation of results

The synthetic-study deliverables record reruns of the historical model, numerical checks, and verification of the segment-level metric. The following small checks have also been rerun in the available working environment:

- **12/12** successful segment-simulation tests (match counts, $B_x$, families, ties, and basic statistical constructions).
- Successful execution of the marginal-methodology tests and the historical reference program.
- **8/8** successful numerical matching checks for small explicitly specified cases.

These executions test the correctness of particular calculations. The simulations are sensitivity analyses of the **design**: synthetic performances derive from specified generation mechanisms, and the main scientific hypotheses are evaluated on the real M1, A2, and M2 data.

### 12.3 Minimal suite of matching tests

| ID | Test case | Expected result |
| --- | --- | --- |
| T1 | Prediction `(4,13)` for $B_x=\{(4,11),(6,13)\}$ | Reject recombined, non-admissible boundary pair. |
| T2 | A one-event boundary shift outside $B_x$ | Failure under the primary metric with $\tau=0$. |
| T3 | Admissible boundary pair with incorrect family label | Count the prediction as FP and the corresponding reference occurrence as FN. |
| T4 | Reversing the order of two competing predictions | Identical maximum number of successful matches. |
| T5 | Mutually incompatible alternative boundaries for neighboring occurrences | Select from globally admissible analyses. |
| T6 | Overlapping segments produced by a non-overlapping decoder | Validate the output and handle invalid predictions explicitly. |
| T7 | Coupled reference choices without overlap among predictions | Enforce additional compatibility constraints. |
| T8 | Alternative analyses with different occurrence counts | Maximize F1 with the relevant denominator $P+X(c)$. |

The complete evaluator implementation will be checked against a small exhaustive reference program enumerating legal analyses, with T1–T8 included in automated testing.

## 13. Parameter finalization and PE0/PE1 checks

PE0/PE1 specify the implementation of rule J through the following deliverables:

1. **Musicological reference annotation.** Document occurrences, gather independent specialist assessments, finalize $B_x$ sets, choose one globally compatible reference pair per occurrence for $G_A$, define relations $\mathcal C_{\mathrm{legal}}$, and prespecify exhaustively annotated scoring cores with context margins.
2. **Shared representation and decoding.** Verify the projection of $u_1/u_3$ onto atomic events, maintain a common output schema, and implement matching with tests T1–T8.
3. **Family adequacy.** Record independent assessments from two specialists and evaluate the medoid model on an appropriate pilot corpus to predetermine $g_{\mathrm{use}}$, $\delta_{\mathrm{use}}$, and $g_{\min}$.
4. **Statistical calibration.** Assess independent work–source groups, the number of shared initializations, resampling frequency with $n_f^{(b)}=0$, simultaneous coverage of the 78-dimensional region, and conservative procedures when coverage is inadequate.
5. **Data separation and generalization.** Use nested group-wise cross-validation, finalize one $R^\star$ on the complete development material, and evaluate A2/M2 independently, without allowing closed test sets to influence representation selection.

Rule J remains common to all applications. These procedures specify its parameters, reference annotation quality, and empirical reliability requirements.

**Editorial integration of the specification.** Aligning the short proposal with analytical §§5.4, 6.1, E.1, E.3, G.5.1, and J.4 is a current task in finalizing the research text: the consolidated version will use the same J criterion, distinguish primary and diagnostic metrics, and retain architecture A throughout A2/M2.

## 14. Conclusion

Study M1 establishes an integrated framework for choosing symbolic representations for Byzantine melodic formulae. The $U\times\Phi$ grid examines the role of input granularity and additional feature layers. Rule J evaluates recognition of a complete formula with the correct family identity under prespecified architecture A. The criterion $G_A\ge g_{\min}$ ensures a minimum level of family adequacy on known boundaries, while the simultaneous uncertainty region captures statistically compatible candidate optima.

Synthetic Studies A, B, and C identify mechanisms affecting selection among O, N, and J. The independent A/B/C comparison continues to test joint learning of boundaries and family identity. With one operational $R^\star$, A2 and M2 can estimate their own contrasts on comparable input and shared segmental infrastructure.

The final empirical assessment will evaluate generalization and statistical stability on independent works and sources under the criteria specified in PE0/PE1.

# M1 — Revision of the representation design and selection criterion $`R^\star`$

**Methodological documentation · 31 October 2026**

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/research/m1-selection-decision.md) · **English**
<!-- language-switch:end -->

> **Status:** Finalised specification of selection rule J. Application to annotated data, final construction of the musicological reference, and calibration of statistical coverage are scheduled for WP0/WP1. The numerical tables below report synthetic design simulations.
>
> **Related documents:** [Detailed M1 chapter (Greek)](../../../docs/full/05-m1.md) · [M1-X extension](m1-x-design.md) · [Core research programme](../../README.md) · [Source history (Greek)](../../../docs/maintenance/source-history.md) · [Research decision log (Greek)](../../../docs/review/decisions.md).

## 1. Why the M1 design was revised

M1 investigates how the symbolic representation of Byzantine chant affects the localisation and recognition of melodic formulae in continuous works. The initial design prioritised boundary accuracy. Further development of the protocol revealed a central requirement: recognising a formula in full entails identifying both its start and end boundaries and the family to which it belongs. This combination now provides the principal criterion for representation selection.

A melodic formula is treated as a variable-length segment with a family identity. Its boundaries may differ from those of a syllable, word, or notational symbol, while related realisations may differ substantially in their surface form. M1 therefore jointly examines the choice of symbolic input unit, the additional information provided by notational, temporal, modal, and textual features, and recognition on previously unseen works and sources. The design retains twelve input conditions mapped to a common sequence of atomic melodic events, so that all comparisons address the same computational task.

The revision progressed from rule **O**, which prioritised boundary F1, to **N**, which averaged complete-recognition F1 over architectures A/B/C, and finally to **J**. Rule J selects the representation according to recognition of an entire formula with the correct family in the prespecified architecture A, subject to a separate family-adequacy requirement. Its final specification is:

```math
\widehat J(R)=\frac{1}{n_{\mathrm{rep}}}\sum_{r=1}^{n_{\mathrm{rep}}} F_{1,\mathrm{seg+fam}}^{(r)}(R,A),
```

```math
\widehat{\mathcal A}_{\mathrm{dec}}=\{R\in U\times\Phi:\widehat G_A(R)\ge g_{\min}\},
\qquad
R^\star=\underset{R\in\widehat{\mathcal A}_{\mathrm{dec}}}{\arg\max}\,\widehat J(R).
```

$`\widehat G_A`$ measures macro-averaged recall across known families on documented boundaries. The threshold $`g_{\min}`$ is set through a specialist procedure and a pilot reference model before the twelve representations are compared. The operational choice of a single $`R^\star`$ is accompanied by a separate statistical uncertainty set $`\mathcal R^\star`$ and at most one sensitivity representation $`R_{\mathrm{sens}}`$. Architectures B/C are evaluated independently across the complete grid, keeping input selection tied to the principal architecture.

The same representation is subsequently used in A2 and M2, allowing the contribution of musicological knowledge and relational supervision to be examined on a fixed input. In M2's historical comparison, the primary contrast is:

```math
\Delta_{\mathrm{hist}}=S_{\mathrm{EISE}}-S_{\mathrm{B2}_{\mathrm{main}}}.
```

$`\mathrm{B2}_{\mathrm{main}}`$ and EISE share segmental infrastructure and a matched protocol. Their comparison investigates what the documented exegetical relationship of the same passage contributes to an independent performance-based criterion.

The choice of J is developed below through numerical counterexamples, three complementary synthetic sensitivity studies, and separate algorithmic and statistical checks. The discussion follows the reasoning from candidate representations and selection rules to the final evaluation protocol.

## 2. The representation grid: input units and successive feature layers

The candidate representation space is:

```math
\mathcal R=U\times\Phi,\qquad |U|=3,\quad |\Phi|=4,\quad |\mathcal R|=12.
```

Earlier documentation denoted the feature set by F. The current research reader uses **$`\Phi`$** for the feature axis and reserves **F** for a formula family. This changes the notation while retaining all twelve experimental conditions.

| Factor | Levels | Research purpose |
| --- | --- | --- |
| Input unit U | u1: notational symbol · u2: atomic melodic event · u3: compound neumatic unit with a specified grouping rule | Compares the informational and structural granularity of the input. |
| Feature layers $`\Phi`$ | N · N+T · N+T+M · N+T+M+L | Measures successive contributions of temporal (T), modal (M), and textual/prosodic (L) information beyond the initial notational/melodic description N. |

**u3** is constructed by a prespecified grouping procedure independent of family labels and model predictions. The common output resolution is the atomic event sequence. Even when the input uses larger units, candidate boundaries are projected onto the same atomic coordinates. The projection, reproducibility of grouping, and preservation of permitted information therefore require explicit verification.

The four feature sets form a **cumulative sequence**. Each adjacent comparison estimates the incremental contribution of a particular layer conditional on those already included. The initial sensitivity analysis retained **twelve** main conditions. A full factorial extension or an additional syllabic unit can be examined diagnostically without changing the main design. See the [detailed M1 chapter (Greek)](../../../docs/full/05-m1.md).

The comparison also tests for indirect information leakage: a symbol or compound-unit identifier may reveal features ostensibly removed from an input condition. Model capacity, replicates, hyperparameter-search budgets, and data partitions remain comparable.

## 3. How the methodological decision developed

The changing selection rule reflects a more precise formulation of the research objective: from boundary localisation to joint boundary-and-family recognition, and finally to selection of the representation used by the principal architecture. The dates below refer to successive specifications and design studies.

| Period | Stage | Methodological development |
| --- | --- | --- |
| Up to analytical version v8.68i | Initial selection | Priority given to boundary F1, with a requirement for simultaneous statistical superiority to identify a single representation. Several representations could be carried into M2 when performance was indistinguishable. |
| **7 October 2026** | **Simulation Study A** | One operational choice using a constrained argmax, a separate uncertainty set, and at most one sensitivity analysis; exploration of family-adequacy and non-inferiority criteria. |
| October 2026, analytical version v8.71e | Rule **O** | Boundary micro-F1 as the primary measure, family criterion $`G`$, a simultaneous uncertainty region, and separate reporting of lost family recall. |
| 22–26 October 2026 | Intermediate core drafts | Stronger emphasis on the shared semi-Markov architecture and complete-formula evaluation while retaining the initial selection criterion. |
| **30 October 2026** | Rule **N** | Inclusion of architectures A/B/C and their mean complete-formula F1 in the selection rule, with a family-adequacy requirement for all three. |
| **31 October 2026** | **Simulation Studies B and C** | Examination of representation–architecture interactions, dependence between localisation and labels, and behaviour with few independent groups. Formulation of rule **J**. |
| **31 October 2026** | Algorithmic and statistical validation | Definition of complete admissible boundary pairs $`B_x`$, compatible matching, the uncertainty set $`\mathcal R^\star`$, families absent from bootstrap samples, and the common role of A in A2/M2. |

Earlier versions remain useful for reconstructing how the decision was reached. The operative specification appears in Sections 9–11 and is intended to be carried into the main research proposal as its source documents are harmonised.

## 4. Three selection rules and the quantities they estimate

### 4.1 Rule O — priority to boundary localisation

```math
R_O^\star=\underset{R:\widehat G_{e_0}(R)\ge g_{\min}}{\arg\max}\widehat M_{\mathrm{bnd}}(R,e_0).
```

$`M_{\mathrm{bnd}}`$ is boundary micro-F1, with the prespecified tolerance when applicable; $`G`$ is macro recall over known families in externally bounded occurrences. The common estimator $`e_0`$ was left for a later stage in the initial specification; the final design explicitly sets $`e_0=A`$. Rule O directly targets boundary accuracy. Complete-formula recognition is reported as a separate outcome.

### 4.2 Rule N — mean performance across A/B/C

```math
R_N^\star=\underset{R:\min_{a\in\{A,B,C\}}\widehat{\mathrm{Rec}}_{\mathrm{fam}}(R,a)\ge r_{\min}}{\arg\max}\frac{1}{3}\sum_{a\in\{A,B,C\}}\widehat F_{1,\mathrm{seg+fam}}(R,a).
```

Rule N estimates mean complete-formula recognition across three specified architectures. This is a coherent objective when transferability to A/B/C with equal weighting is the aim. In the present research design, B/C act as **comparators**, while A supplies the shared infrastructure for A2/M2. Selection by the A/B/C average may therefore differ from the input that best serves the main model. The minimum criterion also requires adequacy under B/C and left ambiguity over whether recall was measured at known or predicted boundaries.

### 4.3 Rule J — complete recognition with A

Rule J retains O's constrained argmax and family threshold while using the measure that directly reflects the full recognition task:

```math
R_J^\star=\underset{R:\widehat G_A(R)\ge g_{\min}}{\arg\max}\widehat F_{1,\mathrm{seg+fam}}(R,A).
```

This produces one operational input for A2/M2. Architectural comparisons are carried out separately across all representations. A remains the common segmental model for the downstream studies, while B/C provide independent comparators.

| Property | O | N | J |
| --- | --- | --- | --- |
| Primary measure | F1 of individual boundaries | Mean complete-formula F1 across A/B/C | Complete-formula F1 under A |
| Family-adequacy criterion | Macro G for one estimator | Minimum recall across A/B/C | Macro G under A |
| Role of B/C | Additional architectural comparison | Also influence representation selection | Independent comparators for every R |
| Input to main M2 | One R | One R | One R |
| Alignment with the joint task under A | Indirect | Through an average | Direct |

## 5. Numerical counterexamples that motivated the metric

The following examples are **mathematically constructed** to isolate particular mechanisms. Their numerical values illustrate selection behaviour; actual performance will be estimated from annotated data.

### 5.1 Correct endpoints and fully correct segments can rank representations differently

Consider 100 reference occurrences and 100 predicted segments with correct family labels under two alternative outputs:

| Representation | Both endpoints correct | Only one endpoint correct | Neither endpoint correct | Boundary-F1 | Joint segment-family-F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| R1 | 80 | 20 | 0 | **0.90** | 0.80 |
| R2 | 85 | 0 | 15 | 0.85 | **0.85** |

Rule O selects R1, whereas J selects R2. This reversal occurs even with exact endpoints and the same family filter. Joint F1 measures successful completion of M1's full recognition task.

### 5.2 The A/B/C average can disadvantage the main architecture A

| Representation | A | B | C | Mean A/B/C |
| --- | ---: | ---: | ---: | ---: |
| R1 | **0.92** | 0.60 | 0.60 | 0.707 |
| R2 | 0.85 | 0.85 | 0.85 | **0.850** |

With adequate G for both representations, N selects R2. A then performs 0.07 below the available R1, which J selects. This example isolates the representation–architecture interaction $`R\times a`$, examined separately in the architectural comparison.

### 5.3 The minimum criterion makes A depend on weaknesses in B/C

If macro family recall for a representation is $`(A,B,C)=(0.90,0.60,0.60)`$ with threshold $`0.70`$, N excludes it even though A satisfies the criterion. If all candidate representations show similar weaknesses in B/C, N may produce an empty eligible set. J evaluates family adequacy under A, the architecture used in subsequent studies.

### 5.4 Joint success depends on the alignment of boundaries and family labels

A case study compared two representations with high boundary accuracy and high G but different **dependence between successful localisation and correct labels on the same occurrences**. Under condition O-b, R1 has boundary-F1 0.905 and joint F1 0.478; R2 has boundary-F1 0.853 and joint F1 0.558. Family recall on known boundaries is 0.800 and 0.779, respectively. The complete-recognition criterion captures whether both parts of the task succeed for the same occurrence.

## 6. Simulation Study A: operational selection and the statistical uncertainty set (7 October 2026)

The first study examined the decision rules over a grid of twelve representations using synthetic marginal measures of boundary performance and family recall. Its principal concern was how to choose **one operational representation** when several exhibit statistically similar performance.

The procedure had three distinct levels: (a) operational selection through point-estimate eligibility and maximisation of the primary measure; (b) construction of an uncertainty set $`\mathcal R^\star`$ containing statistically compatible optimal choices; and (c) evaluation of the main historical comparison with one $`R^\star`$, alongside at most one additional representation for descriptive sensitivity analysis.

The simulation covered **148 parameter combinations** and seven principal scenarios. In synthetic settings with a moderate number of independent groups, requiring a certified lower bound $`L_G(R)\ge g_{\min}`$ for eligibility frequently led to an empty set. For example, in a particular setting with sixteen groups and threshold 0.70, the probability that $`\widehat{\mathcal A}^{-}`$ was empty was approximately 0.673. Operational selection therefore retains the point-estimate criterion $`\widehat G(R)\ge g_{\min}`$, while the simultaneous uncertainty region is evaluated separately.

The direction of the statistical non-inferiority criterion was also checked. For a difference of $`-0.10`$, standard error 0.05, and multiplier 1.645, the **lower** confidence bound is $`-0.18225`$. Certifying non-inferiority against a margin of 0.04 requires the lower bound to be at least $`-0.04`$. Operational selection and non-inferiority certification thus serve different purposes in the protocol.

Study A's generator produced **marginal counts**. It did not represent the joint information for both endpoints and the family label of an individual occurrence, or the three architectures A/B/C. Two further synthetic studies were developed to assess complete recognition and representation–architecture interactions. The size of $`\mathcal R^\star`$ is treated as a random outcome of each scenario, with no universally predetermined range.

## 7. Simulation Study B: occurrence-level modelling and localisation–family dependence

The second study used a synthetic generator at the **occurrence level**. For each family, representation, and architecture, success in detecting a complete segment and correctly identifying its family was simulated, allowing positive or negative dependence within the Fréchet bounds. The design included interactions $`R\times a`$ and shared random effects for work–source groups.

The experiment used four representative representations, three architectures, eight families, sixteen groups, and approximately 290 occurrences per synthetic sample. It ran **2,000 Monte Carlo replicates**. The population reference was the best eligible representation according to A's joint segment-and-family F1. $`P(\text{target})`$ denotes the probability of choosing that representation; expected **regret** measures the shortfall from its population-optimal value under the same criterion.

| Scenario | O: selection probability / regret | N: selection probability / regret | J: selection probability / regret | Controlled mechanism |
| --- | --- | --- | --- | --- |
| S1 | 0.452 / 0.012 | **0.612 / 0.007** | 0.496 / 0.011 | Similar rankings across A/B/C; averaging reduces selection variance. |
| S2 | 0.692 / 0.015 | 0.000 / 0.062 | **0.744 / 0.012** | Representation–architecture interaction; the A/B/C average differs from A's best input. |
| S3 | 0.006 / 0.178 | 0.336 / 0.001 | 0.347 / 0.001 | Almost-correct boundaries and negative localisation–label dependence; boundaries alone select weaker complete recognition. |
| S4 | 0.742 / 0.017 | 0.618 / 0.025 | **0.803 / 0.013** | Performance close to the family-adequacy threshold; the A/B/C minimum increases the chance of excluding a suitable input. |

In S1, averaging A/B/C reduces selection noise. In S2, architectural differences change representation rankings and favour direct assessment under A. S3 reveals the effect of localisation–label dependence on complete recognition. The four scenarios provide targeted checks of the selection rules under explicitly defined synthetic assumptions.

## 8. Simulation Study C: complete segments across all twelve representations

The third study extended synthetic generation to **complete segments**, with start–end coordinates, family predictions, and admissible boundary pairs $`B_x`$. It included all twelve representations in $`U\times\Phi`$, eight scenarios S0–S7, **100 Monte Carlo replicates per scenario**, and **199 bootstrap resamples** per synthetic dataset. The shared evaluation criterion was A's population-level F1 for complete segments with correct family labels, estimated from a separate large synthetic reference sample.

| Scenario | Mechanism | O under A | N | J |
| --- | --- | ---: | ---: | ---: |
| S0 | One clearly superior representation | 0.7936 | 0.7936 | 0.7936 |
| S1 | Reversed rankings for correct endpoints and exact complete segments | 0.2808 | 0.5961 | 0.5961 |
| S2 | Rare families and imbalance in occurrence counts | 0.6269 | 0.6269 | 0.6269 |
| S3 | Representation–architecture interaction | 0.7183 | 0.5347 | 0.7183 |
| S4 | Adequate A with weaker B/C | 0.7227 | empty eligible set | 0.7227 |
| S5 | Six near-tied representations | 0.5883 | 0.5881 | 0.5880 |
| S6 | Six independent groups with strong within-group correlation | 0.4874 | **0.4899** | 0.4794 |
| S7 | Best boundary and complete-segment performance arise under different representations | 0.5590 | 0.6364 | 0.6364 |

S1 and S7 highlight the need for a primary metric defined on complete segments. S3 and S4 examine equal-weight A/B/C averaging and N's stricter family-adequacy requirement. In S6, N has the highest expected performance under the common target, because averaging over architectures limits selection noise with few independent groups.

For S6 specifically, empirical coverage of the simultaneous region at nominal 0.95 was **0.67 for J**, **0.81 for N**, and **0.73 for O**. Bootstrap adequacy is therefore a separate concern for WP1. In S5, with six similarly performing representations, the uncertainty set contains approximately six candidates on average, while downstream analysis still uses a single operational choice.

The generator produces controlled synthetic predictions and correlations. Empirical evaluation will measure corresponding quantities on genuinely annotated works and sources, including family-identity evidence, relational historical supervision, and the independent criteria used in A2/M2.

## 9. Evaluation specification: complete boundary pairs, families, and legal analyses

### 9.1 The set of admissible boundary pairs

Each reference occurrence $`x`$ has a family $`f_x`$ and a documented, fixed set of admissible **complete** start–end pairs:

```math
B_x=\{(s_1,e_1),\ldots,(s_k,e_k)\}.
```

Start and end coordinates remain paired: $`(4,11)`$ and $`(6,13)`$ do **not** imply an additional $`(4,13)`$. A prediction $`y`$ with $`(\hat s_y,\hat e_y,\hat f_y)`$ matches $`x`$ correctly only if $`(\hat s_y,\hat e_y)\in B_x`$ **and** $`\hat f_y=f_x`$. The primary metric uses **$`\tau=0`$** additional tolerance. Musicologically admissible boundary alternatives are already specified in $`B_x`$.

The sets $`B_x`$ are constructed before the predictions of the compared models are examined. For each alternative pair, the sources, independent judgements, and disagreement-resolution procedure are retained. Boundary tolerance $`\tau_b`$ is used for diagnostic boundary F1 and a separate tolerant segment-F1; it does not alter J.

### 9.2 Maximum-cardinality matching with correct family labels

The principal evaluation uses **edges that jointly satisfy boundary and family criteria**, with one-to-one maximum-cardinality matching and deterministic tie-breaking. Geometric matching that disregards labels is performed separately **for diagnostic boundary F1**.

Let $`P`$ denote the number of predictions, $`X`$ the number of reference occurrences, and $`m`$ the maximum number of correct matches. For a fixed reference count,

```math
TP=m,\qquad FP=P-m,\qquad FN=X-m,\qquad F_{1,\mathrm{seg+fam}}=\frac{2m}{P+X}.
```

Corpus-wide micro-F1 aggregates TP/FP/FN **before** taking the ratio. An empty region with $`P=X=0`$ contributes no artificial success to the numerator of corpus-level micro-F1. An entirely empty, standalone evaluation case follows a prespecified convention.

### 9.3 When bipartite matching suffices and when global compatibility must be enforced

If the number of reference occurrences is fixed and local boundary alternatives can coexist, maximum **bipartite matching** over admissible, family-consistent edges is sufficient. If musicological evidence links adjacent choices through additional constraints, evaluation must consider the set of **globally legal complete analyses** $`\mathcal C_{\mathrm{legal}}`$. With fixed $`X`$, the objective is:

```math
m^\star=\max_{c\in\mathcal C_{\mathrm{legal}}}m(c),\qquad F_1=\frac{2m^\star}{P+X}.
```

For alternative analyses with **different numbers of reference occurrences**, the more general definition applies:

```math
F_{1,\mathrm{seg+fam}}^\star=\max_{c\in\mathcal C_{\mathrm{legal}}}\frac{2m(c)}{P+X(c)}.
```

The preceding expression describes a standalone evaluation case. **At corpus level**, when alternative legal reference analyses yield different occurrence counts, the compatible analysis is selected jointly over all evaluation cases, maximising a single micro-F1 ratio:

```math
F_{1,\mathrm{seg+fam}}^{\mathrm{corpus}}=
\max_{c\in\mathcal C_{\mathrm{legal}}^{\mathrm{corpus}}}
\frac{2M(c)}{P_{\mathrm{total}}+X(c)}.
```

Here $`M(c)`$ is the total number of correct matches, $`P_{\mathrm{total}}`$ the total number of predictions, and $`X(c)`$ the total number of reference occurrences in the selected globally legal corpus analysis. This rule prevents a separate denominator from being optimised within each individual region.

The constraint structure determines whether bipartite matching, dynamic programming, or integer programming is appropriate. The general expression with variable $`X(c)`$ requires an explicitly prespecified evaluation regime and musicological verification of alternative **occurrences**, beyond alternative boundaries for a single occurrence.

In the main non-overlapping semi-CRF pathway, decoded predictions cannot overlap. Examples involving overlapping predictions test the evaluator's response to outputs prohibited by that decoder and provide input-validity checks. **Non-overlapping** predictions may also require global compatibility when alternative reference analyses are interdependent.

## 10. Family adequacy and statistical uncertainty

### 10.1 Known boundaries and known families

$`G_A(R)`$ denotes macro recall across known families **on complete gold-standard segments**, using forced-choice classification over a common vocabulary of known families. Abstention and unknown-family outputs are disabled for this specific test, so that representation-specific rejection thresholds cannot change eligibility. Open-set recognition, abstention, coverage, and their calibration are evaluated separately where they form part of the task.

```math
\widehat G_A(R)=\frac{1}{n_{\mathrm{rep}}}\sum_{r=1}^{n_{\mathrm{rep}}}\frac{1}{|\mathcal F|}\sum_{f\in\mathcal F}\frac{TP_{f,r}^{\mathrm{gold}}(R,A)}{n_f}.
```

The threshold $`g_{\min}`$ is fixed before ranking, using independent specialist assessments and a pilot medoid:

```math
g_{\min}=\max\{g_{\mathrm{use}},\widehat G_0^{\mathrm{pilot}}+\delta_{\mathrm{use}}\}.
```

An empty eligible set triggers the prespecified review of corpus and annotation readiness. Exact ties are resolved by preferring fewer additional feature layers and then the fixed, prespecified order of input units U.

### 10.2 One operational R and one uncertainty set

Exactly one R is selected for operational use. The simultaneous uncertainty region covers **66** pairwise J differences among the twelve representations and **12** G values: **78** quantities in total. Writing $`L`$ and $`U`$ for lower and upper confidence bounds, define:

```math
\widehat{\mathcal{A}}^{-} = \lbrace R : L_G(R) \ge g_{\min} \rbrace, \qquad \widehat{\mathcal{A}}^{+} = \lbrace R : U_G(R) \ge g_{\min} \rbrace,
```

```math
\mathcal{R}^\star = \lbrace R \in \widehat{\mathcal{A}}^{+} : L_{iR} \le 0 \quad \text{for every } i \in \widehat{\mathcal{A}}^{-} \setminus \lbrace R \rbrace \rbrace.
```

Here $`L_{iR}`$ is the lower bound of the difference $`J(R_i)-J(R)`$. If $`\widehat{\mathcal A}^{-}`$ is empty, the set equals $`\widehat{\mathcal A}^{+}`$. Whenever the simultaneous region covers the underlying population quantities, every truly eligible optimal representation lies in $`\mathcal R^\star`$. This theoretical property depends on the **actual simultaneous coverage** achieved by the estimation procedure.

The sensitivity analysis selects at most **one** $`R_{\mathrm{sens}}`$ from eligible members of the uncertainty set, preferring a different U and then a higher J. This analysis is descriptive; the primary $`\Delta_{\mathrm{hist}}`$ is calculated with the single $`R^\star`$. Lost family recall $`\Delta_G^{\mathrm{loss}}`$ is also reported.

### 10.3 Bootstrap inference with few independent groups

The independent sampling unit is a prespecified work–source group. Each resample is shared across all representations and initialisations, retaining the pairing of the entire grid. The core proposal specifies **five common random initialisations**. Any increase is decided and fixed before the main ranking.

If a bootstrap sample has $`n_f^{(b)}=0`$ for a family, that family's recall is **undefined** in the sample. This event is recorded rather than replaced automatically by zero. Feasibility and simultaneous coverage of the resampling procedure are evaluated in WP0/WP1. If reliability is inadequate, the conservative fallback reports **the entire grid as the uncertainty set**, while retaining a single operational R. A preregistered pilot trigger, such as coverage below 0.90 against a nominal 0.95, is a **warning/readiness criterion**, not proof of nominal coverage.

Nested group-based validation repeats training, tuning, and selection within each outer evaluation fold, measuring **generalisation of the selection procedure**. The final operational R is then selected on the complete development corpus and fixed before independent A2/M2 evaluation. Held-out historical and performance cases play no role in selection.

## 11. Architectural comparisons and continuity from M1 to A2 and M2

M1 includes **36 architecture–representation conditions** (12 R × 3 architectures), before replication and any shared-classifier accounting. A/B/C provide a separate test of how joint family information affects segmentation.

The main architectural contrast compares A with C, averaged across all representations:

```math
\Delta_{A-C}=\frac{1}{12}\sum_{R\in U\times\Phi}\left[F_{1,\mathrm{seg+fam}}(R,A)-F_{1,\mathrm{seg+fam}}(R,C)\right].
```

It is accompanied by $`\Delta_{A-B}`$ and a separate boundary-F1 contrast $`\Delta_{A-C}^{\mathrm{bnd}}`$. Resampling is performed on each group's **complete paired profile**, because the twelve differences share works and random initialisations.

A2 retains the selected architecture A as its common infrastructure. In [M2](m2-eise-research-design.md), A uses the same $`R^\star`$; symbolic recognition is assessed separately using $`\mathrm{B0}_{\mathrm{sym}}`$, and historical performance descriptions using $`\mathrm{B0}_{\mathrm{profile}}`$. B1, B2, and EISE are trained from shared initial weights in each replicate, according to the M2 protocol. The earlier policy of subsequently selecting B or C as the main architecture belongs to a preceding design stage. In the revised protocol, B/C remain independent architectural comparators.

$`G`$ isolates discrimination between families at known boundaries. By contrast, M5-min processes complete works with predicted boundaries, open-set recognition, and possible abstention. Its metrics are reported separately.

### 11.1 · C_fac in the representation grid and the M1-X extension

Architecture **C** in Section 11 is implemented as **C_fac**, a factorised model $`p_C(B,\mathbf f\mid X)=p_B(B\mid X)\prod_{s\in B}p_F(f_s\mid s,X)`$ with a shared trainable encoder, a free boundary-scoring head, and family supervision. It is trained using a joint partial likelihood over the **same sets of compatible complete analyses** as A. In the main M1 study, C obtains its boundary decision from the marginal boundary distribution $`p_B`$ and subsequently assigns a family. Accordingly, the average $`\Delta_{A-C}`$ contrast across the twelve representations refers to the same C_fac comparator used in the complementary M1-X study.

**M1-X** evaluates additional decoding procedures on the **same trained A/C_fac weights**: K-best candidate legal segmentations and global joint MAP decoding. The primary architectural comparison uses the $`R_A^\star`$ representation selected by rule J; selection of $`R_C^\star`$ is analysed separately on development data. The family-neutral condition and the boundary-only trained C_B control assess distinct mechanisms. Architecture A, rule J, and the operational inputs to A2/M2 are preserved.

[Full M1-X protocol](m1-x-design.md) · [Technical specification G.5.1.1 (Greek)](../../../docs/appendices/g.md#r186x).

## 12. Reproducibility and technical evidence

### 12.1 Registry of synthetic studies

Each synthetic study has a separate package of code and results. The table records the **exact SHA-256 hashes** of the original compressed packages, which were rechecked when the Greek methodological document was prepared. File names in the first column are proposed publication names. Renaming an outer file without changing its contents preserves its hash.

| Study and proposed file | Contents | SHA-256 |
| --- | --- | --- |
| **A** — m1_sim_marginal_gate.zip | Marginal model, 148 settings, seven main scenarios, and selection-region checks | 12129537468fb7e8280b615c4f7adf8cdfe6764b5727b7ccfb9d239bf8e076df |
| **B** — m1_sim_occurrence_4R.zip | Occurrence generator, numerical counterexamples, and scenarios S1–S4 | 346d5828f157aac444d8fbfc9ede90eef1af9ed45a8b51355f16592e75b87e4e |
| **C** — m1_sim_segment_12R.zip | Complete segment generator, scenarios S0–S7, CSV results, and tests | 55b9ee74ae305dda289fcec7c5cf9e04e4e59007a3fc0219ed9208a0ee0c84a6 |

Publishing reproducible packages requires a final review of their contents and metadata. If internal files are edited or the archives are repackaged, the hashes must be recalculated and the table updated to match the published artefacts. Until then, these are **proposed file names**, rather than active download links in the repository.

### 12.2 Reproduction checks and interpretation

The synthetic study deliverables document reruns of earlier models, numerical checks, and validation of the segmental metric. The following additional small-scale checks were also rerun in the original working environment:

- **12/12** segmental simulation tests passed, covering match counts, $`B_x`$, families, tie-breaking, and basic statistical constructions.
- The tests for the marginal methodology and the historical reference program completed successfully.
- **8/8** numerical matching checks passed on small, explicitly defined cases.

These executions verify particular computations. The simulations assess the **sensitivity of the design**: synthetic performance values arise from prespecified generative mechanisms, while the main scientific hypotheses are evaluated on real data in M1, A2, and M2.

### 12.3 Minimum matching test suite

| ID | Test case | Expected result |
| --- | --- | --- |
| T1 | Prediction $`(4,13)`$ when $`B_x=\{(4,11),(6,13)\}`$ | Reject the recombined inadmissible pair. |
| T2 | A boundary shifted by one event beyond $`B_x`$ | Failure under the primary metric with $`\tau=0`$. |
| T3 | An admissible boundary pair with an incorrect family | Record the prediction as FP and the corresponding occurrence as FN. |
| T4 | Reverse the order of two competing predictions | Preserve the same maximum number of correct matches. |
| T5 | Incompatible alternative boundaries of adjacent occurrences | Select from globally legal analyses. |
| T6 | Overlapping segments returned by a non-overlapping decoder | Validate the input and explicitly handle the illegal output. |
| T7 | Interdependent reference choices without prediction overlap | Enforce additional compatibility constraints. |
| T8 | Alternative analyses with different occurrence counts | Maximise F1 with the appropriate denominator $`P+X(c)`$. |

The full evaluator will be tested against a small exhaustive reference implementation that enumerates globally legal analyses, with T1–T8 included in automated testing.

## 13. Parameter finalisation and WP0/WP1 checks

WP0/WP1 operationalise rule J through the following deliverables:

1. **Musicological reference.** Record documented occurrences and independent specialist judgements, fix the sets $`B_x`$, and define compatibility relations $`\mathcal C_{\mathrm{legal}}`$.
2. **Shared representation and decoding.** Validate the projection of $`u_1/u_3`$ onto atomic events, fix the output format, and implement matching with tests T1–T8.
3. **Family adequacy.** Record independent assessments by two specialists and evaluate the medoid model on a suitable pilot corpus to prespecify $`g_{\mathrm{use}}`$, $`\delta_{\mathrm{use}}`$, and $`g_{\min}`$.
4. **Statistical calibration.** Check the independence of work–source groups, the number of shared initialisations, the frequency of samples with $`n_f^{(b)}=0`$, simultaneous coverage over the region of 78 quantities, and a conservative procedure when coverage is inadequate.
5. **Data partitions and generalisation.** Use nested group-based cross-validation, finalise one $`R^\star`$ on the complete development corpus, and evaluate A2/M2 independently without consulting held-out test sets for representation selection.

Rule J is the common selection criterion throughout. These procedures specify its parameters, the quality of the reference annotations, and the reliability requirements for empirical evaluation.

**Integrating the specification into the research documents.** Harmonisation of the short proposal with detailed Sections 5.4, 6.1, E.1, E.3, G.5.1, and J.4 is an ongoing editorial step. The common requirements are rule J, a clear distinction between principal and diagnostic metrics, and a fixed architecture A for A2/M2.

## 14. Concluding methodological choice

M1 establishes a unified approach to symbolic representation selection for the study of Byzantine melodic formulae. The grid $`U\times\Phi`$ examines the contributions of input granularity and cumulative feature layers. Rule J evaluates successful recognition of an entire formula with the correct family identity under the prespecified architecture A. The requirement $`G_A\ge g_{\min}`$ establishes minimum family adequacy on known boundaries; the simultaneous uncertainty region records statistically compatible selections.

Synthetic Studies A, B, and C identify mechanisms affecting selection under O, N, and J. The separate A/B/C comparison retains the ability to study how joint boundary-and-family learning affects performance. With one operational $`R^\star`$, A2 and M2 can estimate their respective contrasts using comparable inputs and the shared segmental infrastructure.

The final empirical evaluation will assess generalisation and statistical stability on independent works and sources, following the requirements established in WP0/WP1.

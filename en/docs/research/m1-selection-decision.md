# M1 — Revision of the representation design and selection criterion $R^\star$

**Methodological documentation · 31 October 2026**

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/research/m1-selection-decision.md) · **English**
<!-- language-switch:end -->

> **Status:** Finalised specification of selection rule J. Application to annotated data, final construction of the musicological reference, and calibration of statistical coverage are scheduled for WP0/WP1. The numerical tables below report synthetic design simulations.
>
> **Related documents:** [Detailed M1 chapter (Greek)](../../../docs/full/05-m1.md) · [Core research programme](../../README.md) · [Source history (Greek)](../../../docs/maintenance/source-history.md) · [Research decision log (Greek)](../../../docs/review/decisions.md).

## 1. Why the M1 design was revised

M1 investigates how the symbolic representation of Byzantine chant affects the localisation and recognition of melodic formulae in continuous works. The initial design prioritised boundary accuracy. Further development of the protocol revealed a central requirement: recognising a formula in full entails identifying both its start and end boundaries and the family to which it belongs. This combination now provides the principal criterion for representation selection.

A melodic formula is treated as a variable-length segment with a family identity. Its boundaries may differ from those of a syllable, word, or notational symbol, while related realisations may differ substantially in their surface form. M1 therefore jointly examines the choice of symbolic input unit, the additional information provided by notational, temporal, modal, and textual features, and recognition on previously unseen works and sources. The design retains twelve input conditions mapped to a common sequence of atomic melodic events, so that all comparisons address the same computational task.

The revision progressed from rule **O**, which prioritised boundary F1, to **N**, which averaged complete-recognition F1 over architectures A/B/C, and finally to **J**. Rule J selects the representation according to recognition of an entire formula with the correct family in the prespecified architecture A, subject to a separate family-adequacy requirement. Its final specification is:

$$
\widehat J(R)=\frac{1}{n_{\mathrm{rep}}}\sum_{r=1}^{n_{\mathrm{rep}}} F_{1,\mathrm{seg+fam}}^{(r)}(R,A),
$$

$$
\widehat{\mathcal A}_{\mathrm{dec}}=\{R\in U\times\Phi:\widehat G_A(R)\ge g_{\min}\},
\qquad
R^\star=\underset{R\in\widehat{\mathcal A}_{\mathrm{dec}}}{\arg\max}\,\widehat J(R).
$$

$\widehat G_A$ measures macro-averaged recall across known families on documented boundaries. The threshold $g_{\min}$ is set through a specialist procedure and a pilot reference model before the twelve representations are compared. The operational choice of a single $R^\star$ is accompanied by a separate statistical uncertainty set $\mathcal R^\star$ and at most one sensitivity representation $R_{\mathrm{sens}}$. Architectures B/C are evaluated independently across the complete grid, keeping input selection tied to the principal architecture.

The same representation is subsequently used in A2 and M2, allowing the contribution of musicological knowledge and relational supervision to be examined on a fixed input. In M2's historical comparison, the primary contrast is:

$$
\Delta_{\mathrm{hist}}=S_{\mathrm{EISE}}-S_{\mathrm{B2}}.
$$

B2 and EISE share segmental infrastructure and a matched protocol. Their comparison investigates what the documented exegetical relationship of the same passage contributes to an independent performance-based criterion.

The choice of J is developed below through numerical counterexamples, three complementary synthetic sensitivity studies, and separate algorithmic and statistical checks. The discussion follows the reasoning from candidate representations and selection rules to the final evaluation protocol.

## 2. The representation grid: input units and successive feature layers

The candidate representation space is:

$$
\mathcal R=U\times\Phi,\qquad |U|=3,\quad |\Phi|=4,\quad |\mathcal R|=12.
$$

Earlier documentation denoted the feature set by F. The current research reader uses **$\Phi$** for the feature axis and reserves **F** for a formula family. This changes the notation while retaining all twelve experimental conditions.

| Factor | Levels | Research purpose |
| --- | --- | --- |
| Input unit U | u1: notational symbol · u2: atomic melodic event · u3: compound neumatic unit with a specified grouping rule | Compares the informational and structural granularity of the input. |
| Feature layers $\Phi$ | N · N+T · N+T+M · N+T+M+L | Measures successive contributions of temporal (T), modal (M), and textual/prosodic (L) information beyond the initial notational/melodic description N. |

**u3** is constructed by a prespecified grouping procedure independent of family labels and model predictions. The common output resolution is the atomic event sequence. Even when the input uses larger units, candidate boundaries are projected onto the same atomic coordinates. The projection, reproducibility of grouping, and preservation of permitted information therefore require explicit verification.

The four feature sets form a **cumulative sequence**. Each adjacent comparison estimates the incremental contribution of a particular layer conditional on those already included. The initial sensitivity analysis retained **twelve** main conditions. A full factorial extension or an additional syllabic unit can be examined diagnostically without changing the main design. See the [detailed M1 chapter (Greek)](../../../docs/full/05-m1.md).

The comparison also tests for indirect information leakage: a symbol or compound-unit identifier may reveal features ostensibly removed from an input condition. Model capacity, replicates, hyperparameter-search budgets, and data partitions remain comparable.

## 3. How the methodological decision developed

The changing selection rule reflects a more precise formulation of the research objective: from boundary localisation to joint boundary-and-family recognition, and finally to selection of the representation used by the principal architecture. The dates below refer to successive specifications and design studies.

| Period | Stage | Methodological development |
| --- | --- | --- |
| Up to analytical version v8.68i | Initial selection | Priority given to boundary F1, with a requirement for simultaneous statistical superiority to identify a single representation. Several representations could be carried into M2 when performance was indistinguishable. |
| **7 October 2026** | **Simulation Study A** | One operational choice using a constrained argmax, a separate uncertainty set, and at most one sensitivity analysis; exploration of family-adequacy and non-inferiority criteria. |
| October 2026, analytical version v8.71e | Rule **O** | Boundary micro-F1 as the primary measure, family criterion $G$, a simultaneous uncertainty region, and separate reporting of lost family recall. |
| 22–26 October 2026 | Intermediate core drafts | Stronger emphasis on the shared semi-Markov architecture and complete-formula evaluation while retaining the initial selection criterion. |
| **30 October 2026** | Rule **N** | Inclusion of architectures A/B/C and their mean complete-formula F1 in the selection rule, with a family-adequacy requirement for all three. |
| **31 October 2026** | **Simulation Studies B and C** | Examination of representation–architecture interactions, dependence between localisation and labels, and behaviour with few independent groups. Formulation of rule **J**. |
| **31 October 2026** | Algorithmic and statistical validation | Definition of complete admissible boundary pairs $B_x$, compatible matching, the uncertainty set $\mathcal R^\star$, families absent from bootstrap samples, and the common role of A in A2/M2. |

Earlier versions remain useful for reconstructing how the decision was reached. The operative specification appears in Sections 9–11 and is intended to be carried into the main research proposal as its source documents are harmonised.

## 4. Three selection rules and the quantities they estimate

### 4.1 Rule O — priority to boundary localisation

$$
R_O^\star=\underset{R:\widehat G_{e_0}(R)\ge g_{\min}}{\arg\max}\widehat M_{\mathrm{bnd}}(R,e_0).
$$

$M_{\mathrm{bnd}}$ is boundary micro-F1, with the prespecified tolerance when applicable; $G$ is macro recall over known families in externally bounded occurrences. The common estimator $e_0$ was left for a later stage in the initial specification; the final design explicitly sets $e_0=A$. Rule O directly targets boundary accuracy. Complete-formula recognition is reported as a separate outcome.

### 4.2 Rule N — mean performance across A/B/C

$$
R_N^\star=\underset{R:\min_{a\in\{A,B,C\}}\widehat{\mathrm{Rec}}_{\mathrm{fam}}(R,a)\ge r_{\min}}{\arg\max}\frac{1}{3}\sum_{a\in\{A,B,C\}}\widehat F_{1,\mathrm{seg+fam}}(R,a).
$$

Rule N estimates mean complete-formula recognition across three specified architectures. This is a coherent objective when transferability to A/B/C with equal weighting is the aim. In the present research design, B/C act as **comparators**, while A supplies the shared infrastructure for A2/M2. Selection by the A/B/C average may therefore differ from the input that best serves the main model. The minimum criterion also requires adequacy under B/C and left ambiguity over whether recall was measured at known or predicted boundaries.

### 4.3 Rule J — complete recognition with A

Rule J retains O's constrained argmax and family threshold while using the measure that directly reflects the full recognition task:

$$
R_J^\star=\underset{R:\widehat G_A(R)\ge g_{\min}}{\arg\max}\widehat F_{1,\mathrm{seg+fam}}(R,A).
$$

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

With adequate G for both representations, N selects R2. A then performs 0.07 below the available R1, which J selects. This example isolates the representation–architecture interaction $R\times a$, examined separately in the architectural comparison.

### 5.3 The minimum criterion makes A depend on weaknesses in B/C

If macro family recall for a representation is $(A,B,C)=(0.90,0.60,0.60)$ with threshold $0.70$, N excludes it even though A satisfies the criterion. If all candidate representations show similar weaknesses in B/C, N may produce an empty eligible set. J evaluates family adequacy under A, the architecture used in subsequent studies.

### 5.4 Joint success depends on the alignment of boundaries and family labels

A case study compared two representations with high boundary accuracy and high G but different **dependence between successful localisation and correct labels on the same occurrences**. Under condition O-b, R1 has boundary-F1 0.905 and joint F1 0.478; R2 has boundary-F1 0.853 and joint F1 0.558. Family recall on known boundaries is 0.800 and 0.779, respectively. The complete-recognition criterion captures whether both parts of the task succeed for the same occurrence.

## 6. Simulation Study A: operational selection and the statistical uncertainty set (7 October 2026)

The first study examined the decision rules over a grid of twelve representations using synthetic marginal measures of boundary performance and family recall. Its principal concern was how to choose **one operational representation** when several exhibit statistically similar performance.

The procedure had three distinct levels: (a) operational selection through point-estimate eligibility and maximisation of the primary measure; (b) construction of an uncertainty set $\mathcal R^\star$ containing statistically compatible optimal choices; and (c) evaluation of the main historical comparison with one $R^\star$, alongside at most one additional representation for descriptive sensitivity analysis.

The simulation covered **148 parameter combinations** and seven principal scenarios. In synthetic settings with a moderate number of independent groups, requiring a certified lower bound $L_G(R)\ge g_{\min}$ for eligibility frequently led to an empty set. For example, in a particular setting with sixteen groups and threshold 0.70, the probability that $\widehat{\mathcal A}^{-}$ was empty was approximately 0.673. Operational selection therefore retains the point-estimate criterion $\widehat G(R)\ge g_{\min}$, while the simultaneous uncertainty region is evaluated separately.

The direction of the statistical non-inferiority criterion was also checked. For a difference of $-0.10$, standard error 0.05, and multiplier 1.645, the **lower** confidence bound is $-0.18225$. Certifying non-inferiority against a margin of 0.04 requires the lower bound to be at least $-0.04$. Operational selection and non-inferiority certification thus serve different purposes in the protocol.

Study A's generator produced **marginal counts**. It did not represent the joint information for both endpoints and the family label of an individual occurrence, or the three architectures A/B/C. Two further synthetic studies were developed to assess complete recognition and representation–architecture interactions. The size of $\mathcal R^\star$ is treated as a random outcome of each scenario, with no universally predetermined range.

## 7. Simulation Study B: occurrence-level modelling and localisation–family dependence

The second study used a synthetic generator at the **occurrence level**. For each family, representation, and architecture, success in detecting a complete segment and correctly identifying its family was simulated, allowing positive or negative dependence within the Fréchet bounds. The design included interactions $R\times a$ and shared random effects for work–source groups.

The experiment used four representative representations, three architectures, eight families, sixteen groups, and approximately 290 occurrences per synthetic sample. It ran **2,000 Monte Carlo replicates**. The population reference was the best eligible representation according to A's joint segment-and-family F1. $P(\text{target})$ denotes the probability of choosing that representation; expected **regret** measures the shortfall from its population-optimal value under the same criterion.

| Scenario | O: selection probability / regret | N: selection probability / regret | J: selection probability / regret | Controlled mechanism |
| --- | --- | --- | --- | --- |
| S1 | 0.452 / 0.012 | **0.612 / 0.007** | 0.496 / 0.011 | Similar rankings across A/B/C; averaging reduces selection variance. |
| S2 | 0.692 / 0.015 | 0.000 / 0.062 | **0.744 / 0.012** | Representation–architecture interaction; the A/B/C average differs from A's best input. |
| S3 | 0.006 / 0.178 | 0.336 / 0.001 | 0.347 / 0.001 | Almost-correct boundaries and negative localisation–label dependence; boundaries alone select weaker complete recognition. |
| S4 | 0.742 / 0.017 | 0.618 / 0.025 | **0.803 / 0.013** | Performance close to the family-adequacy threshold; the A/B/C minimum increases the chance of excluding a suitable input. |

In S1, averaging A/B/C reduces selection noise. In S2, architectural differences change representation rankings and favour direct assessment under A. S3 reveals the effect of localisation–label dependence on complete recognition. The four scenarios provide targeted checks of the selection rules under explicitly defined synthetic assumptions.

## 8. Simulation Study C: complete segments across all twelve representations

The third study extended synthetic generation to **complete segments**, with start–end coordinates, family predictions, and admissible boundary pairs $B_x$. It included all twelve representations in $U\times\Phi$, eight scenarios S0–S7, **100 Monte Carlo replicates per scenario**, and **199 bootstrap resamples** per synthetic dataset. The shared evaluation criterion was A's population-level F1 for complete segments with correct family labels, estimated from a separate large synthetic reference sample.

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


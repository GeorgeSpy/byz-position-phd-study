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


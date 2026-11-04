# A2 — Musicological knowledge as an experimental variable

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/research/a2-knowledge-design.md) · **English**
<!-- language-switch:end -->

**Research design and scientific rationale · 3 November 2026**

> **Status:** Research specification. Synthetic and numerical checks support choices in the protocol. Budgets are initial estimates. Confirmatory evaluation requires real, independently annotated occurrences, enough independent work–source groups and a successful calibration of the statistical procedure in WP0.
>
> **Technical protocol:** [Appendix K — A2 technical protocol](../appendices/k.md). **Synthetic checks:** [`a2/support/`](../../../docs/research/a2/support/README.en.md).
>
> **Related texts:** [Revised M1](m1-selection-decision.md) · [Revised M2](m2-eise-research-design.md) · [Musical position and family](../current/position-and-family.md) · [ECSI](ecsi/README.md) · [Core research plan (LaTeX)](../../../documents/core-research-plan.tex) · [Musicological memorandum (LaTeX)](../../../documents/musicological-memorandum.tex).

## Contents

1. [The research question of A2](#1-the-research-question-of-a2)
2. [How the design emerged](#2-how-the-design-emerged)
3. [Musicological ontology and criteria](#3-musicological-ontology-and-criteria)
4. [Connection with informed machine learning](#4-connection-with-informed-machine-learning)
5. [What M1 passes on to A2](#5-what-m1-passes-on-to-a2)
6. [Diagnostic concepts and the family specification](#6-diagnostic-concepts-and-the-family-specification)
7. [Flat versus structured use](#7-flat-versus-structured-use)
8. [The 2×2 factorial experiment](#8-the-22-factorial-experiment)
9. [Controlled perturbations of knowledge](#9-controlled-perturbations-of-knowledge)
10. [The comparators B_K and B★](#10-the-comparators-b_k-and-b)
11. [The primary estimands](#11-the-primary-estimands)
12. [Metrics and hard cases](#12-metrics-and-hard-cases)
13. [Statistical analysis and multiplicity](#13-statistical-analysis-and-multiplicity)
14. [Data, annotation and leakage control](#14-data-annotation-and-leakage-control)
15. [Computational budget](#15-computational-budget)
16. [What different outcomes mean](#16-what-different-outcomes-mean)
17. [Relation to M2a, M2b–EISE, Mthesis and ECSI](#17-relation-to-m2a-m2beise-mthesis-and-ecsi)
18. [Decisions in this revision and open questions](#18-decisions-in-this-revision-and-open-questions)
19. [Why the experiment matters internationally](#19-why-the-experiment-matters-internationally)
20. [Core bibliography](#20-core-bibliography)
21. [Run registry and glossary](#21-run-registry-and-glossary)

## 1. The research question of A2

A2 asks whether **the validity of diagnostic musicological relations** and **the way they are logically integrated** provide distinct information for recognising families of Byzantine musical positions (theseis). The central question is:

> In a computational model that recognises musical positions within continuous symbolic notation, how much of the improvement comes from the validity of the musicological content and how much from the additional structured use of the same musical concepts?

The question has two testable parts:

- **RQ-A2.1 — Validity of content.** Does the ranking of each family's occurrences against all other occurrences (the AP of §12) improve when the specifications contain musicologically valid relations, compared with matched, controlled perturbed specifications?
- **RQ-A2.2 — Logical composition.** With the same valid diagnostic concepts available in both conditions, what does evaluating the complete logical specification add over an additive summary?

The methodological contribution of the design is the **separate experimental variation of two factors**: musicological validity and the integration mechanism. The evaluation links historically documented musical knowledge to measurable outcomes in symbolic music information retrieval (MIR).

A2 is an autonomous part of the core research programme. Earlier versions discussed it as "A2 of M2". In the current design the order is **M1 → A2 → M2a**; M2b–EISE follows under additional requirements on historical pairs and independent performance evaluation. ECSI is a separate, later architectural extension with its own protocol.

## 2. How the design emerged

The stages below describe the logic of the decisions, not necessarily their exact chronological order.

**First decision — a common computational base.** M1 selects one symbolic representation and one architecture for recognising boundaries and families. A2 uses this base, so that the effects of knowledge are tested without a new representation search.

**Second decision — two different sources of improvement.** Adding musical features and exploiting the logical composition of a specification are different learning mechanisms. A2 therefore uses a common table of musical concepts with two modes of use.

**Third decision — valid versus controlled perturbed knowledge.** A simple "with rules / without rules" comparison does not isolate the value of musical content. A2 therefore introduces perturbations with matched logical structure, applicability and missingness, but with altered musical relations.

**Fourth decision — a full factorial design.** The two factors are crossed in four conditions FV, FP, DV, DP. The design yields main contrasts and a secondary interaction.

**Fifth decision — strong comparators.** The linear $B_K$ and the stronger $B^\star$ test whether written musicological knowledge offers anything beyond free learning from the available features.

**Sixth decision — prespecified statistical interpretation.** The two primary estimands were defined before confirmatory evaluation. Five training replicates, ten perturbations, multiplicity control and independent work–source groups were specified.

**Seventh decision — technical and musicological verifiability.** The following checks come before the interpretation of any final performance:

- non-equivalence of the perturbations;
- correct semi-CRF normalisation;
- behaviour of the three-valued logic;
- information parity across conditions;
- independent judgements.

**Eighth decision — a calibrated statistical procedure.** Synthetic checks showed that the per-dataset bootstrap-t gives lower coverage with few groups. They also showed that the strict rule on undefined resamples requires near-ubiquitous family presence. The primary candidate procedure became the jackknife with a Student $t(G-1)$ reference distribution. Its confirmatory use depends on calibration in WP0, before the independent test set is opened (§13).

## 3. Musicological ontology and criteria

### 3.1 Musical position

A **musical position** is treated as a historically and musicologically identifiable melodic formation. It has internal organisation and can appear in different written or performed realisations. Its exact computational delimitation is part of the research protocol; variable length and the relation to wider context are recorded explicitly.

### 3.2 Historical type, analytical family, occurrence, realisation

A **historical type** is a name or morphological distinction documented in a specific music theory, manuscript or research tradition. The same name may cover variants that need further analysis.

An **analytical family** $F$ is a versioned musicological hypothesis. It links a specific specification $\sigma_{F,v}$ to the register of assessed occurrences in the reference corpus. Its scope, requirements and exclusions are recorded explicitly. The category can be revised, split or merged when work on the sources requires it.

An **occurrence** is a specific passage of a work in a specific source, with its boundaries, musical and textual context and alignments.

A **realisation** is the concrete form of the melodic formation, with its modal, melodic, temporal and syllabic organisation. Written realisations and performed responses are different levels of observation.

### 3.3 Musicological relations in A2

For each candidate family the following are recorded, as appropriate:

1. **Melodic structure:** course, internal articulations, sequence of characteristic figures.
2. **Cadential process:** relation of the cadence to the melodic course and its function in the given context.
3. **Modal function:** echos, active degrees, genus, martyriai or phthorai, where they give genuinely assessable information.
4. **Temporal and rhythmic organisation:** relations that may characterise the position or an alternative development of it.
5. **Prosodic and syllabic application:** relation to the text, syllabic development and functional place in the melos.
6. **Alternative sufficient configurations:** more than one musically legitimate internal form.
7. **Exclusions:** documented relations that distinguish a family from its nearest confusable types.
8. **Historical documentation:** exact sources, older notations, exegeses, names and expert judgements.

The combination is **specific to each family**. A2 does not assume a single universal melodic core for all positions.

### 3.4 The role of historical sources

Karagounis's (2003) study of the Cherubic hymns and Gheorghiță's (2009) study of the Sunday Koinonika provide candidate diagnostic relations, cases of historical naming and comparisons of realisations. Older names and notational signs are concrete pieces of evidence that need analysis of their melodic function.

Distinctions such as *parakalesma*, *parakletike*, *kylisma*, *lygisma* and other great hypostaseis need particular care. Historical or notational kinship can create a candidate family relation, which is then assessed against defined musicological criteria.

Chrysanthos's example on the parakalesma and its variation by degree (*Θεωρητικόν Μέγα της Μουσικής*, ed. P. G. Pelopidis, Trieste 1832, §408) is an object of primary examination. The paragraph number is checked in the 1832 print and compared with the 1816 autograph before the example is used as a validated musical case. Likewise, the cases in Karagounis and Gheorghiță are turned into complete source cards before they are used as validated training or evaluation examples.

Relations between occurrences are also kept explicitly distinct: shared family, historical homology of the same passage, exegetical relation and copying dependence. One relation is never used as automatic proof of another.

## 4. Connection with informed machine learning

**Informed machine learning** describes procedures in which prior knowledge enters a learning system explicitly. The knowledge may shape the representation, the structure, the objective or the checking of results. The taxonomy of **von Rueden et al. (2023)** provides the main methodological frame.

In A2 musicological knowledge acts at several levels. It defines the family hypothesis, feeds specific diagnostics, specifies the logic of membership and is tested against independent musical judgements. The distinctive research choice is that **the knowledge itself becomes an experimental variable**. The design separates:

- the value of **valid musical content**;
- the value of **a specific computational way of composing** that content;
- the potential **interaction** of validity and composition.

In neurosymbolic learning, **Xu et al. (2018)** link logical specifications to probabilities. **Koh et al. (2020)** study transparent intermediate concepts and **Marconato et al. (2023)** analyse reasoning shortcuts. **van Krieken et al. (2024)** examine the limits of the independence assumption for concepts. Penalising constraint violations inside a structured model has a direct precedent in the constrained conditional models of **Chang, Ratinov and Roth (2012)**. A2 does not propose a new form of penalty. It places the penalty in a controlled symbolic MIR experiment with valid and with perturbed, historically documented content. The need for such controls is not hypothetical: models that use knowledge graphs can perform almost as well with heavily perturbed graphs (**Raman et al., 2021**).

The analogy with physics-informed machine learning concerns the explicit use of scientific knowledge. Here the content comes from musicological analysis and is subject to checks of historical, source-critical and interpretive validity.

## 5. What M1 passes on to A2

### 5.1 The $U\times\Phi$ grid and architecture A

M1 examines **three kinds of input unit** combined with **four levels of cumulative features**, twelve representations in total. The information groups are $N$ (notation), $T$ (time), $M$ (modal features) and $L$ (text and prosody).

The main architecture **A** scores variable-length segments with a semi-Markov CRF of order zero in family transitions and estimates boundaries and family jointly. It thus scores the whole musical position rather than isolated events (Sarawagi and Cohen, 2004). The encoder is chosen before the grid, on internal, independent development splits: TCN-S as the initial choice and a BiGRU with matched context width as the comparison model.

### 5.2 Selection rule J

The operational representation $R^\star$ results from:

$$
\widehat J(R)=\frac{1}{5}\sum_{r=1}^{5}F1_{\mathrm{seg+fam}}^{(r)}(R,A),
$$

$$
\widehat{\mathcal{A}} _ {\mathrm{dec}}=\lbrace R\in U\times\Phi:\widehat G_A(R)\ge g_{\min}\rbrace,
$$

$$
R^\star=\arg\max_{R\in\widehat{\mathcal{A}} _ {\mathrm{dec}}}\widehat J(R).
$$

$\widehat G_A$ is the mean recall per known family on complete known segments, with forced choice of a label. The threshold $g_{\min}=\max\lbrace g_{\mathrm{use}},\widehat G_0^{\mathrm{pilot}}+\delta_{\mathrm{use}}\rbrace$ is set before ranking, from independent expert judgements and a pilot reference model. Architectures B and C of M1 are evaluated across the whole grid with descriptive and estimative status. $R^\star$ is finalised before the main A2 starts. The separate set $\mathcal{R}^\star$ describes selection uncertainty and does not give A2 several post hoc "best" inputs. Details: [revised M1](m1-selection-decision.md).

### 5.3 Five bases

For a candidate segment $s$ and family $f$, each replicate $r=1,\dots,5$ has its own trained base:

$$
b_r(s,f)=b_{\widehat{\psi} _ r}(s,f).
$$

$b_r$ uses the `A_M1_selected` configuration on $R^\star$. It is trained without specifications on development groups $\mathcal{D} _ {\mathrm{base}}$, and its temperature is fitted on separate internal development groups $\mathcal{D} _ {\mathrm{int}}$. In the **main A2** the base remains fixed and shared by the conditions of the same replicate. The intervention therefore concerns how musicological knowledge is used. Full retraining of the encoder is a separate sensitivity analysis.

Model names are kept distinct. M2 uses the symbolic reference models $\mathrm{B0_{sym}}$ and $\mathrm{B0_{profile}}$ and the neural conditions B1, $\mathrm{B2_{fam}}$ and $\mathrm{B2_{main}}$. A2 uses the bases $b_r$ of architecture A and its own comparators $B_K$ and $B^\star$. The trained M1 weights are recorded as `m1_checkpoint_id` for reproduction.

## 6. Diagnostic concepts and the family specification

For segment $s$, family $f$ and knowledge $K\in\lbrace V,P\rbrace$ a table of diagnostic concepts is defined. Automatic extractors compute the concepts from the selected symbolic input and legitimate context. The true label of the occurrence remains hidden during prediction.

A family specification organises concepts into three logical roles:

- **required relations** $R$, e.g. a specific cadential function;
- **alternative sufficient configurations** $A$, in groups of which one suffices, e.g. two admissible internal developments;
- **explicit exclusions** $E$, e.g. a specific incompatible modal change.

The specification also defines its **scope**: echos, genre, period, notational level and functional position. The cards also record **supportive relations**, which strengthen a membership without imposing it; an example is the neumatic patterns of the kylisma. Supportive relations **do not enter** the summaries $Q$ or the rule $\phi$ of the main analysis. Their status is decided in WP0, before the specifications are finalised.

A synthetic example rule is:

$$
\phi_f(z)=z_1\land(z_2\lor z_3)\land\neg z_4 .
$$

Here $z_1$ may express a required cadential relation, $z_2,z_3$ alternative internal figures and $z_4$ an excluded modal behaviour. The meaning of each $z_i$ is specific to the family, with explicit judgement criteria. The example describes a logical possibility; without further evidence it does not correspond to a historically validated family.

The possibility of more than one sufficient branch matters musicologically. Many realisations can belong to the same family without sharing an identical local form. Which features are shared and which are alternatives is decided by source criticism and independent examination of real occurrences.

## 7. Flat versus structured use

### 7.1 Shared summaries $Q_f^K$

Every condition receives the same concept table and the same role assignment. Each literal $j$ gives $q_j=2c_j-1$ if it belongs to role R or A and is observed, $q_j=1-2c_j$ if it belongs to E and is observed, and $q_j=0$ if its value is unknown. The three summaries are:

$$
Q_R=\frac1{|R|}\sum_{j\in R}q_j,\qquad Q_A=\frac1{|\mathcal{G}|}\sum_{G\in\mathcal{G}}\frac1{|G|}\sum_{j\in G}q_j,\qquad Q_E=\frac1{|E|}\sum_{j\in E}q_j .
$$

$Q_R$ measures satisfaction of the required relations, $Q_A$ of the alternative groups and $Q_E$ the absence of exclusions. Values lie in $[-1,1]$. Denominators include unknown literals, so that missingness does not inflate the mean of the rest.

### 7.2 Flat mechanism $F$

$$
\boxed{\ell_{F,K}(s,f)=b_r(s,f)/T_r+w^\top Q_f^K(s)} .
$$

The mechanism combines the three summaries additively. It learns weights shared by all families and tests the usefulness of the concepts without enforcing their full logical relation.

### 7.3 Structured mechanism $D$

$$
\boxed{\ell_{D,K}(s,f)=b_r(s,f)/T_r+w^\top Q_f^K(s)-\lambda v_f^K(s)},\qquad v_f^K(s)=\mathbf{1}[\phi_f^K(s)=0].
$$

Structured use adds a penalty when the complete musicological specification is **documentably violated**. The penalty enters the segment scores and the semi-CRF normalisation, in both training and prediction. The parameters are constrained to

$$
w_r\ge0.1,\qquad\sum_rw_r=1,\qquad\lambda\in[0,2].
$$

The weights are shared across families and fitted separately for each condition with a common procedure, on the groups $\mathcal{D} _ {\mathrm{int}}$. The value $\lambda=0$ is feasible, so $D$ can coincide numerically with $F$. No positive lower bound is imposed. The distribution of $\hat{\lambda}$, the share with $\hat{\lambda}\lt 0.1$ and the frequency at the upper bound 2 are reported. A nearly inactive penalty and an active penalty without benefit are different outcomes (§16).

### 7.4 Why structure can add information

The rule $z_1\land(z_2\lor z_3)\land\neg z_4$ can also be represented on binary features by a linear threshold: the decision $3z_1+z_2+z_3-6z_4\ge4$ is equivalent. **Using logical connectives does not by itself create an expressive advantage.**

By contrast, $(a\lor b)\land(c\lor d)$ is in general not linearly separable as a function of $a,b,c,d$. The complete logic of independent alternative groups can express decisions that a simple additive rule cannot. The specific $F$ shows the difference directly: the states $(a,b,c,d)=(1,1,0,0)$ and $(1,0,1,0)$ have the same summary $Q_A=0$, while the first violates the rule ($\phi=0$) and the second satisfies it ($\phi=1$). The additive knowledge term $w^\top Q$ of $F$ is therefore the same in both states, while the term $-\lambda v$ of $D$ separates them. The base score $b_r$ may already distinguish them; the difference concerns the knowledge term only. The general discussion of linear separability also concerns the free linear $B_K$, which sees the same concepts without roles. Which kind of specification actually occurs in musical families is an empirical question. A2 tests a specific musicological content and a specific computational composition.

### 7.5 Three-valued logic: true, false, unknown

A source may not allow every diagnostic to be assessed. A2 distinguishes three values: documented satisfaction, documented violation and an unknown or unassessable state. The rule $\phi$ is computed with Kleene's strong three-valued logic. In the main version an unknown value **does not trigger a penalty**. It is recorded, so that diagnostic coverage per family and source can be reported. A missing observation is thus not equated with musical incompatibility.

### 7.6 Semi-CRF normalisation

For a legal complete segmentation $y$ of sequence $X$, the structured mechanism gives

$$
p_{D,K}(y\mid X)=\frac{\exp\left(\sum_{(s,f)\in y}\ell_{D,K}(s,f)\right)}{\displaystyle\sum_{y'\in\mathcal{Y} _ {\mathrm{legal}}(X)}\exp\left(\sum_{(s,f)\in y'}\ell_{D,K}(s,f)\right)} .
$$

$\mathcal{Y} _ {\mathrm{legal}}$ contains the non-overlapping admissible segmentations. In the main order-zero configuration there are no transition terms between families of neighbouring segments; the constraints of a complete segmentation still apply. The unknown family has no logical rule but remains in the same normalisation.

## 8. The 2×2 factorial experiment

The two factors are:

- **knowledge validity** $K\in\lbrace V,P\rbrace$: musicologically valid specification $V$ or controlled perturbed specification $P$;
- **mechanism of use** $C\in\lbrace F,D\rbrace$: flat additive or structured logical use.

| | Valid specification $V$ | Controlled perturbed $P$ |
|---|---|---|
| **Flat use $F$** | **FV** — valid concepts, additive summaries | **FP** — perturbed relations, additive summaries |
| **Structured use $D$** | **DV** — valid knowledge with a logical penalty | **DP** — perturbed knowledge with the same logical procedure |

The design examines the two main contrasts and their interaction. $R^\star$, the bases, the eligible passages, the budgets and the tuning procedure remain matched. Superiority of DV over FV shows an added benefit of logical composition under valid knowledge. The DV–DP comparison examines validity within the structured mechanism. FV–FP and DP–FP help interpret the general effect of structure.

## 9. Controlled perturbations of knowledge

### 9.1 Why perturbations are not random noise

To assess the specific value of musicological content, perturbed knowledge must be comparable in non-musical complexity. A simple random change of a diagnostic can produce much easier or completely incompatible rules and destroy the interpretation of the experiment.

### 9.2 What the generator preserves

Each of the ten perturbations results from a **universal bijective mapping** of concept identities, applied to all families simultaneously. It preserves:

1. the logical skeleton of the rule;
2. the number and roles of literals and the sizes of alternative groups;
3. modal applicability, through admissible permutation classes per concept type;
4. family overlaps and the multiplicities with which concepts occur;
5. the presence frequency of each concept, within a tolerance of 0.10;
6. the missingness rate of each concept, within a tolerance of 0.10.

Frequencies are computed on development data without labels. The mapping comes from a **constrained sampler** that proposes only images within tolerance. In the synthetic checks uniform permutations almost never met the tolerance. The **canonical card of every family** must change. A swap inside the same alternative group or within the same role moves literals without changing the specification and does not count as a change. The perturbation thus alters the musical relation: it may replace a diagnostic cadence or an internal figure with a feature of similar frequency that was judged non-diagnostic for the family.

### 9.3 Checking logical non-equivalence

A change in the written form of a rule is not enough. A perturbation is accepted only if:

- it differs from V and from earlier perturbations both in the canonical form of the specification and in the values $(Q,v)$ on observed states;
- every family has a state of certain satisfaction ($\phi=1$) and a state of documented violation ($\phi=0$);
- two linear programmes give positive distances $d_F$ and $d_D$ between the scores of V and P.

The distances are computed over all admissible $w$ and $\lambda\in[0,2]$. A certificate is accepted only if the solver terminates successfully, the primal residual, dual residual and duality gap are at most $10^{-8}$, and a conservative dual lower bound is positive. The reason the search terminated is also recorded. Perturbations are selected without labels and without performance on the evaluation set. If ten accepted perturbations are not found within 100,000 proposals, confirmatory A2 stops and the comparisons are reported descriptively ([Appendix K, §K.5](../appendices/k.md#k5--perturbations-and-the-non-equivalence-certificate)).

### 9.4 Musicological judgement of a perturbation

The protocol requires expert documentation that a substitution is not synonymous or a trivial rewording. A stricter version is proposed for decision in WP0: independent experts examine blind, without knowing which specification is V, whether the new relations are indeed unsuitable as diagnostics for the family. A perturbation judged equally valid musically is an alternative scientific hypothesis and is labelled as such.

## 10. The comparators B_K and B★

### 10.1 $B_K$: free linear learning from the same concepts

$B_K$ uses the same extracted concepts, without roles and without a specification, and learns free per-family weights on the same base $b_r$, on the same groups $\mathcal{D} _ {\mathrm{int}}$. It shows how much information a linear estimator recovers from the same concepts.

If $B_K$ outperforms a valid specification, the result returns to musicological review. The rule may be inadequate or overgeneralised, an extractor may be wrong, or application may fail in a given context. The evaluation then examines the real occurrences and their diagnostics.

### 10.2 $B^\star$: a strong neural reference point

$B^\star$ combines supervised contrastive learning (SupCon), family prototypes and the same concept supervision. It has additional learning capacity and a declared computational budget. SupCon (Khosla et al., 2020) organises representations so that examples with the same label lie close together. Prototypes give a reference point for each family. The comparison tests whether explicit structured musical knowledge offers an advantage over an adaptive neural model.

$B_K$ and $B^\star$ have distinct roles and are not merged into one generic reference model "without musicological knowledge".

## 11. The primary estimands

Let $S(C,K)$ be the mean $\mathrm{AP_{fam}}$ of condition $(C,K)$ over the five replicates and $\bar S(C,P)$ the mean over the ten perturbations. The aggregation is defined in §12 and is the same in all conditions.

### 11.1 Primary estimand: $\Delta_{\mathrm{know}}$

$$
\boxed{\Delta_{\mathrm{know}}=\frac{1}{2}\left\lbrace S(D,V)-\bar S(D,P)+S(F,V)-\bar S(F,P)\right\rbrace} .
$$

It estimates the effect of valid knowledge, averaged over the two modes of use. Its interpretation refers to the declared set of families, perturbations and work–source groups.

### 11.2 Primary estimand: $\Delta_{\mathrm{logic},V}$

$$
\boxed{\Delta_{\mathrm{logic},V}=S(D,V)-S(F,V)} .
$$

It estimates the added benefit of the structured logical penalty **when the musicological knowledge is valid**.

### 11.3 Secondary interaction

$$
I=\big[S(D,V)-S(F,V)\big]-\big[\bar S(D,P)-\bar S(F,P)\big].
$$

The interaction shows whether the benefit of structure changes with the validity of knowledge. The protocol keeps **two primary estimands** and the interaction as secondary. ECSI has its own, partly different confirmatory hierarchy; it does not change the experiment already defined for A2.

### 11.4 The scope of a positive result

A positive $\Delta_{\mathrm{know}}$ supports the predictive value of valid musicological content relative to the controlled perturbations. A positive $\Delta_{\mathrm{logic},V}$ supports the specific structured integration over additive use. A strong interpretation and its generalisation depend on the musicological validity of the specifications, statistical adequacy, independent checks, the quality of the generator and the comparators.

## 12. Metrics and hard cases

The primary comparison uses average precision $\mathrm{AP_{fam}}$, a measure of ranking quality. For each family $f$ of the fixed set $\mathcal{F} _ 0$, occurrences are ranked by the score of $f$, one against the rest. Each occurrence has equal weight. Tied blocks are inserted simultaneously. $\mathrm{AP_{fam}}$ is the mean of the $\mathrm{AP} _ f$. If a family has no positives in the evaluation set, $\mathrm{AP_{fam}}$ is undefined and the family is not removed post hoc.

The following are also recorded:

- $F1_{\mathrm{seg+fam}}$: exact joint recognition of boundaries and family, under the agreed boundary and matching rule, as in M1;
- $F1_{\mathrm{bnd}}$: boundary quality, regardless of family;
- behaviour on **hard negatives**, i.e. occurrences with high surface similarity and different musicological identity;
- results **per family**, especially where recognisability or diagnostic coverage differs;
- results on **known reference boundaries** and on **predicted boundaries**, where the metric allows;
- sensitivity to removing the textual layer $L$, to detect lexical shortcuts;
- quality, assessability and expert agreement per diagnostic concept.

Hard examples connect to reasoning shortcuts: a correct final prediction can arise from intermediate concepts that lack the intended musicological meaning (Marconato et al., 2023).

## 13. Statistical analysis and multiplicity

The two **one-sided primary tests** concern

$$
H_{0,1}:\Delta_{\mathrm{know}}\le0,\qquad H_{0,2}:\Delta_{\mathrm{logic},V}\le0 .
$$

The **Holm (1979)** correction is applied with an overall $\alpha=0.025$ for the two tests. If both are rejected, a second, hierarchically dependent level of superiority tests of DV against $B_K$ and $B^\star$ opens, also with Holm.

The uncertainty estimate accounts for:

- the correlation of many occurrences within the same work;
- possible copying or historical dependence between sources;
- recurring families and passages in the same contexts;
- the shared bases of the conditions;
- the reuse of the ten perturbations on the same specifications.

The five replicates measure numerical stability and allow paired comparison. They are not five independent musical samples. Likewise, the ten perturbations do not increase the number of independent works.

**Primary candidate procedure.** For each contrast $\theta$, the original estimate $\hat{\theta}$ over all $G$ independent groups of the test set H is divided by the delete-one-group standard error $\mathrm{SE} _ J$. The statistic $T=\hat{\theta}/\mathrm{SE} _ J$ is referred to a Student $t(G-1)$ distribution. Each deletion recomputes the pooled AP and exactly the same contrasts. A confirmatory $p$ is issued only if all quantities are defined and the standard errors are finite and positive. The paired group bootstrap-t is evaluated separately as a sensitivity analysis. Full definitions are in [Appendix K, §K.8](../appendices/k.md#k8--statistical-procedure-and-multiplicity).

**Calibration before H.** The $t(G-1)$ reference is a prespecified approximation. Its confirmatory use requires acceptable operating characteristics in a simulation study with realistic sizes from the pilot, before H is opened. The study uses exact null hypotheses, runs the full procedure on every synthetic dataset and reports separate denominators for planned, defined and issued datasets. If the gate fails, results are reported **as estimates**, with intervals and exploratory status. No alternative method is chosen on the basis of H.

**Composition of H.** H is designed so that every family appears in enough independent groups. Presence in at least two groups is necessary for the jackknife to be defined but is not sufficient for power or coverage. The coverage rule determines which groups can be in H together and hence the evaluation distribution. The simulation study therefore runs the same algorithm that allocates groups to H and development. The target $m_H$ and the minimum coverage of development are set jointly in the pilot.

**What the synthetic checks showed.** The checks in [`a2/support/`](../../../docs/research/a2/support/README.en.md) use arbitrary synthetic parameters. They show mechanisms and orders of magnitude, not the performance of the real corpus. With exact nulls and independent random streams, the jackknife-t with a $t(G-1)$ reference kept the FWER at 0–0.026 for $G=6$–30, with coverage 0.953–0.994. An earlier batch with a shared stream for the reference and the datasets had given 0.028, with an upper Monte Carlo bound of 0.047. The per-dataset bootstrap-t gave lower coverage (0.89–0.94) and, because of suspensions, lower power. With sparse family presence, allocating groups to H for family coverage raised the issued datasets from 498 to 992 of 1000; with $m_H=2$, however, development was often left with a family in fewer than two groups. Calibration in the pilot remains necessary: in one scenario the FWER reached the nominal level, and $m_H$ is set together with the minimum coverage of development.

### 13.1 Equivalence and non-inferiority

A non-significant difference between valid and perturbed knowledge does not establish equivalence. Equivalence requires a different, prespecified test with an appropriate margin, power and confidence intervals. The distinction matters because a strong effect of structure can appear regardless of content validity. Appropriate comparators and an accurate account of the interaction are needed before performance is attributed to valid musicological knowledge.

## 14. Data, annotation and leakage control

### 14.1 WP0 as a prerequisite

Before the main run, an inventory is needed of available works, sources, realisations, licences, candidate families, possible historical dependencies and the proportion of assessable diagnostics. The soundness of A2 depends particularly on the quality of the **family cards**. Each diagnostic relation needs a source, scope, examples, distinguishing criteria and, where present, a record of uncertainty or disagreement.

### 14.2 Data splits

Work–source groups are split, before any selection and training, into three parts:

- the closed independent test set **H**, defined in month 12 with a family-coverage design;
- the groups **$\mathcal{D} _ {\mathrm{base}}$**, for the bases and the extractors;
- the groups **$\mathcal{D} _ {\mathrm{int}}$**, for temperature, heads, $B_K$ and abstention.

Fitting the heads on $\mathcal{D} _ {\mathrm{int}}$ avoids the underestimation of $\lambda$ observed when heads were fitted on the same groups as the base. Allocating H for family coverage must not leave development without enough families. The protocol ensures that:

- a work and its directly dependent copies are not spread across different parts of the split;
- constructing a specification uses no information from H;
- extractors do not receive the true family label;
- conditions FV, FP, DV and DP have the same access to data and reference boundaries;
- perturbations are not selected on performance;
- uncertainty and multiple splits are recorded under a common protocol.

### 14.3 Independent musicological validation

M3a checks membership judgements and musical distinctions on new passages. In the first phase experts judge boundaries and family without access to specifications or predictions; these judgements provide the evaluation labels. A2 uses the checked diagnostics while keeping the drafting of specifications separate from their external evaluation.

### 14.4 Proposed additional checks

The following are proposed as secondary checks, with an activation policy to be prespecified:

- hard or quantised concepts;
- replacing an estimated concept with a confirmed expert value (concept clamping), which is not automatically interpreted as a causal intervention with an explicit structural causal model;
- independent blind evaluation of perturbations (§9.4).

## 15. Computational budget

The main specification uses **five replicates** and **ten perturbations**. Per final split:

| Group | Computation | Fits |
|---|---|---:|
| FV and DV | 2 conditions × 5 replicates | 10 |
| FP and DP | 2 conditions × 10 perturbations × 5 replicates | 100 |
| $B_K$ and $B^\star$ | 2 comparators × 5 replicates | 10 |
| **Total** | | **120** |

The number concerns the **main run**, mostly small parametric heads on a fixed base. The five bases $b_r$, pre-training, configuration trials, hyperparameter search, calibration simulations, full retraining and sensitivity analyses cost extra.

For initial musicological and symbolic annotation the core plan foresees roughly **2–4 hours per work** and **1–2 hours** of second judgement for works in the relevant subset. For 40–60 works the first annotation corresponds to **80–240 hours**. These are initial estimates to be replaced by WP0 measurements. Before the confirmatory run, training time, memory and cost per perturbation and replicate must be measured.

## 16. What different outcomes mean

The cases below are **interpretive scenarios**, not results.

| Observed pattern | Interpretation and next check |
|---|---|
| $\Delta_{\mathrm{know}}\gt 0$ and $\Delta_{\mathrm{logic},V}\gt 0$ with adequate precision | Valid knowledge and its logical composition give a distinct benefit. DV is tested against $B_K$ and $B^\star$, and generalisation per family is checked. |
| Positive validity effect, small structure effect | The musicological concepts are useful, but the extra logical penalty may add little in this corpus. |
| Small validity effect, positive structure effect | A general benefit of the constraining parametrisation, or insufficient separation of valid and perturbed knowledge, is investigated. |
| $\hat{\lambda}$ near zero in most fits | The penalty stays nearly inactive: the data do not use it. Activation of $v$ and extractor quality are checked. |
| Active penalty ($\hat{\lambda}$ away from 0) without benefit on H | The penalty is used in training but does not generalise; dependence on the development groups and the validity of the rules are examined. |
| $B_K$ above DV | Extractor quality, scope and excessive narrowness or breadth of the specifications are examined. |
| $B^\star$ above DV | Relative expressiveness and capacity and the practical value of explicit rules for the available data are examined. |
| Large variation across sources or families | Generalisation is characterised per group; musicological inconsistencies, rare types and missing diagnostics are investigated. |
| Too few independent groups or failed calibration | Estimative reporting, sensitivities and planning of further data collection instead of a confirmatory claim. |

A2 has research value even when an initial hypothesis fails. A reliably documented negative result shows where musical knowledge, an extractor or the logical composition needs revision.

## 17. Relation to M2a, M2b–EISE, Mthesis and ECSI

### 17.1 M1

M1 examines the choice of $R^\star$, segmentation and the joint recognition of families. A2 assesses the added information of specific musicological specifications on top of this infrastructure.

### 17.2 M2a — relational supervision from shared family

M2a examines the contribution of real pairs of occurrences of the same family. Its main contrast, $\mathrm{B2_{fam}}$ against B1, concerns relational supervision and is interpreted together with the check $Q_{\mathrm{real}}$ that realisation information is retained.

### 17.3 M2b — historical supervision with EISE

M2b compares same-family pairs with historically verified **co-exegeses of the same passage**. Its main historical estimand is

$$
\Delta_{\mathrm{hist}}=S_{\mathrm{EISE}}-S_{\mathrm{B2_{main}}} .
$$

Independent performance dispersion provides an external criterion when the adequacy gates for historical pairs, recordings and statistical precision are met. $\Delta_{\mathrm{hist}}$ differs from the A2 estimands.

### 17.4 Mthesis — probabilities of realisations

The probabilistic operator Mthesis defines, for family $F$, context $C$ and realisations $X$:

$$
M_{\mathrm{θέσις}}(F,C)[X=x]=p_\theta(x\mid F,C).
$$

A2 examines knowledge for **recognising the family**. Mthesis examines what an already identified family predicts about the **admissible and preferred realisations** in a given context. The two studies share musicological infrastructure and have different computational targets.

### 17.5 ECSI-D — dependent probabilistic composition

ECSI (*Evidence-Conditioned Selective Invariance*) is a later, self-contained architectural extension. It examines whether the musicologically documented specification of a family can be compiled into a probabilistic event under a **dependent** distribution of diagnostics:

$$
m_F(x,c)=\sum_{z\in S_F(c)}q_\theta(z\mid x,c).
$$

The exact union of sufficient branches requires each overlap to count once and computationally feasible inference. ECSI-D also examines the meaning of concepts, assessability, calibration across families and retention of realisation information.

The A2 of the core programme uses the additive score with and without a logical violation penalty, as defined in Appendix K. ECSI-D **does not replace** condition $D$ of A2. It is evaluated under its own protocol, estimands and criteria, so the two questions remain separate.

### 17.6 Summary map

| Study | Research object | Main contrast |
|---|---|---|
| M1 | Boundaries and family identity | $U\times\Phi$, architectures A/B/C, rule J |
| A2 | Content and logical use of musicological knowledge | $V/P\times F/D$, $\Delta_{\mathrm{know}}$, $\Delta_{\mathrm{logic},V}$ |
| M2a | Family kinship and realisation | $\mathrm{B2_{fam}}-\mathrm{B1}$, $Q_{\mathrm{real}}$ |
| M2b–EISE | Historically documented relation of the same passage | $S_{\mathrm{EISE}}-S_{\mathrm{B2_{main}}}$ |
| Mthesis | Distribution of realisations given $F,C$ | Prediction $p_\theta(x\mid F,C)$ and related checks |
| ECSI-D | Dependent concepts and exact union of sufficient branches | Structured versus flat knowledge and strong reference models, under its own protocol |

## 18. Decisions in this revision and open questions

### 18.1 What has been specified

- A2 examines two factors in a full $2\times2$ design, with primary estimands $\Delta_{\mathrm{know}}$ and $\Delta_{\mathrm{logic},V}$.
- The input comes from M1 and is finalised before the comparison; each replicate has its own base $b_r$.
- $F$ and $D$ use the same concepts and three role summaries $Q_R,Q_A,Q_E$.
- $D$ adds a penalty for documented logical violation inside the semi-CRF, with $\lambda\in[0,2]$.
- Ten active perturbations, five replicates, $B_K$, $B^\star$ and 120 main fits per final split are foreseen.
- The two one-sided primary tests use the Holm correction with $\alpha=0.025$.

### 18.2 Decisions in this revision

1. **Single technical reference:** [Appendix K](../appendices/k.md) is the A2 protocol for this version.
2. **$\lambda$:** remains $[0,2]$ without a positive lower bound; the distribution of $\hat{\lambda}$, the share with $\hat{\lambda}\lt 0.1$ and the frequency at 2 are reported.
3. **Heads:** fitted on $\mathcal{D} _ {\mathrm{int}}$, where the temperature is also fitted.
4. **Generator:** a constrained sampler of bijective mappings, a change in every family's canonical card, canonical and functional uniqueness, LP certificates with checked residuals and a conservative dual lower bound.
5. **$\mathrm{AP_{fam}}$:** fully defined (§12 and §K.6).
6. **Statistical procedure:** jackknife-t with a $t(G-1)$ reference as primary candidate, bootstrap-t as sensitivity, calibration in WP0 before H.
7. **Composition of H:** family-coverage design, with the same allocation algorithm in the calibration study.
8. **Supportive relations:** outside $Q$ and $\phi$ until the WP0 decision.
9. **Metrics:** $F1_{\mathrm{seg+fam}}$ for joint recognition of boundaries and family and $F1_{\mathrm{bnd}}$ for boundaries, as in M1.

### 18.3 Open before preregistration

1. **Feasibility:** enough musicologically assessed families and independent groups; extractor accuracy; access rights.
2. **Adequacy of perturbations in the real corpus:** immovable families, tolerance and, optionally, blind musicological judgement.
3. **Calibration:** operating characteristics with the real pilot sizes and at least 5000 replications per critical scenario; minimum issuance probability; coverage target $m_H$ together with the minimum coverage of development.
4. **Supportive relations:** inclusion as required or alternative relations, a separate descriptive analysis or remaining on the cards only.
5. **The ratio $\mathcal{D} _ {\mathrm{base}}/\mathcal{D} _ {\mathrm{int}}$.**
6. **Execution reproducibility:** manifests for splits, cards, seeds, perturbation identifiers, model versions and checked results.

### 18.4 Additional, not yet integrated strengthenings

Proposed so far: a blind-supervision subset per diagnostic, replacing concepts with expert values, learning curves, coverage of rare sufficient branches, more specific checks of rater dependence and a stricter check of concept meaning per modal context. Their inclusion is decided before final preregistration, with a feasibility check and a clear separation from the main hypotheses.

## 19. Why the experiment matters internationally

A2 offers a transferable **research question**: how much predictive value lies in the *validity* of a musical domain's knowledge, and how much in the *logical form* in which it enters symbolic recognition models?

The question connects informed machine learning, neurosymbolic reasoning, music ontology and reproducible MIR evaluation. With suitable sources the design can be applied comparatively to other monophonic traditions with reused melodic formulas, such as Gregorian chant. The historical and musicological autonomy of each tradition is kept in the specifications, kinship rules and evaluation sets, with separate concept vocabularies.

> A2 provides a controlled framework for evaluating musicology-informed machine learning, experimentally separating the validity of musical content from the value of its logical integration into the recognition of families of melodic positions.

## 20. Core bibliography

Page numbers of historical examples are checked against the primary source before use in an article.

### 20.1 Byzantine and comparative musicology

- **Karagounis, K. (2003).** *Η παράδοσις και εξήγησις του μέλους των Χερουβικών της βυζαντινής και μεταβυζαντινής μελοποιίας*. Athens: Institute of Byzantine Musicology. Basis for comparative cases of positions, historical names, exegeses and confusable formations.
- **Gheorghiță, N. (2009).** *Chinonicul duminical în perioada post-bizantină (1453–1821). Liturgică și muzică*. București: Sophia. On the papadic melodic idiom, realisations and the historical setting of the Koinonika.
- **Gheorghiță, N. (2010).** Observations on the technique of transcription (exegesis) into the New Method of analytical music notation of the Sunday Koinonikon of the 18th century. *Studii și Cercetări de Istoria Artei*. [Text](https://www.scia.istoria-artei.ro/resources/2010/02_NICOLAE%20GHEORGHITA_technique_of_transcription.pdf)
- **Cambouropoulos, E. (2001).** Melodic cue abstraction, similarity, and category formation: A formal model. *Music Perception*, 18(3), 347–370. [DOI](https://doi.org/10.1525/mp.2001.18.3.347)
- **Volk, A., & van Kranenburg, P. (2012).** Melodic similarity among folk songs: An annotation study on similarity-based categorization in music. *Musicae Scientiae*, 16(3), 317–339.

### 20.2 Structured prediction, informed and neurosymbolic learning

- **Sarawagi, S., & Cohen, W. W. (2004).** Semi-Markov conditional random fields for information extraction. *Advances in Neural Information Processing Systems*, 17. [Proceedings](https://papers.nips.cc/paper_files/paper/2004/hash/eb06b9db06012a7a4179b8f3cb5384d3-Abstract.html)
- **Chang, M.-W., Ratinov, L., & Roth, D. (2012).** Structured learning with constrained conditional models. *Machine Learning*, 88(3), 399–431. [DOI](https://doi.org/10.1007/s10994-012-5296-5)
- **von Rueden, L., et al. (2023).** Informed machine learning – A taxonomy and survey of integrating prior knowledge into learning systems. *IEEE Transactions on Knowledge and Data Engineering*, 35(1), 614–633. [DOI](https://doi.org/10.1109/TKDE.2021.3079836)
- **Xu, J., Zhang, Z., Friedman, T., Liang, Y., & Van den Broeck, G. (2018).** A semantic loss function for deep learning with symbolic knowledge. *Proceedings of ICML*, PMLR 80, 5502–5511. [PMLR](https://proceedings.mlr.press/v80/xu18h.html)
- **Koh, P. W., et al. (2020).** Concept bottleneck models. *Proceedings of ICML*, PMLR 119. [PMLR](https://proceedings.mlr.press/v119/koh20a.html)
- **Khosla, P., et al. (2020).** Supervised contrastive learning. *NeurIPS 2020*. [Proceedings](https://papers.neurips.cc/paper_files/paper/2020/hash/d89a66c7c80a29b1bdbab0f2a1a94af8-Abstract.html)
- **Ahmed, K., et al. (2022).** Semantic probabilistic layers for neuro-symbolic learning. *NeurIPS 2022*. [Proceedings](https://proceedings.neurips.cc/paper/2022/hash/c182ec594f38926b7fcb827635b9a8f4-Abstract.html)
- **Marconato, E., et al. (2023).** Not all neuro-symbolic concepts are created equal: Analysis and mitigation of reasoning shortcuts. *NeurIPS 2023*. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/e560202b6e779a82478edb46c6f8f4dd-Abstract.html)
- **van Krieken, E., Minervini, P., Ponti, E. M., & Vergari, A. (2024).** On the independence assumption in neurosymbolic learning. *Proceedings of ICML*, PMLR 235, 49078–49097. [PMLR](https://proceedings.mlr.press/v235/van-krieken24a.html)
- **Raman, M., et al. (2021).** Learning to deceive knowledge graph augmented models via targeted perturbation. *ICLR 2021*. [arXiv](https://arxiv.org/abs/2010.12872)
- **Darwiche, A., & Marquis, P. (2002).** A knowledge compilation map. *Journal of Artificial Intelligence Research*, 17, 229–264. [DOI](https://doi.org/10.1613/jair.989) Relevant mainly to ECSI.

### 20.3 Statistical methodology

- **Holm, S. (1979).** A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70. [JSTOR](https://www.jstor.org/stable/4615733)
- **Efron, B., & Stein, C. (1981).** The jackknife estimate of variance. *The Annals of Statistics*, 9(3), 586–596. [DOI](https://doi.org/10.1214/aos/1176345462)
- **Ibragimov, R., & Müller, U. K. (2010).** t-Statistic based correlation and heterogeneity robust inference. *Journal of Business & Economic Statistics*, 28(4), 453–468. [DOI](https://doi.org/10.1198/jbes.2009.08046)
- **Giacomini, R., Politis, D. N., & White, H. (2013).** A warp-speed method for conducting Monte Carlo experiments involving bootstrap estimators. *Econometric Theory*, 29(3), 567–589. [DOI](https://doi.org/10.1017/S0266466612000655)

### 20.4 Internal sources

- [Core research plan — A2 section and appendix](../../../documents/core-research-plan.tex): equations $\ell_F,\ell_D$, primary estimands, $B_K$, $B^\star$, perturbations, replicates and statistical status.
- [Musicological memorandum — A2 section](../../../documents/musicological-memorandum.tex): musical interpretation of the relations, logical examples and the distinction between content and structure.
- [Appendix K — A2 technical protocol](../appendices/k.md) and [synthetic checks](../../../docs/research/a2/support/README.en.md).
- [Revised M1](m1-selection-decision.md) · [Revised M2](m2-eise-research-design.md) · [Musical position and family](../current/position-and-family.md) · [ECSI](ecsi/README.md).

## 21. Run registry and glossary

### 21.1 Run registry

The operational order of execution and the required technical checks are given in [Appendix K](../appendices/k.md#k10--criteria-fallbacks-and-timeline). Proposed fields for each fit:

```yaml
experiment: A2_knowledge_factorial
protocol_version: A2-2026-11-03
source_commit: <git commit>
representation_id: <R_star manifest>
m1_checkpoint_id: <M1 weights>
base_id: <b_r checkpoint>          # one per replicate r
replicate: <r in 1..5>
temperature: <T_r, fitted on D_int>
split_id: <H / D_base / D_int manifest>
mechanism: F_or_D
knowledge_status: V_or_P
perturbation_id: null_or_1_to_10
generator_seed: <seed>
lp_certificate: {d_F: <value>, d_D: <value>, primal_residual: <value>, duality_gap: <value>}
family_registry_version: <sigma registry>
concept_extractor_version: <version>
unknown_semantics_version: <version>
head_fit: {split: D_int, w: <values>, lambda_hat: <value>}
BK_version: <version>
Bstar_version: <version>
metric_definition_id: AP_fam-2026-11-03
statistical_plan_id: jackknife-t-G-1-2026-11-03
wallclock_seconds: <measured>
memory_peak_mb: <measured>
notes: <registered deviations>
```

The registry records the exact files and versions of annotations and specifications and distinguishes development material from independent evaluation data. Results per family, perturbation, replicate and provenance group remain available for reproducibility checks.

### 21.2 Glossary

| Term | Working definition |
|---|---|
| **Position (thesis)** | Musicologically identifiable melodic formation of variable length |
| **Historical type** | Historically attested name or morphological category |
| **Family of positions** | Versioned analytical hypothesis with a specification and a register of occurrences |
| **Occurrence** | Specific passage of a position in a work and source |
| **Realisation** | Concrete written or performed form of the position |
| **Diagnostic** | Testable musicological property or relation that bears on family membership |
| **Specification** $\sigma_{F,v}$ | Record of roles R/A/E, scope, supportive relations and version |
| **Knowledge validity (V/P)** | Valid versus controlled perturbed musicological content |
| **Flat use (F)** | Additive use of the three role summaries |
| **Structured use (D)** | The same additive use with a penalty for documented logical violation |
| **$B_K$** | Free linear comparator on the same concepts |
| **$B^\star$** | Strong neural comparator with SupCon, prototypes and concept supervision |
| **$\Delta_{\mathrm{know}}$** | Mean effect of content validity across mechanisms F and D |
| **$\Delta_{\mathrm{logic},V}$** | Effect of structured use under valid knowledge |
| **jackknife-t** | Original estimate divided by the delete-one-group standard error, referred to a Student $t$ with $G-1$ degrees of freedom |
| **IUT** | Intersection–union test of the ECSI confirmatory framework; it does not replace the two primary A2 tests |
| **Concept clamping** | Operational replacement of an estimated concept with a confirmed value, without automatic causal interpretation |

---

A2 is a controlled experiment for musicology-informed machine learning. **It separates the validity of a specification's content from the way that content is logically integrated** into a shared infrastructure for segmental recognition. It combines family hypotheses from source criticism, explicit logical rules, controlled perturbations, strong comparators and prespecified, calibrated statistical evaluation. The benefit concerns Byzantine musicology, which asks which relations establish the identity of a position. It also concerns symbolic MIR and machine learning, which ask how to measure the real value of adding valid scientific knowledge to a trained system.

[Home](../../README.md) · [Revised M1](m1-selection-decision.md) · [Revised M2](m2-eise-research-design.md) · [Appendix K](../appendices/k.md) · [Sources and versions](../reference.md)

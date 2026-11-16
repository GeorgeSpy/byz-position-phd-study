# Guide to research studies, codes and mathematical notation

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/start/study-codes-and-notation.md) · **English**
<!-- language-switch:end -->

[Home](../../README.md) · [Navigation](../../NAVIGATION.md) · [Terminology](../../TERMINOLOGY.md) · [Core research summary](research-summary.md)

This guide identifies the **programme-specific study codes**, model configurations and principal mathematical notation used throughout the proposal. Each entry links to its research specification. Standard abbreviations from the scientific literature are listed separately. In Greek prose, **Μ1** and **Α2** use Greek characters; the corresponding English designations **M1** and **A2** refer to the same studies.

**Documentation precedence.** The latest approved, study-specific specification determines the current design, together with verified sources and recorded research decisions. Earlier analytical chapters remain available as historical records. Research additions contained in a draft pull request are explicitly marked as **pending integration**.

## 1. Study and research-direction index

| Code | Research question or purpose | Detailed specification |
|---|---|---|
| **WP0 / WP1** (ΠΕ0 / ΠΕ1) | Source and rights inventories, annotation, feasibility, data preparation and assessment | [Data and feasibility (Greek)](../../../docs/full/08-data.md) |
| **M1** | Representation selection and joint identification of complete formula boundaries and family identity | [Selection rule J](../research/m1-selection-decision.md) |
| **M1-X** | The contribution of family-aware parameterisation and decoding/search to complete-formula recognition | [Architectural extension](../research/m1-x-design.md) |
| **A2** | Factorial 2×2 experiment on the validity of musicological knowledge and its structured incorporation | [A2 design](../research/a2-knowledge-design.md) · [Appendix K](../appendices/k.md) |
| **A2–S3** | Secondary investigation of complete formula extent: an accepted right endpoint versus truncation or extension, with known family and fixed start | [ByzCorpus overview](../research/byzcorpus/a2-s3-delimitation/README.md) · [Protocol](../research/byzcorpus/a2-s3-delimitation/protocol.md) · [PR #65](https://github.com/GeorgeSpy/byz-position-phd-study/pull/65) |
| **M2a** | Learning formula-family identity while preserving information specific to each realisation | [M2 methodology](../research/m2-eise-research-design.md) |
| **M2b** | Learning from verified historical co-exegeses and comparing against matched same-family supervision | [B2–EISE design](../research/m2-eise-research-design.md) |
| **M3a** | Independent musicological assessment of boundaries, family identity and relations among realisations | [Musicological validation (Greek)](../../../docs/full/07-validation.md#r052) |
| **M3b** | Listening study of human categorisation of formula families | [Categorisation study (Greek)](../../../docs/full/07-validation.md#r061) |
| **M3c** | Listening experiment on musical expectation and surprise at event and family levels | [Expectation study (Greek)](../../../docs/full/07-validation.md#r060) |
| **M4** | Performance timing and variability in recorded realisations | [Performance analysis (Greek)](../../../docs/full/07-validation.md#r063) |
| **M4-min** | Minimal external comparison of notated differentiation and performed timing variability for M2b | [M2 methodology](../research/m2-eise-research-design.md) |
| **M5** | Quantitative description of family distributions, sequences, functions and within-family differentiation across works | [Work characterisation (Greek)](../../../docs/full/09-nikolaos.md) |
| **M5-min** | Application of the selected model to complete held-out works and construction of morphological maps | [Core research summary](research-summary.md) |
| **ATL** | Learning historical morphological transformations between documented exegeses | [ATL](../current/atl.md) |
| **ATL-INV** | Inverse prediction of older notational choices from later exegesis | [Historical retrieval](../current/inverse-problem.md) |
| **Mθέσις / Mthesis** | Probabilistic operator modelling written formula realisations given family and musical context | [Definition](../current/m-thesis.md) · [Technical development](../current/m-thesis-technical.md) |
| **ByzCorpus** | Symbolic research corpus, annotation, segmentability and formula-family recognition | [Research infrastructure](../research/byzcorpus/README.md) |
| **ECSI** | *Evidence-Conditioned Selective Invariance*: separate extension in musicology-informed machine learning | [ECSI programme](../research/ecsi/README.md) |
| **Znamenny transfer** | Comparative extension investigating formula identity and transfer to Znamenny popevki | [Comparative research](../research/znamenny-transfer/README.md) |

**Main research sequence:** WP0/WP1 → M1 → A2 → M2a. M2b requires sufficient independently verified historical pairs and performance-based external assessment. M3a and M5-min support independent validation and application. M1-X, A2–S3, ECSI, ATL, ATL-INV, Mθέσις and cross-tradition studies retain separate research questions and decision criteria.

## 2. Model configurations and experimental identifiers

| Code | Meaning and context |
|---|---|
| **A / B / C (M1)** | Architectural comparison in M1. **A** is the principal semi-Markov full-span architecture; B and C are reference architectures. [M1](../research/m1-selection-decision.md) |
| **C_fac (M1-X)** | Factorised boundary and family model, trained with the same family supervision and input. [M1-X](../research/m1-x-design.md) |
| **F (ByzCorpus)** | Full-formula span-and-family scoring model. [Full formula versus composition](../research/byzcorpus/segmentation-and-family-recognition/02-full-position-vs-composition.md) |
| **C_comp (ByzCorpus)** | Composition of a complete formula from latent subsegments; distinct from C_fac. [Comparison](../research/byzcorpus/segmentation-and-family-recognition/02-full-position-vs-composition.md) |
| **LASM** | Experimental mechanism incorporating boundaries inferred for smaller statistical segments. [Multiscale boundary study](../research/byzcorpus/segmentation-and-family-recognition/03-multiscale-boundary-information.md) |
| **RM / DBC** | Models of family-aware subsegment composition. RM has synthetic tests; DBC remains an architectural design. [Family composition](../research/byzcorpus/segmentation-and-family-recognition/04-family-compositional-learning.md) |
| **V / P (A2)** | Valid and systematically perturbed musicological family specifications. |
| **F / D (A2)** | Flat/additive and structured/logical use of the same diagnostic concepts. **F** has a different meaning in the ByzCorpus architecture study. |
| **FV / FP / DV / DP** | Four cells of A2: mechanism F/D × knowledge condition V/P. A2–S3 reuses their model scores. [Appendix K](../appendices/k.md) |
| **R / A / E (A2)** | Required relations, sufficient alternative configurations and explicit exclusions in family specifications. |
| **B_K / B★ (A2)** | Freely weighted linear concept baseline / strong neural reference model. [A2 comparators](../research/a2-knowledge-design.md) |
| **B_L (A2–S3)** | Reference model controlling exact length per candidate family, articulation and text boundaries. [S3 protocol](../research/byzcorpus/a2-s3-delimitation/protocol.md) |
| **B0_sym / B0_profile (M2)** | Symbolic recognition baseline / direct historical profile of written differentiation. |
| **B1 / B2_fam / B2_main (M2)** | Shared neural baseline / family-based relational supervision / matched family condition for historical evaluation. [M2](../research/m2-eise-research-design.md) |
| **EISE** | *Exegesis-Invariant Segmental Encoder*: representation learning from verified co-exegeses of the same historical passage. [M2b](../research/m2-eise-research-design.md) |
| **ECSI-D / ECSI-F** | Dependent / factorised probabilistic models for diagnostic relations in ECSI. [Architecture](../research/ecsi/02-architecture.md) |
| **P0′ / P1′ / P2′ (ECSI)** | Feasibility inventory → specification dossiers → matched experiment. These are distinct from dissertation WP0/WP1. [Protocol](../research/ecsi/03-methods-and-gates.md) |
| **P-BYZ-…** | ByzCorpus experiment identifiers. **P-BYZ-A2-S3** denotes the dedicated delimitation study. [Experiment register](../research/byzcorpus/segmentation-and-family-recognition/08-decisions-and-evidence.md) |
| **R0–R4** | Historical inverse-retrieval protocol stages, distinct from the R/A/E diagnostic roles in A2. [ATL-INV](../current/inverse-problem.md) |

## 3. Principal mathematical notation

Full definitions, conditions and estimators are provided in the linked protocols.

| Symbol | Interpretation | Study |
|---|---|---|
| $U\times\Phi$ | Grid of three input units and four cumulative feature layers | [M1](../research/m1-selection-decision.md) |
| $N,T,M,L$ | Notational/melodic, timing, modal and text-related features | M1 |
| $R^\star$ / $R_A^\star$ | Operationally selected input representation for architecture A | M1 |
| $J$ / $\widehat J$ | Representation-selection rule and estimated selection score based on complete recognition | M1 |
| $F_{1,\mathrm{seg+fam}}$ | F1 requiring acceptable boundaries and the correct formula family | M1 |
| $B_x$ | Set of admissible boundary pairs for an occurrence in the matching protocol | M1 |
| $\mathcal F_0$ | Prespecified, fixed family set for evaluation | A2 / A2–S3 |
| $Q_R,Q_A,Q_E$ | Summaries of required, alternative and exclusion relations, each in $[-1,1]$ | A2 |
| $b_r$, $T_r$ | Baseline segment score and temperature for replication $r$ | A2 |
| $\lambda$, $\phi_f$ | Structured penalty parameter and logical family specification | A2 |
| $\mathrm{AP}_{\mathrm{fam}}$ / macro AP | Mean average precision across formula families | A2 |
| $\Delta_{\mathrm{know}}$ | Primary effect of knowledge validity | A2 |
| $\Delta_{\mathrm{logic},V}$ | Primary effect of structured versus flat use of valid knowledge | A2 |
| $z_{\mathrm{id}}$, $z_{\mathrm{real}}$ | Family-identity representation and realisation-specific information | M2 |
| $Q_{\mathrm{real}}$ | Diagnostic of preservation of realisation-specific information | M2 |
| $\Gamma_F$ | External profile of performance timing variability | M4-min / M2b |
| $\Delta_{\mathrm{hist}}=S_{\mathrm{EISE}}-S_{\mathrm{B2}_{\mathrm{main}}}$ | Principal comparison of historical and family-based supervision | M2b |
| $B_i$, $B_i^{a^\star}$ | Complete accepted boundary-pair set / subset sharing the preferred start | A2–S3 |
| $W_i$, $v^-$, $v^+$ | Shared local evaluation window, eligible truncation and extension | A2–S3 |
| $D_i^{(c)}(v)$ | Log-probability contrast of an accepted full extent against an alternative | A2–S3 |
| $D_{\mathrm{fam}},D_{\mathrm{seq}},D_{\mathrm{func}},D_{\mathrm{within}}$ | Family, sequence, functional and within-family differentiation measures | M5 |
| $\sigma_F$ | Source-grounded formula-family specification | ECSI |
| $q_\theta(z\mid x,c)$, $S_F(c)$ | Dependent diagnostic distribution and allowed set of states | ECSI-D |
| $m_F(x,c)$ | Probability that a family specification is satisfied | ECSI-D |

## 4. Established abbreviations

| Abbreviation | Expansion |
|---|---|
| **MIR** | *Music Information Retrieval* |
| **Symbolic MIR** | MIR based on symbolic musical representations |
| **MIML** | *Musicology-Informed Machine Learning* |
| **CRF / semi-CRF** | *Conditional Random Field* / semi-Markov segment-based variant |
| **NHPYLM** | *Nested Hierarchical Pitman–Yor Language Model* |
| **HMM / MDL** | *Hidden Markov Model* / *Minimum Description Length* |
| **AP / F1 / AUROC** | Average precision / harmonic mean of precision and recall / area under the ROC curve |
| **GLMM** | *Generalised Linear Mixed Model* |
| **SupCon** | *Supervised Contrastive Learning* |
| **LP** | *Linear probe*, a test of information accessible in an encoding |

## 5. Shared letters with distinct meanings

- **F** is the full-span model in ByzCorpus and the flat knowledge mechanism in A2.
- **A** denotes the main M1 architecture and a sufficient-alternatives role in A2.
- **R** denotes an input representation in M1, a required relation in A2 and stages R0–R4 in ATL-INV.
- **B0/B1/B2, B_K, B_L and B★** belong to different protocols; the subscript and study context determine the comparator.
- **S3** already names synthetic scenarios in M1 and source-group labels in the Gheorghiță inventory. The proposed new study is consistently **A2–S3**. [M1 scenarios](../research/m1-selection-decision.md) · [Source inventory](../research/corpus/README.md).
- **A2, A2–S3 and ECSI** have distinct methodological roles. A2 supplies the principal knowledge-validity experiment; A2–S3 reuses A2 scores in a secondary extent analysis; ECSI pursues a separate model of source-grounded specifications.

## 6. How to interpret evidence and earlier versions

Each claim should be read together with its evidence status: **synthetic/numerical check**, **exploratory study using real data**, **approved specification** or **planned assessment**. The completed Gregorian segmentation pilot and the future Byzantine evaluation involve distinct materials and metrics. [ByzCorpus](../research/byzcorpus/README.md).

[Earlier Greek glossary](../../../study/08_glossary.md) · [Source and version history (Greek)](../../../docs/maintenance/source-history.md) · [English translation status](../translation-status.md)

# Overview of the research proposal

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/start/overview.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Home](../../README.md) · [Summary of the core research](research-summary.md) · [Method map](../current/index.md) · [Documents and sources](../reference.md)

> **Programme structure:** The dissertation is organised around a coherent, implementable **core plan (M1, A2, M2a/M2b)** with independent expert validation (**M3a**) and full-work morphological mapping (**M5-min**). Around this core, **conditional extensions** (the probabilistic realisation operator *M-thesis*, historical transformations *ATL*, the inverse recovery problem *ATL-INV*, listening studies *M3b/c* and full *M5* style analysis) are activated as source availability and data adequacy permit.

## The musical and computational problem

How can a computational model locate the boundaries of a musical formula and recognise its identity when its written form, syllabic setting and degree of elaboration change? How does explicit musicological knowledge contribute to this recognition, and what do parallel transcriptions (*exegeses*) in the New Method allow us to recover from the historical transmission of the chant?

The proposal investigates these questions in the papadic repertoire of Cherubic Hymns and Communion chants (*Koinonika*). A **melodic formula** (*thesis*, θέση) is a historically grounded, structured melodic formation of variable length. A **family** is the analytical category that links occurrences sharing the same identity on the basis of explicit diagnostic criteria. Each **occurrence** is located in a specific work and source, while its **realisation** describes the particular melodic, rhythmic and syllabic form it takes there. [The four concepts, with an example](../current/position-and-family.md#a-schematic-example).

## What the dissertation will contribute

**In musicology**, the research determines which occurrences belong to the same family, which structural relationships persist across melodic variation and where divergences concentrate within a formula. At the same time, it examines what parallel exegeses of the same passage (co-exegeses) reveal and how formula selection and elaboration shape the compositional structure of complete works (extending to the compositional style of Nikolaos Protopsaltes of Smyrna and the recoverability of older notational distinctions).

**In music information retrieval (MIR)**, it identifies which symbolic representation supports joint boundary detection and recognition of this musical unit across complete works, even when occurrences differ in length and melodic surface. Evaluation incorporates alternative acceptable boundary placements, unknown families and challenging borderline cases.

**In machine learning**, it experimentally disentangles the substantive validity of expert knowledge from its structured logical composition (by comparing valid against systematically perturbed specifications) and tests whether the documented historical relationship between two co-exegeses provides a richer supervisory signal than a shared family label alone.

Optional cognitive studies further examine how family organisation relates to categorisation and melodic expectation among experienced listeners. [What each study will teach us](../review/knowledge-contributions.md) · [Contributions and previous research](../review/contribution-matrix.md).

## Core plan and conditional extensions

| Tier | Central task | Outcome |
|---|---|---|
| **Core plan (M1, A2, M2)** | Joint boundary detection and family recognition (M1), evaluation of musicological knowledge (A2), and representation learning from family pairs and co-exegeses (M2a/M2b). | Representation selection, specification evaluation, the EISE encoder and morphological maps of complete works (M5-min). |
| **Extensions (M-thesis, ATL, ATL-INV, M3b/c, full M5)** | Probabilistic realisation operator, historical transformations, inverse recovery of older notation, listening studies and compositional style analysis. | Profiles of exegetical transformation, a recoverability map and cognitive validation. |

## The core route (M1, A2, M2)

In the first stage (**M1**), twelve symbolic input combinations are compared. Built on these, a semi-Markov conditional random field (joint semi-CRF) learns to estimate jointly where an occurrence begins and ends and which family it belongs to, taking documented boundary ambiguities into account. Rule J selects the operational symbolic representation using complete formula-and-family recognition under architecture A.

**Complementary M1-X.** On the representation selected by J, a separate architectural study compares A with C_fac, a factorised model with matched family supervision, through marginal boundary decisions, K-best rescoring and global joint decoding. The two zero-order forms can express the same probabilistic model class with sufficient capacity. The study estimates the value of family-informed parameterisation as an inductive bias for boundary detection, while preserving the M1 selection rule and the inputs to A2/M2. [M1-X design](../research/m1-x-design.md).

Next (**A2**), keeping the trained M1 neural representation fixed, a $2\times 2$ factorial experiment measures how much the musicological validity of family specifications contributes compared with controlled perturbed rules, and what structured logical composition adds beyond simple additive scoring of the same diagnostic concepts.

The third pillar (**M2a/M2b**) examines how shared identity can be learned without losing realization-specific details, and **what the historical provenance of a musical relationship contributes to learning**: under strictly matched conditions, it compares learning from same-family pairs across different works against learning from verified co-exegeses of the same historical passage (EISE). External evaluation measures how closely each model's profile of written variation agrees with timing variability across audio recordings by different chanters (**M4-min**). Blind expert review (**M3a**) and morphological maps of complete unseen works (**M5-min**) complete the core evaluation.

[Detailed M1 design](../research/m1-selection-decision.md) · [M1-X architectural extension](../research/m1-x-design.md) · [A2 design](../research/a2-knowledge-design.md) · [Family and historical supervision in M2](../research/m2-eise-research-design.md)

## Conditional extensions: realisation operator and historical route

The **probabilistic realisation operator (M-thesis)** models which forms are expected when the family and its musical context are known, distinguishing the strictness of a specification from the relative frequency of compatible forms. In this way, family identity acquires measurable predictive content for organised melodic variation. [The operator's idea and definition](../current/m-thesis.md).

**Learning historical transformations (ATL)** examines how one exegesis expands, contracts or varies a passage relative to a parallel exegesis, aiming to identify regularities that generalise to families outside the training set. [Transformations between exegeses](../current/atl.md).

**Historical recovery (ATL-INV)** addresses the inverse question: because different notational choices in the older script can share the same metrophonic path, we test whether analytical exegesis in the New Method retains an additional trace of the original written choice beyond metrophonia, local context and already known exegetical rules. [The inverse problem](../current/inverse-problem.md).

Complementing these, listening studies (**M3b/M3c**) examine how family organisation relates to human categorisation and expectation, while **full M5** analyses formula sequences and the compositional individuality of Nikolaos Protopsaltes of Smyrna. [Independent evaluation (Greek)](../../../docs/full/07-validation.md).

## From sources to research outcomes

The research workflow begins with the passage inventory and the drafting of family specifications, proceeds through independent musicological validation and controlled model comparisons, and concludes with application to complete works.

The broader aim of the dissertation is to establish a methodology for musical traditions in which structural identity persists across diverse realisations and historical documentation provides substantive guidance for machine learning. Transferability to related modal repertories (such as Znamenny and Gregorian chant) is examined using their own musicological evidence and evaluation data.

[Core research plan (PDF, Greek)](../../../documents/core-research-plan.pdf) · [English short proposal](../../../documents/short-proposal-en.pdf) · [Greek short proposal](../../../documents/short-proposal.pdf) · [Detailed proposal — Greek PDF](../../../documents/analytical-proposal.pdf) · [Documents and protocols](../reference.md)

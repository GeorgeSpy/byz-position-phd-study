# Overview of the research proposal

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/start/overview.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Home](../../README.md) · [Method map](../current/index.md) · [Documents and sources](../reference.md)

## The musical and computational problem

How can the same melodic formula be recognised when its written form, syllabic setting and degree of elaboration change? And what does an analytical transcription (*exegesis*) in the New Method allow us to recover from the notation of an earlier manuscript?

The proposal investigates these two questions in the papadic repertoire of Cherubic Hymns and Communion chants (*Koinonika*). A **melodic formula** (*thesis*, θέση) is a historically grounded, structured melodic formation of variable length. A **family** is the analytical category that links occurrences sharing the same identity on the basis of explicit diagnostic criteria. Each **occurrence** is located in a specific work and source, while its **realisation** describes the particular melodic, rhythmic and syllabic form it takes there. [The four concepts, with an example](../current/position-and-family.md#a-schematic-example).

## What the dissertation will contribute

**In musicology**, the research determines which occurrences belong to the same family, which structural relationships persist across melodic variation and where divergences concentrate within a formula. It also examines which older notational distinctions remain recoverable through exegeses and how the compositional individuality of Nikolaos Protopsaltes of Smyrna is reflected in his choice, sequencing and elaboration of formulae.

**In music information retrieval (MIR)**, it identifies which symbolic representation supports joint boundary detection and recognition of this musical unit across complete works, even when occurrences differ in length and melodic surface. Evaluation incorporates both alternative acceptable boundary placements and challenging borderline cases (divergent realisations of the same family and superficially similar occurrences from different families).

**In machine learning**, it tests whether the documented historical relationship between two parallel exegeses of the same passage provides a richer supervisory signal than a shared family label alone. At the same time, comparing valid against controlled perturbed specifications disentangles the substantive validity of expert knowledge from its structured logical composition.

Finally, a cognitive extension examines how family organisation relates to categorisation and melodic expectation among experienced listeners. [What each study will teach us](../review/knowledge-contributions.md) · [Contributions and previous research](../review/contribution-matrix.md).

## Two routes sharing sources

| Route | Central task | Outcome |
|---|---|---|
| **Identity and variation** | Locate occurrences and recognise families in the continuous flow of the chant. | Morphological maps of formulae and a model of their variation. |
| **Historical transmission** | Compare exegeses and recover an older notational choice. | Profiles of exegetical transformation and a recoverability map. |

## The route of musical identity

In the first stage, we compare alternative symbolic representations of the notation. Built on the selected representation, models learn to estimate jointly where an occurrence begins and ends and which family it belongs to, taking documented boundary ambiguities into account.

The central representation-learning experiment examines **what the historical provenance of a musical relationship contributes to learning**: under strictly matched conditions, it compares a model trained on same-family pairs from different works against a model trained on verified co-exegeses of the same historical passage. External evaluation measures how closely each model's profile of written variation agrees with timing variability across independent audio recordings.

Complementing this, blind expert judgements and listening tests examine how family organisation relates to human categorisation and expectation, while the morphological application maps formula selection and elaboration across complete works by Nikolaos Protopsaltes of Smyrna.

[Recognition protocol (Greek)](../../../docs/full/05-m1.md) · [Comparison of supervision sources (Greek)](../../../docs/full/06-eise.md) · [Independent evaluation (Greek)](../../../docs/full/07-validation.md)

## The historical route and the operator

**Learning historical transformations** examines how one exegesis expands, contracts or varies a passage relative to a parallel exegesis, aiming to identify regularities that generalise to families outside the training set. [Transformations between exegeses](../current/atl.md).

**Historical recovery** addresses the inverse question: because different notational choices in the older script can share the same metrophonic path (the same sequence of quantitative interval movements), we test whether analytical exegesis in the New Method retains an additional trace of the original written choice. The two main comparisons measure, first, the information provided by the exegesis beyond metrophonia and local context, and second, its added value beyond already known exegetical rules. For passages preserved in two parallel exegeses, the contribution of the second exegete is evaluated separately against an independent reading of the older manuscript witness. [The inverse problem](../current/inverse-problem.md).

The **probabilistic realisation operator** models which forms are expected when the family and its musical context are known, distinguishing the strictness of a specification from the relative frequency of compatible forms. In this way, family identity acquires measurable predictive content for organised melodic variation. [The operator's idea and definition](../current/m-thesis.md).

## From sources to research outcomes

The research workflow begins with the passage inventory and the drafting of family specifications, proceeds through independent musicological validation and controlled model comparisons, and concludes with application to complete works. Neural modelling enriches the representation of variable-length sequences and their musical context.

The broader aim of the dissertation is to establish a methodology for musical traditions in which structural identity persists across diverse realisations and historical documentation provides substantive guidance for machine learning. Transferability to related modal repertories is subsequently examined using their own musicological evidence and evaluation data.

[English short proposal](../../../documents/short-proposal-en.pdf) · [Greek short proposal](../../../documents/short-proposal.pdf) · [Detailed proposal — Greek PDF](../../../documents/analytical-proposal.pdf) · [Documents and protocols](../reference.md)

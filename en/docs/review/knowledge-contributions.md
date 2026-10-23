# What the dissertation will establish

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/review/knowledge-contributions.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Concise statement and prior research](contribution-matrix.md) · [Overview](../start/overview.md) · [Methodological map](../current/index.md)

The dissertation aims to explain **how a melodic formula retains its identity across different notations, exegeses and performances**. It will establish which melodic relations constitute families, how their variation is organised, and which information from old notation remains recoverable in analytical renderings. It will also show how historical and musicological documentation can teach these relations to computational models.

## Musicological knowledge: four questions about the music

### Which occurrences realise the same melodic formula?

Historical names and morphological analysis provide starting points for comparing occurrences in Cherubic and Communion chants. The dissertation asks within what scope each named formula corresponds to a coherent family, when forms need to be distinguished by mode or genre, and when different names cover related material. Karagkounis's studies and comparative analysis of exegesis establish the question. [Morphological foundations (Greek)](../../../docs/musicology/02-variation.md).

Experts develop criteria on development material and apply them independently to new works. The resulting knowledge concerns **the scope and boundaries of the musical category**: a coherent family, a documented division, or ambiguity. Disagreements are analysed in relation to boundaries, modal interpretation and source legibility, distinguishing interpretative diversity from annotation problems. Analysts, editors and teachers gain comparable occurrences and reasoned alternative readings. [Definitions](../current/position-and-family.md) · [Independent family assessment (Greek)](../../../docs/full/07-validation.md#r052).

### What remains stable, and where does variation concentrate?

The dissertation compares internal regions of a family in written realisations and parallel exegeses. It examines which relations persist, where expansion and contraction concentrate, and how these tendencies change with musical context. Independent recordings additionally measure where contemporary chanters differ **in timing**.

The result identifies regions of relative stability and greater variability, and estimates agreement between written variation and contemporary temporal variation. Agreements and divergences are returned to specific passages and examined alongside tempo, phrase organisation and source provenance. Morphology and performance-practice research thereby gain a measurable relationship between two forms of variation. [Historical profiles and performance criterion (Greek)](../../../docs/full/06-eise.md#r045) · [Contemporary performance (Greek)](../../../docs/full/07-validation.md#r063).

### Which old written distinctions do the exegeses preserve?

Research on exegesis examines how particular older notations are rendered in the New Method. The dissertation adds a comparable test: among historical choices sharing the same metrophonia, **how well does the exegesis predict the label read in a specific old witness?** Comparison with metrophonia and context measures the total added value of exegesis; comparison with a predefined rule model measures its value beyond that comparator.

The musicological result is the distribution of this predictability by old distinction, exegete and context. It concerns nineteenth-century written exegetical practice and supplies evidence for the study of historical transmission. Arvanitis's “The Transcriptions of the Three Teachers: An Old or a New Sound?” places exegesis within this broader discussion. [Original article](https://doi.org/10.12681/eml.28005) · [Historical protocol](../current/inverse-problem.md).

The comparison will establish where recoverable information concentrates among old distinctions and what each exegete adds. For editors and scholars of exegesis, the finding connects the reading of an old passage with its particular analytical rendering. [Interpreting historical outcomes](../current/inverse-problem.md#interpreting-historical-outcomes).

### Where does Nikolaos of Smyrna's individuality lie?

The historical application distinguishes **composition through family selection** from **composition through family realisation**. It compares complete works by Nikolaos Protopsaltes of Smyrna with a chronologically controlled reference corpus, identifying the specific passages that produce differentiation.

Family selection and within-family realisation constitute the basic historical characterisation. Extended analysis additionally examines their succession and functional placement. Comparison with published analyses of Nikolaos connects quantitative profiles with particular compositional choices. The history of composition thus gains an answer about **how a composer differentiates his work** relative to a defined repertoire. [Full protocol and M5-min (Greek)](../../../docs/full/09-nikolaos.md).

## Music information retrieval: what the new task examines

The melodic formula combines a musicological category with an occurrence of variable extent in the continuous flow of chant. The dissertation examines how a system can recognise this unit while retaining documented alternative analyses.

| Question | Specific methodological step | What we will learn |
|---|---|---|
| How can joint boundary detection and family recognition be evaluated when several analyses are admissible? | Jointly compatible boundary sets, partial annotation, unknown families and a separate abstention decision. | How reference ambiguity affects performance and which occurrences are recognised reliably in new works. |
| Does learned similarity follow family identity when surface resemblance misleads? | Separate testing of documented hard positive and negative examples, including examples sharing metrophonia. | Which musical distinctions surface distance can capture and where additional relations are needed. |
| Which unit and information layers help each task? | Twelve input conditions compared under a common selection rule. Comparing explicit formulas, an event model and induced units is a separate structural-unit experiment. | When benefit is associated with encoding, features or organisation into musical units. |
| Which changes between exegeses can be predicted in new works and families? | Learning alignments and transformations from attested parallel passages, compared with rules and learned baselines. | Which regularities transfer and which families or contexts require a more local description. |

The contribution connects **formula-family identity, continuous symbolic input and source documentation** in a common recognition task. Learning historical transformations establishes which regularities of exegesis can be used to predict new realisations.

The corpus and protocol allow symbolic MIR researchers to compare systems using the same musicological distinctions and admissible analyses. [Recognition and input selection (Greek)](../../../docs/full/05-m1.md) · [Learning historical transformations](../current/atl.md).

## Machine learning: which knowledge changes prediction

### Provenance of positive pairs

The central experiment asks **what an attested historical relationship adds within the same family category**. The two conditions share architecture and family supervision and match exposure to data, difficulty characteristics and computational budget. The controlled difference is the choice of positive relations: shared family or verified co-exegesis of a specific passage.

Independent temporal variation in contemporary performances judges whether this difference leads to musically useful representations. Learning curves additionally examine how benefit changes with available historical material. The result will show which musical structure is learned from a shared historical passage and how much supervision of this kind is needed. [Estimating and interpreting the difference (Greek)](../../../docs/full/06-eise.md#τι-μαθαίνουμε-από-τη-σύγκριση-των-δύο-πηγών-εποπτείας).

The contribution to representation learning is a controlled way to assess the value of relational provenance in small corpora with rich documentation. Application in another domain requires its own relations and external criterion. [B2–EISE comparison (Greek)](../../../docs/full/06-eise.md).

### Knowledge content and how it enters the model

The experiment using correct or systematically perturbed knowledge, with simple or structured use, examines **which musical knowledge helps and how it is used**. Main effects and the interaction of the two factors estimate the value of knowledge correctness under each mode of incorporation.

Distinguishing content from use gives practical direction to model design: which musicological documentation is worth collecting and which mechanism can exploit it. The interaction shows when structured use specifically strengthens correct knowledge. [Musicologically informed learning and A2 (Greek)](../../../docs/research/machine-learning.md).

### Inverse prediction from dependent historical sources

The historical label is read in a specific old witness, with recorded uncertainty and a separate relation to the exegete's possible exemplar. Candidates share metrophonia and prediction is compared with both context and a predefined rule model. For two exegeses, a joint channel allowing statistical dependence is estimated.

The contribution connects **verifiable historical reference, source dependence and calibrated inverse prediction** in one problem. Source criticism establishes which relationships are attested; the probabilistic model assesses what each observation adds to label recovery. [Inverse problem](../current/inverse-problem.md).

### Specification selectivity and preference in practice

The probabilistic operator examines **what the family predicts about a realisation's form beyond musical context**. Evaluation distinguishes the selectivity of admissible forms from learned relative frequencies within the same admissible set. A common comparison basis identifies which compatible forms are preferred and how their frequencies change with musical context.

The research benefit is the distinction between a rule and its use: the specification describes the space of admissible forms and the empirical model describes the family's characteristic realisation. Prediction on independent occurrences tests how much musical knowledge this account provides. [Idea and definition](../current/m-thesis.md) · [Exact decomposition and conditions](../current/m-thesis-technical.md).

## Cognitive knowledge: family, categorisation and expectation

The human study asks **whether different realisations are perceptually organised by family** and **whether family succession explains additional variation in judgements of a continuation's unexpectedness**. Controls for surface distance and comparisons with event-level prediction establish the contribution of family organisation.

Results are examined by experience level and with uncertainty intervals. Cognitive research will learn for which listeners and under which conditions a historically documented family relates to categorisation and expectation. The two human hypotheses retain their own family of tests with Holm correction and the existing protocol. [Human tasks (Greek)](../../../docs/full/07-validation.md).

## Bibliographic starting points

- Karagkounis: [formula morphology and variation (Greek)](../../../docs/musicology/02-variation.md), [2003 bibliography entry (Greek)](../../../docs/bibliography/entries/b010.md).
- Arvanitis (2022), [The Transcriptions of the Three Teachers: An Old or a New Sound?](https://doi.org/10.12681/eml.28005).
- Wang, C.-i., Mysore, G. J., & Dubnov, S. (2017). [Re-visiting the Music Segmentation Problem with Crowdsourcing](https://archives.ismir.net/ismir2017/paper/000102.pdf). Proceedings of ISMIR 2017.
- Ristad and Yianilos: [learned edit distance (Greek note)](../../../docs/bibliography/methodology.md#s072), [original research](https://arxiv.org/abs/cmp-lg/9610005).
- Mavromatis: [computational modelling of contemporary chant and author publications](https://steinhardt.nyu.edu/people/panayotis-mavromatis).

The [contribution review record (Greek)](../../../docs/maintenance/contributions-review-2026-10-23.md) distinguishes verified bibliographic starting points from specific attributions requiring further examination.

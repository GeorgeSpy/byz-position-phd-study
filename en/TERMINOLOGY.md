# Terminology of the research proposal

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../TERMINOLOGY_GR.md) · **English** · [Translation progress](docs/translation-status.md)
<!-- language-switch:end -->

[Home](README.md) · [Overview](docs/start/overview.md) · [Method map](docs/current/index.md) · [Musicological documentation (Greek)](../docs/musicology/index.md)

This guide brings together the terminology used in the repository's reading pages. Its purpose is to identify each concept consistently across musicological analysis, symbolic music information retrieval (MIR) and machine learning. The English vocabulary follows the selected English short proposal.

## Musical units and evidence

| Term | Meaning and use |
|---|---|
| Neume | A graphic sign in musical notation. |
| Atomic event | A unit of the common computational reference layer. Its relationship to neumes is recorded in digital encoding. |
| Melodic formula (*thesis*, plural *theseis*) | A historically grounded, organised melodic formation of variable length. Historical name, family, occurrence and realisation are distinguished in the [definitions](docs/current/position-and-family.md). |
| Named historical formula | A type named or described in a specified source or analysis. Its correspondence with analytical families is documented. |
| Realisation | The symbolic content of an occurrence in a declared representation and at a specified level of analysis. |
| Occurrence | The localised presence of a formula in a passage of a particular work and source. |
| Performance | A chanter's vocal rendering. Computational procedures are described as being run, computed or applied. |
| Formula family | A testable analytical category with a versioned specification and a register of documented occurrences. Correspondence between historical name and family may be one-to-one, a split or a merger; families without an attested historical name are also recorded. |
| Catalogue melodic type | An entry in St Anthony's Monastery's catalogue. Catalogue attribution retains its own provenance. |
| Exegesis; plural exegeses | A documented analytical rendering of an older chant in a later notation. |
| Older witness | A specific older manuscript or other written document from which a historical notation is read. |
| Martyria | A notational indication of mode and pitch basis. Historical evidence is described as a source, treatise or document. |
| Scale degree, scale, echos (mode) | Musical concepts. Audio data are described as a recording or audio signal. |
| Transcription | In the terminology of the Greek reader, staff transcription. Conversion into machine-readable data is digital encoding. Historical publications may also use “transcription” for exegesis; their published titles are retained. |

The part–whole relationship connects atomic events, formula occurrences, formula sequences and the complete chant. A family classifies an occurrence through a membership judgement. The relationship between neume and event is recorded in digital encoding. Compound formulae, overlaps and alternative boundaries are declared at their respective analytical level.

## Specification, label and pair

A **family membership specification** contains diagnostic musical relationships, their scope, alternative sufficient configurations, exclusion criteria and numbered revisions of the rules.

The specification is developed from identified sources and development material, with justified revisions. Applying it to an occurrence produces a judgement of member, non-member or ambiguous. Independent evaluation uses the finalised version and separate material. Verified labels and documented historical relationships support the construction of positive training pairs. Each stage retains its own evidence and identifier.

**Diagnostic** describes musical relationships that distinguish a family. Technical checks are described as verification checks, compression measurements or separate measurements, as appropriate. A classifier used to examine a finalised representation is a **probe**.

## Representations and learning

| Concept | Consistent term |
|---|---|
| Converting primary source material into data | Digital encoding. |
| Selecting $`R`$, $`R^\star`$ or a cell of $`U\times\Phi`$ | Symbolic representation. |
| Neural network producing representations | Encoder. |
| Person judging boundaries, relationships and labels | Expert annotator. |
| Output $`z_{\mathrm{id}}`$ | Family-identity representation. |
| Output $`h_t`$ | Local state. |
| Fields $`N/T/M/L`$ | Feature layers. Each input variable is a feature. |
| Learning from labels or relationships | Supervision, supervised learning, relational supervision. |
| Learning without labels | Unsupervised learning. |
| Incomplete boundary or label information | Partial annotation. |
| Deciding the beginning and end of an occurrence in M1 | Boundary estimation. |
| General or statistical division of a sequence | Segmentation. |

EISE (Exegesis-Invariant Segmental Encoder) uses a relational term in M2 that attracts positive pairs. Family discrimination is supported by Conditional Random Field (CRF) scoring and a family-prototype term. Hard negative examples are used in independent evaluation.

The definitions of [ATL](docs/current/atl.md), [ATL-INV](docs/current/inverse-problem.md) and the [probabilistic operator](docs/current/m-thesis.md) retain their distinct prediction targets.

## Design and evaluation

| Concept | Term |
|---|---|
| Point after which rules or parameters are held fixed | Finalisation or freezing. In R4, encoder parameters receive no further updates. |
| Committing the design before inspecting evaluation data | Finalisation and preregistration. |
| Ranking tasks from 1 to 5 | Priority levels. |
| Size or granularity of the musical unit | Level of analysis or structural unit. |
| Comparison system | Reference model or baseline condition. |
| Quantity being estimated | Estimand. |
| Function measuring performance | Evaluation measure or metric. |
| Checking whether available data support an analysis | Adequacy criterion: sufficient, borderline or insufficient coverage. |
| Dataset for comparable tests | Evaluation corpus or benchmark. |
| Removing a component of a model | Ablation. |
| Estimating uncertainty by resampling groups | Cluster bootstrap. |
| F1 aggregated across all boundaries | Boundary micro-F1. |
| Area under the receiver operating characteristic curve | AUROC. |
| Representative member with the smallest total distance from the others | Family medoid. |
| Testing whether a distinction transfers across conditions | Cross-Condition Generalization Performance (CCGP). |

Cross-entropies and information quantities in the reader are expressed in **bits**, using base-2 logarithms. The reference unit is stated each time, for example per event, historical label or realisation. Conversion from an older information measure uses $`\mathrm{CE}_{\mathrm{bits}}=\mathrm{CE}_{\mathrm{nats}}/\ln 2`$. Logarithms in timing models and training losses follow their own mathematical definitions.

## Consistent writing

The Greek reader introduces a Greek term followed once by its English counterpart. The English reader uses the corresponding English term and introduces specialist Greek terms where needed. Established method names, acronyms, bibliographic titles and data identifiers retain their spelling. Claims specify a concrete task, evidence and outcome in direct language.

Terminological editing applies to the reading pages. Original PDF and LaTeX files remain records of their submitted versions. Technical field names such as <code>type_signature_version</code>, <code>frozen</code> and <code>scale</code> retain their schema spelling; their explanations follow this terminology.

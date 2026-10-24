# Melodic formula, family, occurrence and realisation

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/current/position-and-family.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Method map](index.md) · [Historical concept (Greek)](../../../docs/musicology/01-history.md) · [Variation (Greek)](../../../docs/musicology/02-variation.md) · [Families (Greek)](../../../docs/musicology/03-families.md) · [Terminology](../../TERMINOLOGY.md)

A **melodic formula** is a historically grounded, organised melodic formation of variable length. The research distinguishes the historically named type, the analytical family, the specific occurrence in a work and source, and its symbolic realisation. These distinctions connect musicological evidence with the units of annotation, prediction and evaluation.

## Why the formula family is the central analytical category

A Byzantine melodic formula is not merely a sequence of pitches that happens to recur. Historical theory treats the *thesis* as an organised combination of musical signs constituting *melos*; comparative musicological work recognises formulae across works, composers and modes even when their metrophonic or notational realisations differ. Karagkounis (2003, pp. 714–715, 783–789, 810–811) offers a particularly concrete precedent: he compares recurring formulae, documents variants and distinguishes passages with comparable metrophonia but different notational organisation. His quotation of Manuel Chrysaphes on p. 714 is a mediated citation, not a substitute for direct examination of Chrysaphes's critical edition.

The **formula family** is selected as the *central analytical category* because it relates occurrences of a musicologically supportable melodic type across individual passages without reducing shared identity to surface similarity. It is the intermediate level at which we can examine **what remains recognisable, what varies, and under which musical conditions**. It does not replace the historical name, individual occurrence or formula sequence; rather, it relates these levels through testable correspondences.

| Alternative unit or relationship | What it provides | What it cannot establish by itself |
|---|---|---|
| Metrophonic sequence or algorithmic proximity | Retrieval of candidate similarities and challenging examples | Shared melodic identity where notational agency or internal organisation differs |
| Historical name or catalogue grouping | Evidence of tradition, nomenclature and functional classification | A unique one-to-one correspondence between a name or catalogue section and one family |
| Single occurrence or historical exegesis of a passage | A specific witness and a link between older notation and its rendering | Membership of the same type across other works and independent passages |
| Shared mode, cadence or syntactic role | Musical context and functional comparability | Distinction among multiple formulae serving the same function |
| Whole phrase or chain of formulae | Analysis of succession and recombination | The identity of each constituent formula |

This choice is **musicologically grounded and empirically testable**, rather than true by definition. Held-out evidence must show whether a family specification distinguishes confusable types, recognises documented variants, and contributes explanatory or predictive information beyond simpler representations. The comparative *tune-family* literature (Volk & van Kranenburg, 2012, [DOI](https://doi.org/10.1177/1029864912448329)) supports examining family-specific criteria rather than presuming one universal feature; it does not make the traditions or analytical scales equivalent.

The same family framework supports musicological annotation, recognition of variable-length formulae, analysis of within-family variation and the controlled historical B2–EISE comparison. The family is thus **the object that musicology-informed machine learning aims to learn and test**, not merely a label derived from a similarity algorithm.

## Four objects

| Object | Meaning | Symbol on this page |
|---|---|---|
| Named historical formula | A type named or described in a specified source or analysis, such as the Lygisma formula. | $`T_{\mathrm{hist}}`$ |
| Formula family | An analytical category with a stable identifier, a versioned specification and a register of occurrences judged to be members. | $`F`$ |
| Formula occurrence | A localised passage in a particular work and source, with boundaries and syllabic correspondence. | $`o`$ |
| Symbolic realisation | The content of an occurrence in a declared symbolic representation and at a specified level of analysis. | $`X=R(o)`$ |

$`T_{\mathrm{hist}}`$ is distinguished from the timing layer $`T`$ of Study 1 (M1). $`F`$ denotes a family; the feature-set factor in M1 is denoted by $`\Phi`$ in the grid $`U\times\Phi`$.

## A schematic example

Suppose the analysis documents a family corresponding to the historically named **Lygisma formula**. The identifiers, work, source and boundaries below are hypothetical and illustrate the conceptual distinctions.

| Object | In the example |
|---|---|
| Historical type | The name “Lygisma formula”, with evidence from the relevant source. |
| Family | The hypothetical category F-DEMO, with version 2 of its specification for the stated repertory. |
| Occurrence | A passage of a hypothetical Cherubic Hymn setting in source S-DEMO, covering events 112 through 131 inclusive. |
| Realisation | This passage's particular sequence of melodic events, temporal values and syllabic distribution. |

A second occurrence may differ in extent, density or syllabic distribution. Membership in the same family is judged against the specification. The presence of the lygisma sign alone is insufficient for that judgement.

### Boundaries and musical context

For fully determined boundaries, write $`o=(w,s,[a,b),\ell_o)`$, where $`w`$ is the work, $`s`$ the source and $`\ell_o`$ the syllabic correspondence. Where boundaries admit several documented analyses, a set of acceptable pairs $`\mathcal B_o`$ is recorded, with the alternative realisation for each pair. The common mapping retains compatibility between the boundaries of different occurrences.

The **context** $`C`$ records the mode, functional role, text, prosody and permitted neighbouring material of an occurrence. A family specification may constrain these fields. The particular context value belongs to the occurrence, while its permitted range belongs to the specification's scope.

## Two organisational relationships

| Relationship | What it connects |
|---|---|
| Part–whole | Atomic events, a formula occurrence, a formula sequence and a complete chant, at the stated level of analysis. |
| Instance–type | An occurrence and a family, through a documented membership judgement. |

A family is the occurrence's category. Graphic notation is connected to atomic events through digital encoding; the neume-to-event mapping is recorded separately from melodic composition.

The relationship between historical names and analytical families is recorded as a documented correspondence:

```math
\mu\subseteq\mathcal T_{\mathrm{hist}}\times\mathcal F.
```

| Correspondence | Analytical case |
|---|---|
| 1:1 | One historical name corresponds to one adequately tested family. |
| 1:n, split | The same name covers distinguishable forms within the examined scope. |
| n:1, merger | Different names correspond to the same analytical category, with their distinct provenance retained. |
| No attested historical name | A family arises from analytical evidence and has a research identifier. |

Every correspondence records its source, notational stage, genre and justification. More complex relationships are recorded on the same basis if identified during the inventory.

## Specification and membership judgement

The **family specification** organises diagnostic relationships and their application rules:

```math
\sigma_{F,v}=(\mathcal D_F,\mathcal S_F,\mathcal A_F,\Gamma_F,v).
```

- $`\mathcal D_F`$ contains diagnostic predicates on $`(X,C)`$, with a stated notational level, source and judgement rule.
- $`\mathcal S_F`$ contains the minimal sufficient configurations of these predicates.
- $`\mathcal A_F`$ contains exclusion criteria.
- $`\Gamma_F`$ specifies scope: modes, genres, periods and level of analysis. Here it denotes the specification's domain of applicability.
- $`v`$ identifies the version.

Experts develop the specification from identified sources and development examples. Every revision has a justification and version; examples used to revise it remain development material. Diagnostic relationships from older notation are applied to New Method realisations through documented correspondence between the levels.

The **polythetic character** is examined through the alternative combinations of diagnostic relationships supporting membership. Multiple sufficient configurations can coexist with shared mandatory features: for example, $`\{d_1,d_2\}`$ and $`\{d_1,d_3\}`$ both require $`d_1`$. The inventory records shared, alternative and uncertain features. The [comparative study of tune families (Greek synthesis)](../../../docs/musicology/03-families.md) provides a methodological precedent.

For expert $`r`$, judgement uses the specification and the occurrence's permitted evidence:

```math
J_r(o;\sigma_{F,v})\in
\{\text{member},\text{non-member},\text{ambiguous}\}.
```

Missing necessary evidence and unresolved disagreements are retained as ambiguity. After the declared procedure for combining judgements, the membership register in the inventoried corpus $`D`$ is

```math
\mathcal E^{D}_{F,v}
=\{o\in D:J^*(o;\sigma_{F,v})=\text{member}\}.
```

Within this corpus, the family is described by its specification and register, $`F=(\sigma_{F,v},\mathcal E^{D}_{F,v})`$. Computational models receive $`F`$ as a category identifier. The evaluation register is kept separate from training data. Independent experts test the finalised specification on new occurrences: this is the meaning of a **testable analytical hypothesis**.

## Musicological criteria for identity and family membership

Membership is judged from a **musicologically justified combination of relationships specific to the type under investigation**. No single melodic “skeleton” has been established as a universal necessary feature of all Byzantine formulae. Some types may support a diagnostic core, others several permissible configurations or a constrained polythetic account. Their boundaries must be established from sources, comparisons and independent tests.

| Function of criteria | Musicological dimensions | Question to test |
|---|---|---|
| **Diagnostic organisation** (K1, K3, K4) | Melodic syntax, characteristic movements, internal articulation and approach to cadence; notational configuration and the agency of signs where observable | Which relationships distinguish the proposed type from confusable formations? |
| **Context and permissible variation** (K2, K6, K7) | Local modal behaviour, degree, genus, prosody, syllabic distribution, genre, style and placement in the chant | Which changes remain compatible with the type, and which fall outside the specification's scope? |
| **Historical and practitioner evidence** (K5, K8) | Historical nomenclature, manuscripts, exegeses, teaching and oral knowledge, and judgements by experienced cantors | What supports the hypothesis of identity without reusing the same evidence as both definition and independent validation? |
| **Comparability and discrimination** (K9, K10) | Boundaries, analytical scale, part–whole relations, nearest confusable types and challenging negative examples | Are the units comparable, and are there examples that genuinely discriminate between types? |

### Historical cases informing the specifications

**Karagkounis (2003, p. 783)** explicitly compares common notational-melodic formulae across Cherubic Hymn settings by different composers without taking metrophonia or the grounding pitch as the sole criteria. On **pp. 784–785**, he traces the opening **parakletike**, including changes in notation and the occasional absence of the lygisma. On **p. 788**, he separates the **antikenoma** from metrophonically similar configurations associated with **lygisma** or **heteron parakalesma**, on the grounds that the great hypostases distinguish those particular formulae. On **pp. 810–811**, he compares older and analytical notation and describes a recurrent exegetical rendering of the parakletike across specified compositions. These passages furnish *candidate* positives and challenging negatives, not automatically validated families.

The relationship between modal degree and realisation is also attested by **Chrysanthos, §408**, as quoted by Karagkounis (2003, p. 715 n. 28), concerning parakalesma on Pa and Vou. A different melodic rendering under a shared historical name **does not, by itself, demonstrate** that the two forms constitute one analytical family; that remains a comparative hypothesis. Gheorghiță (2010, [article](https://www.scia.istoria-artei.ro/resources/2010/02_NICOLAE%20GHEORGHITA_technique_of_transcription.pdf)) on Communion-chant exegeses and Tsogias (2018, [repository record/abstract](https://pergamos.lib.uoa.gr/item/uoadl:2846915)) on the Doxastarion of Iakovos provide further contexts for testing modal variation and interactions with neighbouring formulae respectively. Where the full musical examples have not been inspected, these remain leads for further examination.

### From candidate to tested family

The workflow distinguishes **(a)** collecting historical names and identifiable occurrences, **(b)** developing a type-specific specification with stated analytical scale, context, permissible changes and exclusions, **(c)** separating definition evidence from independent test evidence, **(d)** finalising the specification and asking independent experts to judge new occurrences, and **(e)** recording disagreements, revisions and versions.

A candidate family identifier is not a validation claim. **Assessability is checked before** the existing three-way judgement of **member / non-member / ambiguous**: insufficient notational observability may lead to **not assessable**, while an incompatible analytical scale or historical domain may lead to **out of scope**. Missing evidence is not evidence of a different type.

Judgements of **shared family**, **perceived melodic similarity**, **common function** and **historical relationship** are recorded separately: they can coexist and are not mutually exclusive. Examples used to develop or revise a specification do not count as independent tests. Challenging negatives include highly similar occurrences of a different type, alongside documented variants that may be less similar on the surface.

### Separating family and exegetical supervision

The family relationship concerns **identity at the type level**, potentially across distinct passages. **Co-exegesis** concerns different exegetical renderings of **the same particular passage**. A family specification may itself draw on historical evidence; what differs between B2 and EISE is the **provenance and topology of positive relational pairs**, under common family supervision and architecture ([M2](../../../docs/full/06-eise.md), [matching protocol F.1](../../../docs/appendices/f.md)). The contrast $\Delta_{\mathrm{hist}}=S_{\mathrm{EISE}}-S_{B2}$ evaluates agreement with the independent performance criterion on the common eligible support. On its own, it does not identify a “pure effect of the exegete”, because sharing the composition locus is an intrinsic property of the historical pairs.

<a id="κριτήρια-μουσικολογικής-οριοθέτησης"></a>

## What is insufficient to recognise a formula

| Indication or unit | Necessary distinction | Evidence in the Greek reader |
|---|---|---|
| An individual graphic sign or atomic event | It does not automatically identify a formula. Notational encoding is distinguished from the organised melodic formation analysed in the passage. | [Gabriel Hieromonachos and the intermediate unit](../../../docs/musicology/01-history.md) |
| Mere presence of a qualitative sign | A lygisma sign alone is insufficient to recognise the Lygisma formula; evidence for the melodic formation is needed. | [Karagkounis 2003/2005 and names](../../../docs/musicology/02-variation.md) |
| Metrophonic or surface similarity | The same metrophonia does not entail the same formula. Passages with different great hypostases may retain distinct musical identities. | [Karagkounis 2003, p. 788](../../../docs/musicology/02-variation.md) |
| A chain or sequence of formulae | It is distinct from an individual formula. A compound formula is declared and documented at its own analytical level. | [Karagkounis 2005, pp. 157–163, 175–176](../../../docs/musicology/02-variation.md) |
| A passage's connecting function | Function alone is insufficient for family membership. A connecting region is annotated separately; family attribution needs its own evidence. | [Karagkounis 2003, p. 192](../../../docs/musicology/02-variation.md) |
| A catalogue melodic type | An entry alone is not a validated family. It supplies a candidate relationship tested by a specification and independent judgement. | [Catalogue type and specification](../../TERMINOLOGY.md) |
| Functional role | A common role is insufficient for a common family. It is recorded in context and contributes to identity to the extent stated by the specification. | [Historical and functional context](../../../docs/musicology/01-history.md) |

Extent is assessed independently of syllabic division: a formula may span several syllables, while one syllable may contain successive formulae ([Karagkounis 2003, pp. 207, 209](../../../docs/musicology/02-variation.md)). These links lead to the reader's existing documentation and sources.

## Label provenance and independent evaluation

Each experiment records the fields available to the annotator and the information available before prediction.

| Use of the label | Research target |
|---|---|
| Description of a known realisation, with a label assigned from $`X`$ itself | Describe the distribution and the specification's selectivity. |
| Prospective prediction, with $`F`$ documented outside the masked target | Predict variants or masked material using external family information. |
| Family recognition from observed $`X`$ | Evaluate family classification under its own protocol. |

When a label is assigned from the diagnostic features of the same realisation, predicting those features incorporates the annotation rule. The result is reported as a description of that selectivity. Empirical preferences are studied on a common admissible set and independent realisations; prospective prediction uses family information available outside the target.

Holding out entire works and related sources tests generalisation. Checking the path from target to label additionally establishes the interpretation of prediction. Features outside the specification are examined alongside possible indirect dependencies on fields used in annotation.

In Study 2 (M2), family membership forms B2 pairs; historical co-exegesis forms EISE pairs. In the [probabilistic operator](m-thesis.md), family conditions the distribution of realisations. [ATL](atl.md) transfer to held-out families has its own generalisation scope.

## What these distinctions contribute

The four objects provide a **common unit for organising data and experiments**. The occurrence connects predictions with work and source; the family defines the recognition category and realisation condition; the specification makes musicological knowledge testable; and the realisation supports measurement of a particular variant.

This organisation supports recognition, prediction and historical comparison in the same framework. The methodological contribution lies in how these tasks use and test the relationships on independent material. The [overall contribution](../review/contribution-matrix.md#the-central-methodological-contribution) connects the objects with the intended research outcomes.

[Review of definitions and mathematical assumptions (Greek)](../../../docs/maintenance/position-family-review-2026-10-23.md)

# Melodic formula, family, occurrence and realisation

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/current/position-and-family.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Method map](index.md) · [Historical concept (Greek)](../../../docs/musicology/01-history.md) · [Variation (Greek)](../../../docs/musicology/02-variation.md) · [Families (Greek)](../../../docs/musicology/03-families.md) · [Terminology](../../TERMINOLOGY.md)

A **melodic formula** is a historically grounded, organised melodic formation of variable length. The research distinguishes the historically named type, the analytical family, the specific occurrence in a work and source, and its symbolic realisation. These distinctions connect musicological evidence with the units of annotation, prediction and evaluation.

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

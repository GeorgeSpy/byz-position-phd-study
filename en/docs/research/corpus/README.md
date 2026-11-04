# Preliminary inventory of the Byzantine chant research corpus

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/corpus/README.md) · **English**
<!-- language-switch:end -->

[Home](../../../README.md) · [Core research summary](../../start/research-summary.md) · [Research corpus: data dictionary](data/README.md) · [M1 methodology](../m1-selection-decision.md) · [M2/EISE research design](../m2-eise-research-design.md)

**4 November 2026 · Status: preliminary inventory based on published evidence; not a verified, model-ready corpus.**

This inventory surveys material for a symbolic research corpus using Nicolae Gheorghiță's study of the Sunday Communion chant (*koinonikon*) (2009, Part VII). It records metadata from the published comparative tables: mode, formula type, composer, exegete and printed page. The inventory contains **neither images nor symbolic transcriptions of the notation**. Reported counts are preliminary; manuscript readings, work identities, alignments and usage permissions require further verification.

This English edition contains the **complete inventory** and English-readable companion CSV datasets. The underlying Greek datasets and row identifiers are preserved as the source of record. English columns are supplemental descriptions; they are not independent musical transcriptions.

## 1. What the source covers

Gheorghiță examines **42 eighteenth-century Sunday koinonika, “Ainete ton Kyrion”**, comparatively in older notation and the New Method: eight by **Daniel Protopsaltes** (DP), 26 by **Petros Lampadarios the Peloponnesian** (PLP), and eight by **Petros Byzantios** (PB). The comparison draws on exegeses attributed to **Gregory Protopsaltes** (GP) and **Chourmouzios Chartophylax** (CC). Gheorghiță singles out **11 formulaic formations**, frequently designated by a characteristic great sign ([English-readable formula register](data/gheorghita2009_schemata.csv)).

As an earlier case, he also examines the **eight-mode koinonikon of Petros Bereketis**. The corpus register documents 11 source entries used in the comparative discussion, plus one additional footnote-only reference ([English-readable source register](data/gheorghita2009_sources.csv)).

Three groups of tables are relevant:

1. **Tables organised by mode (printed pp. 153–206).** Each row records one occurrence of a sign or formula in the selected repertory, with older notation, one or more New Method renderings, composer and exegete. According to footnote 194, the tables list all occurrences of the respective signs within this repertory. Such exhaustiveness is relative to the **notated sign and the selected works**.
2. **Synthesis tables (pp. 214–229).** Characteristic notational forms and their distribution across modes; relevant to musicological diagnostic specifications.
3. **Eight-mode Bereketis tables (pp. 238–249).** Fifteen structural units of the first section, presented in older notation and six modal renderings by Gregory.

## 2. Preliminary inventory results

**68 mode-specific tables and 338 occurrence rows** have been transcribed as metadata. The table counts agree with the references in §7.2.9; within each table, the extracted row count equals or exceeds the highest cited example number. This is a metadata-level consistency check.

| Formulaic formation (provisional English label) | Rows | Mode | Rows |
|---|---:|---|---:|
| 1. Kylisma | 52 | Mode I | 51 |
| 2. Parakalesma | 14 | Mode II | 51 |
| 3. Paraklitiki | 60 | Mode III | 41 |
| 4. Epegerma | 8 | Mode IV | 35 |
| 5. Oligon–hyporroe–oligon–epistrophe | 35 | Plagal I | 41 |
| 6. Argosyntheton / gorgosyntheton | 11 | Plagal II | 44 |
| 7. Xiron klasma | 13 | Varys (grave mode) | 46 |
| 8. Ison with klasma–epistrophe–eteron | 78 | Plagal IV | 29 |
| 9. Piasma | 52 | | |
| 10. Synagma | 10 | | |
| 11. Tromikon / psephiston–parakalesma | 5 | | |

By composer, the rows comprise **190 PLP**, **73 DP**, **73 PB** and **two unread composer cells**. These are row counts rather than counts of independently established works or family assignments.

### 2.1 Exegetical configurations

| New Method rendering as transcribed in the tables | Rows | Main association |
|---|---:|---|
| Gregory alone (GP_ONLY) | 206 | Almost all from Petros Peloponnesios |
| Gregory and Chourmouzios on one shared line (CC_GP_SAME) | 93 | Mainly Daniel and Petros Byzantios |
| **Separate Gregory and Chourmouzios renderings (CC_GP_SEPARATE)** | **35** | **All attributed to Daniel** |
| Chourmouzios alone (CC_ONLY) | 1 | |
| Unread (UNREAD) | 3 | |

An **anonymous rendering from BAR 955** occurs as an additional indication in **17 rows**.

The 35 separate-rendering rows are **candidates for further exegetical pair verification**. They are not yet 35 verified independent EISE pairs: manuscript/folio identification, passage alignment, relation type, family membership and dependence between witnesses must be checked. Likewise, the 93 shared-line cases should not be counted as two independently observed exegeses without additional primary evidence.

For Petros Peloponnesios, the tables use sets S2, S3 and S4, and in two modes also S41 and S42. A possible reconstruction is eight works in S2, eight in S3, six in S4 and two in each of S41/S42, giving 26. **This remains a work-identity hypothesis** requiring source verification.

## 3. Implications for the research programme

**M1 — joint segmentation and family recognition.** The tables contain **excerpts**, not continuous pieces. Complete New Method works must be obtained and encoded, for example from *Tameion Anthologias*. The table rows guide the localisation of formula occurrences within complete works. They cannot by themselves supply a full segmentation ground truth, and their coverage applies to the old-notation sign as written.

**A2 — the contribution of musicological knowledge.** Section 7.2.9 discusses notational combinations, subtypes, functional roles and places within the composition. These observations are candidate material for explicit, source-traceable family specifications. Occurrences used to formulate a specification must be separated from its blind evaluation.

**M2a — family-based supervision (B2).** Once independently validated, occurrences of the same family in different works or historical passages can be paired without direct exegetical or copy dependence.

**M2b — historical exegetical supervision (EISE).** The 35 rows with separately recorded Gregory and Chourmouzios renderings are found within the eight Daniel koinonika. They therefore provide a limited number of **independent compositions**, even if they yield several passage-level candidates. Gheorghiță also points to a common interpretative lineage, making dependence checks essential. A verified historical positive requires the same passage and separately supported family membership.

**ATL/ATL-INV — historical notation and realisation.** Each table associates older notation with a New Method rendering. This can guide retrieval and analysis of historical distinctions. The **argosyntheton**, not separately unfolded melodically by the exegetes in the cases described, provides a useful candidate negative control for recoverability, subject to direct source verification.

**Bereketis — held-out diagnostic set.** A common older notational exemplar with six modal renderings by Gregory is a potentially valuable controlled case of modal re-realisation. It is **reserved outside model training** in the current research protocol. The composer's eight-mode Cheroubikon in MPT 744 belongs to the same historical-dependence group.

## 4. Missing evidence and work required before modelling

1. **Witness-level provenance:** GP and CC labels in the comparative tables need manuscript shelfmark and folio for each occurrence.
2. **Composition identity:** composer, mode and S-set identifiers have not yet established 42 individually verified source-to-work records.
3. **Row-level musical content:** section of the piece, syllables, functional role, pitch and neumatic combinations require direct reading.
4. **Complete pieces and permissions:** M1 needs continuous New Method sequences and documented rights for working with the source material.
5. **Transcription accuracy:** the original inventory used OCR of the printed tables. **35 rows across seven pages were visually checked; the remaining 303 are marked OCR_DRAFT.** The review found one missing exegete, an empty row, an unrecognised one-row table and two pages (167–168) initially read incorrectly; these were manually corrected. OCR metadata should be treated as candidates until reviewed.
6. **Independence and leakage:** later splits must group related works, witnesses, exegetical lineages and modal versions before sampling train, development and test passages.

## 5. English-readable files

The English CSVs reproduce every original row and identifier, and **append English descriptive columns** to preserve lossless linkage with the Greek source records.

| Resource | Purpose |
|---|---|
| [Occurrence rows — 338 records](data/gheorghita2009_table_rows.csv) | Mode, formula, page, composer, set, exegetical configuration, verification state; English labels appended |
| [Mode-specific tables — 68 records](data/gheorghita2009_tables.csv) | Table/page indices and row counts, with English labels appended |
| [Formula descriptions — 11 records](data/gheorghita2009_schemata.csv) | English names, location, musical function, mode coverage and notes |
| [Source catalogue — 12 entries](data/gheorghita2009_sources.csv) | Eleven core source entries plus one footnote-only reference, with English bibliographic fields |
| [Verification template](templates/table_row_verification.csv) | Blank CSV with English field names for primary-source checking |
| [English data dictionary](data/README.md) | Field meanings, abbreviations, provenance and join strategy |
| [Extraction tool and usage](tools/README.md) | Documentation for the shared, English-commented Python OCR metadata script; scanned pages are not distributed |

The authoritative, original-text CSVs remain in the [Greek-source data directory](../../../../docs/research/corpus/data/). Codes such as GP, CC, S2, S41 and the opaque `work_key_hypothesis` values remain identical in both views; Greek notation inside an identifier is deliberately retained.

## 6. Next research steps

1. Verify every OCR-draft row against the published page using the verification template; add manuscript and folio for each rendering.
2. Identify the actual 42 compositions, their source witnesses and the complete New Method editions.
3. Encode the first complete works with **Neanes**; preserve the editable `.byzx` file, original source image reference and deterministic import into the research symbolic schema.
4. Locate each published table-row occurrence inside a full work; annotate boundaries and candidate family specifications, keeping unresolved cases explicit.
5. Establish independence groups for composers, works, witnesses, exegetes and historical lineages **before** constructing B2/EISE pairs and splits.
6. Extend the inventory with Stathis (historical formula concordances), Giannopoulos (Cretan reworkings and exegeses), and historically verified Cheroubika.

## Reference

Gheorghiță, N. (2009). *Chinonicul duminical în perioada post-bizantină (1453–1821). Liturgică și muzică*. Bucharest: Sophia. Part VII, printed pp. 126–253.

**Reading order:** [English inventory](README.md) → [English data dictionary](data/README.md) → [M1](../m1-selection-decision.md) / [A2](../a2-knowledge-design.md) / [M2](../m2-eise-research-design.md) → [English navigation](../../../NAVIGATION.md).

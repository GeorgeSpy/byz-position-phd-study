# Papadic Formulae — inventory of St Anthony's Monastery's papadic collection

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/corpus/st-anthony-papadic-formulae.md) · **English**
<!-- language-switch:end -->

[ByzCorpus](../byzcorpus/README.md) · [Source inventories](README.md) · [Data model](../../../../docs/research/byzcorpus/data-model.md)

**19 November 2026 · Source catalogue inventory**

## Source and scope

The [*Papadic Formulae* collection of St Anthony's Greek Orthodox Monastery](https://stanthonysmonastery.org/pages/papadic-formulae) brings together papadic melodic formulae from Cherubic hymns, Communion chants and other pieces. The catalogue organises the material by mode, cadence type, cadential pitch and lexical stress position. Editorially distinguished variants provide further evidence of relationships among the melodic examples.

The inventory draws on the consolidated 1,375-page PDF, with printed pagination 1001–2375, and the eleven corresponding Word documents. It records the modal divisions and catalogue headings, relating printed page references to PDF page numbers.

## Extent of the collection

The eleven documents contain **331 catalogue section entries**. The monastery identifies **758 source compositions**: 248 Greek-language Cherubic hymns, 101 non-Greek Cherubic adaptations, 351 Communion chants and 58 other compositions. The 331 entries describe the catalogue's organisation. A formula-level inventory will establish the number of individual musical examples and editorial variants.

| Modal division | Printed pages | Catalogue sections | Source compositions |
|---|---:|---:|---:|
| First Mode | 1001–1158 | 28 | 101 |
| Tetraphonic First Mode | 1159–1212 | 18 | 26 |
| Second Mode (soft chromatic) | 1213–1313 | 35 | 43 |
| Second Mode (hard chromatic) | 1314–1365 | 18 | 31 |
| Third Mode | 1366–1495 | 31 | 68 |
| Fourth Mode (Agia) | 1496–1695 | 36 | 124 |
| Fourth Mode (Legetos) | 1696–1734 | 19 | 8 |
| Plagal First Mode | 1735–1899 | 40 | 87 |
| Plagal Second Mode | 1900–2070 | 38 | 85 |
| Grave Mode | 2071–2201 | 32 | 87 |
| Plagal Fourth Mode | 2202–2375 | 36 | 98 |
| **Total** | **1,375 pages** | **331** | **758** |

Composition counts follow the monastery's published table; the section counts derive from the indexes of the eleven Word documents.

## Organisation of melodic formulae

The edition uses **1** for a stressed syllable, **0** for an unstressed syllable and **X** for a syllable with variable stress. Lexical stress is classified together with cadential function and cadential pitch. Coloured notation distinguishes editorially related variants, and grey notation identifies examples taken from non-Greek adaptations.

These features are preserved as source metadata. Their relationship to musicologically identified formula families will be investigated through family specifications and documented assessments of individual occurrences.

The editorial selection varies across source groups. Some compositions are represented by all their formulae, while for others the editors omit longer examples extending beyond four lines of notation. This distinction will inform subsequent research into melodic unit length.

## Inventory data

- [Modal divisions](../../../../docs/research/corpus/data/st-anthony-papadic-modes.csv): 11 records with identifiers, Word filenames, printed page ranges, section counts and repertory totals by genre. SHA-256 fingerprints identify the corresponding Word source files.
- [Catalogue sections](../../../../docs/research/corpus/data/st-anthony-papadic-sections.csv): 331 records with unique identifiers, original section labels, section titles, cadence groups, printed pages and PDF page numbers.

Original letters are retained, including repetitions. **AG** occurs twice in the Second Mode catalogue, while **V** and **W** recur in Plagal Fourth, with several instances of V. Seven affected rows are marked `SOURCE_LABEL_COLLISION` for comparison with the printed catalogue. The remaining 324 rows carry `TOC_EXTRACTED`. Both indicate entries derived from the source indexes.

## Towards formula-level symbolic data

The next inventory will register individual musical examples, their page locations, prosodic patterns, cadential pitches, notation and editorial variant relationships. Each example will be matched to its source composition, composer and witness. The monastery states that the Word documents provide information about the source title and composer when the pointer is placed over a formula.

Decoding the EZ font encoding will make it possible to associate catalogue entries with structured neumatic notation. Concordances with complete works will then identify individual occurrences, their boundaries and surrounding melodic context. Editorial groupings can subsequently be compared with the analytical families developed for ByzCorpus and with independent musicological assessments.

Continuous symbolic transcriptions of complete compositions will be central to statistical segmentation experiments. They preserve connective passages and the melodic context in which unit boundaries and lengths can be examined.

## Sources and rights

The monastery provides the musical catalogues, Word documents and source bibliography on its [official collection page](https://stanthonysmonastery.org/pages/papadic-formulae). The CSV datasets contain bibliographic and catalogue metadata linked to the original source. Redistribution of musical examples, Word documents and fonts will be examined separately in accordance with their terms of use.

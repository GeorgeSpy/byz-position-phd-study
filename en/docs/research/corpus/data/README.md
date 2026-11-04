# Gheorghiță corpus — English data dictionary

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά (original corpus)](../../../../../docs/research/corpus/README.md) · **English**
<!-- language-switch:end -->

[English inventory](../README.md) · [Greek original CSV directory](../../../../../docs/research/corpus/data/) · [Verification template](../templates/table_row_verification.csv)

## Data policy

These are **English-readable views of the four original CSV datasets**. Every row and original column is copied without modification, in the same order; English descriptive columns are appended. This is a metadata extraction, not a transcription of Byzantine neumes or an independently verified musicological reference set.

| File | Original rows | Added English columns |
|---|---:|---|
| [gheorghita2009_table_rows.csv](gheorghita2009_table_rows.csv) | 338 | `mode_en`, `schema_en` |
| [gheorghita2009_tables.csv](gheorghita2009_tables.csv) | 68 | `mode_en`, `schema_en` |
| [gheorghita2009_schemata.csv](gheorghita2009_schemata.csv) | 11 | `name_en`, `parts_of_the_koinonikon_en`, `function_in_the_source_en`, `modes_with_tables_en`, `note_en` |
| [gheorghita2009_sources.csv](gheorghita2009_sources.csv) | 12 | `shelfmark_or_edition_en`, `holder_en`, `date_en`, `notation_en`, `scribe_or_author_en`, `exegete_en`, `role_in_book_en` |

The 12-source file contains 11 main references and an additional `G09-X-1` item reported only in a footnote. This distinction matters when counting witnesses used in the analysis.

## Key fields and identifiers

- `row_id` is the stable identifier of an **extracted comparative-table row**; it is not a verified historical formula occurrence ID or an exegetical pair ID.
- `mode` retains the original Greek mode label. `mode_en` is a readable English gloss. The two are linked without recoding modal meaning.
- `formula` (integer 1–11) is the link between the occurrence, table and formula registers. `schema` retains the Greek label; `schema_en` supplies a descriptive transliteration/English gloss.
- `printed_page`, `printed_pages` refer to the **printed pagination**, not an automatically inferred image index.
- `composer`: `DP` = Daniel Protopsaltes, `PLP` = Petros Lampadarios/Peloponnesios, `PB` = Petros Byzantios, `UNREAD` = undeciphered.
- `petros_set`: `S2`, `S3`, `S4`, `S41`, `S42` are source-table group codes; their identification with distinct works remains **hypothetical**.
- `new_method_lines` counts the visual New Method lines in the comparison, not independent works.
- `exegete_per_line` is the raw GP/CC label transcription, and `exegete_configuration` is a derived categorical code:
  - `GP_ONLY`: Gregory only.
  - `CC_ONLY`: Chourmouzios only.
  - `CC_GP_SAME`: a shared line labelled for both; **not automatically two independently established renderings**.
  - `CC_GP_SEPARATE`: separately presented lines; **candidate** for primary-source pair verification.
  - `UNREAD`: unclear.
- `anonymous_bar955_line`: whether the table indicates an additional anonymous BAR 955 rendering.
- `work_key_hypothesis`: opaque working key combining composer, Greek mode and set code. It is preserved verbatim across languages; **do not use as a certified work identifier**.
- `verification`: `CHECKED_VISUALLY` (35 reviewed rows) or `OCR_DRAFT` (303 rows needing direct verification).

## Integrity and workflow

The English datasets must preserve the complete ordered original header and rows, with new columns appended only. For joins use `row_id`, `formula`, `source_id` and the explicitly documented table keys. Any substantive correction must first be entered into the source inventory and then regenerated in the English view.

Use the [verification template](../templates/table_row_verification.csv) to record specific **work identity, witness shelfmark and folio, passage, syllables, function, old/new sign content, great-sign colour, attribution and reviewer evidence**. Training labels should be issued only after primary-source checking, independent musicological review and the relevant task-specific acceptance gates.

**Source:** Gheorghiță (2009), Part VII, pp. 126–253, as catalogued in the [complete English inventory](../README.md).

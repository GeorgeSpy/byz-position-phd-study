# Karagkounis (2003, 2005): inventory of Cherubic hymns and melodic positions

[Corpus inventory](README.md) · [Greek edition](../../../../docs/research/corpus/karagkounis-2003-2005.md)

**15 November 2026 — Preliminary source-linked metadata inventory.** The dataset converts the numbered Cherubic hymn catalogues and selected musicological cross-references in Konstantinos Ch. Karagkounis (2003, 2005) into structured records. The corresponding original Greek CSV files are authoritative; field names are documented below.

## Dataset scope

| Source register | Count | Dataset |
|---|---:|---|
| Cherubic hymns in the 2003 catalogue | 933 | [all works](../../../../docs/research/corpus/data/karagkounis2003_all_works_1_933.csv) |
| Period VII, new compositions between 1814 and the late nineteenth century | 243 (subset) | [period VII](../../../../docs/research/corpus/data/karagkounis2003_period_vii_691_933.csv), [24 composer sections](../../../../docs/research/corpus/data/karagkounis2003_composers_period_vii.csv) |
| Three additional liturgical hymn catalogues in the 2005 book | 118 | [supplementary catalogues](../../../../docs/research/corpus/data/karagkounis2005_three_supplementary_hymn_catalogs.csv) |
| Named-position references tied to numbered Cherubic hymns | 206 references / 161 unique hymn IDs | [references](../../../../docs/research/corpus/data/karagkounis2003_named_position_work_references.csv) |

The supplementary hymn registers contain 23 *Tou Deipnou sou*, 22 *Sigisato pasa sarx*, and 73 *Nyn hai Dynameis*. These are separate from the 933 Cherubic hymns and carry `K05-THU`, `K05-SAT`, and `K05-PRE` record IDs.

## Selection and historical periodisation

Records **1–690 (periods I–VI)** are historical-core candidates for identifying positions and comparing earlier notation with New Method exegeses. Records **691–933 (period VII)** comprise a separate comparison stratum of new post-1814 compositions. This distinction reflects the source's periodisation. It does not assert that every earlier composition has an available New Method transcription.

The *Papadic Formulae* collection of [St. Anthony's Greek Orthodox Monastery](https://stanthonysmonastery.org/pages/papadic-formulae) offers a complementary source of formula examples from selected repertory, including nineteenth-century compositions. The project has not yet conducted a work-by-work match. **All** `st_anthony_match_status` values are `NOT_ASSESSED`; matching will require an exact work, composer, mode and witness/source identification.

## Named-position references

The 206 catalogue-number cross-references in printed pages **784–791** of the 2003 thesis link to catalogue numbers **5–680** only, covering **161 distinct work IDs**. None point to the 243 new compositions of period VII. Consequently, verifying the historical positions within later original compositions is a targeted follow-up investigation.

Reference groups: **Paraklitiki 88; Eteron Parakalesma 34; Antikenokylisma 8; Antikenoma 10; Tromikon–Lygisma section 66**. The references denote *catalogue-number mentions*, not 206 fully verified melodic spans. The `evidence_granularity` column records `CATALOG_NUMBER_CROSS_REFERENCE`.

Additional registers document candidate positions and chains, historical relations, scholarly observations and a [terminology crosswalk with Gheorghiță](../../../../docs/research/corpus/data/karagkounis_gheorghita_terminology_crosswalk.csv). Terminological overlap will be assessed against source notation, mode and structural role before any formula-family mapping.

## Field dictionary and quality

- `record_id` is the stable local catalogue key; `catalog_no` is the interpreted catalogue number; `catalog_number_on_page` preserves the number printed in the book, including discrepancies.
- `catalog_period` and `selection_stratum` separate source periodisation from **proposed** research selection. `NEW_COMPOSITIONS_VII_1814_19C` means source period VII; `HISTORICAL_I_VI_CANDIDATE` identifies possible historical-core material.
- `composer`, `composer_section`, `mode`, `designation` and `witness_reference_raw` hold extracted catalogue metadata. Many composer names for works 1–690 remain unassigned; manuscript citations and modes are provisional when affected by text-layer decoding.
- `pdf_page`, `printed_page`, `verification` and `source_document` preserve provenance. `SOURCE_TEXT_DRAFT` and `SOURCE_CROSS_REFERENCE_DRAFT` require direct inspection before research use.
- `st_anthony_match_status=NOT_ASSESSED` means that work-to-work matching has not been attempted; `position_annotation_status=NOT_ANNOTATED` means no symbolic pitch spans or expert boundaries are supplied.
- Catalogue numbers 327 and 690 have suspect printed numbers (321 and 670); source-analysis references 269 and 362 have conflicting composer attributions and are flagged for verification. Six main-catalogue works have unresolved modes (56, 291, 455, 575, 824, 895).

This release contains metadata and short scholarly descriptions. The underlying book PDFs, notation images and extensive verbatim passages are excluded. A [validation script](../../../../docs/research/corpus/tools/validate_karagkounis_inventory.py) checks the dataset's mechanical integrity; [manifest](../../../../docs/research/corpus/data/karagkounis_inventory_manifest.json) and [verification queue](../../../../docs/research/corpus/data/source_verification_queue.csv) document its status.

**Sources:** Karagkounis, Konstantinos Ch. (2003), *Η παράδοση και εξήγηση του μέλους των Χερουβικών της βυζαντινής και μεταβυζαντινής μελοποιίας*; Karagkounis (2005), *Παραλειπόμενα περὶ τοῦ Χερουβικοῦ Ὕμνου*; Gheorghiță (2009), *Chinonicul duminical în perioada post-bizantină (1453–1821)*.

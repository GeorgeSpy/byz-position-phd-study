# OCR metadata extraction — tool documentation

[English inventory](../README.md) · [English data dictionary](../data/README.md) · [Verification template](../templates/table_row_verification.csv)

The original [Python extraction script](../../../../../docs/research/corpus/tools/extract_gheorghita_rows.py) already has an English docstring and English-oriented command-line usage. The same maintained source is used by both editions to avoid divergence between two scripts.

It extracts **metadata only** from images of Gheorghiță's tables (printed pp. 153–206). It does **not** transcribe the musical notation, identify formula boundaries, prove family membership, or verify historical exegetical pair independence.

Requirements: Python, Tesseract, `pytesseract`, `opencv-python`, `numpy`. The script expects scanned page images with file names corresponding to the local PDF-page indices; the source page images are **not part of this repository**. Run only with legitimately obtained source images and the applicable usage permissions.

The output must be checked against the primary source, using [the English-column CSV views](../data/README.md) and [verification template](../templates/table_row_verification.csv). At the current inventory stage, **303/338 rows remain OCR_DRAFT**.

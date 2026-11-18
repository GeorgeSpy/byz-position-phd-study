# Melodic segmentation and the scale of musicological units

**Extended experimental study · Gregorian chant and the ByzCorpus research programme**

**Language / Γλώσσα:** [Full Greek research report](../../../../docs/research/byzcorpus/nhpylm-helsen-extended-experiments.md) · **English overview**

[ByzCorpus](README.md) · [Gregorian pilot](gregorian-nhpylm-helsen-pilot.md) · [M1-X](../../../../docs/research/m1-x-design.md) · [Annotated bibliography](../../../../docs/research/byzcorpus/nhpylm-helsen-bibliography.md)

## Research question and data

This study examines why unsupervised segmentation using the Nested Hierarchical Pitman–Yor Language Model (NHPYLM) identifies short recurring melodic segments and how those segments relate to Katherine Helsen's larger musicologically annotated elements. The evaluation corpus contains **136 responsories, 1,037 Helsen elements and 901 internal boundaries**, with a mean element length of **19.1 pitches**.

## Maximum segment length and corpus scale

Initial experiments on 75 unlabelled chants compared maximum segment lengths **7, 12, 20 and 30**, producing mean inferred segment lengths of **2.04, 3.27, 6.08 and 6.72 pitches**. This early 75-chant selection differs from the nested scaling samples used later.

In the nested experiment, `L_max=30` produced **7.80 pitches** at epoch 30 from **75 training chants** and **2.54 pitches** at epoch 30 from **300 chants**, measured on the same 46 held-out chants. With **839 training chants**, two independent runs reached **2.77 and 2.66 pitches at epoch 20**, compared with **2.56 and 2.43** at `L_max=7`. The ratio declined from **1.53/1.52 at epoch 10** to **1.08/1.09 at epoch 20**. Both full-data `L_max=30` runs stopped at epochs 20/21 following an environment restart, so the predefined epoch-30 criterion **K4 remains pending**.

The longer-segment setting achieved lower selected-path bits per pitch on the training pool but slightly worse scores on held-out works. These values are based on the selected segmentation and differ from the full marginal likelihood across possible segmentations.

## Boundary alignment and supervised models

NHPYLM identifies a dense set of candidate boundaries. Matched-density evaluation shows useful boundary-ranking information relative to chance and local interval cues, with varying margins across grouped folds. Many complete Helsen elements can be reconstructed as exact unions of induced subsegments; direct prediction of complete elements is rare.

A supervised melody-only BiLSTM achieved **boundary F1 = 0.562** (95% interval **0.531–0.595**) across three grouped folds and three random seeds. Adding NHPYLM boundary or segment-length inputs did not yield stable gains against shuffled controls. A full-element neural semi-Markov CRF (F) obtained **span F1 = 0.391** without text and **0.696** with text. Fixed-length LASM improved the melody-only result to **0.410** (difference **+0.019**, 95% interval **−0.006 to +0.045**). Joint element-and-family recognition is reported separately in the Greek study.

## Variation and architectural research

Only about **13%** of Helsen elements repeat as exact pitch sequences. Mean normalised edit distance is **0.39** between elements with the same analytical label and **0.70** between different labels of comparable length. This motivates explicit modelling of common family structure across melodic variations.

The next comparison considers full-span semi-CRF, semi-CRF with NHPYLM-derived segment features, family-aware PYHSMM and HMM with state merging and model selection via Minimum Description Length. These architectures are research plans, distinct from the executed Gregorian experiments.

## Transfer to Byzantine chant

The ByzCorpus **B-P1** experiment will evaluate candidate NHPYLM boundaries on Byzantine Koinonika and Cherubic hymns, with independent musicological annotations and separate intra-syllabic and inter-syllabic analysis. The M1-X study then addresses full formula-boundary and family recognition.

The **[Greek technical report](../../../../docs/research/byzcorpus/nhpylm-helsen-extended-experiments.md)** includes the full numerical tables, source references, execution conditions and preregistered evaluation criteria.

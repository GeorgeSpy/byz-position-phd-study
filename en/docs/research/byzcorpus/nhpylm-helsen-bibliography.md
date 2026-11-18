# Research Bibliography and Source Notes — Melodic Segmentation, NHPYLM, and Formula Families

**ByzCorpus research bibliography · 18 November 2026**

**Language / Γλώσσα:** [Ελληνικά](../../../../docs/research/byzcorpus/nhpylm-helsen-bibliography.md) · **English**

[Full experimental report](nhpylm-helsen-extended-experiments.md) · [ByzCorpus](README.md) · [M1-X](../m1-x-design.md) · [BibTeX](../../../../docs/research/byzcorpus/nhpylm-helsen-references.bib)

## Research context

This bibliography covers four connected areas: (a) musicological analyses that identify structural units in chant traditions; (b) unsupervised induction of statistical segments; (c) joint prediction of complete-unit boundaries and categories; and (d) the design of valid comparative evaluation protocols. Helsen's analysis provides the direct musicological reference for the Gregorian responsory experiments. The Byzantine study will draw on independent annotation of melodic formulae (*theseis*) and source-verified occurrences in Koinonika and Cherubic hymns.

The principal research question concerns the relationship between short statistical segments and the structural identity of larger melodic units across different realisations. It combines boundary inference, modelling of variation, and formula-family recognition in continuous symbolic sequences. The computational contribution is evaluated using common data, matched protocols, and direct ablations of individual architectural mechanisms.

## Relationship between prior work and the proposed experiments

| Research area | Principal precedents | Research question | Intended experimental use |
|---|---|---|---|
| Gregorian chant morphology | Helsen 2008, 2009; Lanz and Hajič 2025; Cornelissen et al. 2020 | Melodic segmentation and natural units | Grouped evaluation of boundaries, melodic similarity, and analytical family labels |
| Byzantine formulae and exegesis | Gheorghiță 2009, 2010; Karagkounis 2003; Mavromatis 2005/2006/2009 | Historical and musicological identity of formulae and their varied realisations | Independent annotations, family categories, and analysis of melodic relations |
| Bayesian nonparametric models | Teh 2006; Mochihashi et al. 2009; Goldwater et al. 2009 | Induction of short recurrent sequences | NHPYLM baseline, segment-length distribution, bits per pitch |
| Joint segmentation and categorisation | Uchiumi et al. 2015; Fujii et al. 2017 | Joint boundaries and latent labels with limited supervision | Melodic PYHSMM, supervision curves, families |
| Full-span structured prediction | Lafferty et al. 2001; Sarawagi and Cohen 2004; Kong et al. 2016 | Exact boundaries and segment identities | Semi-CRF A/C_fac, LASM, ablation studies |
| Structure selection | Stolcke and Omohundro 1992/1994; Rissanen 1978; Mavromatis 2009 | Learning shared states and selecting complexity | HMM/MDL architecture comparison |
| Experimental evaluation | Efron and Tibshirani 1993; Dror et al. 2018; Richard et al. 2024 | Paired comparisons, uncertainty, and domain-informed learning | Reproducibility, statistical decisions, musicological-knowledge contribution |

The musicological studies define and document the historical and analytical objects. The present extension examines them through systematic computational tests of joint boundary-and-family recognition and compares learning mechanisms on complete unseen works.

## A. Gregorian chant, digital corpora, and segmentation

### Katherine Eve Helsen (2008) — The Great Responsories of the Divine Office: Aspects of Structure and Transmission

**Publication:** Doctoral dissertation, Universität Regensburg. **Source:** [The Great Responsories of the Divine Office: Aspects of Structure and Transmission](https://doi.org/10.5283/epub.10769).

**Relevance:** The principal primary source for the analytical categories and accompanying appendix. The comparison uses specific annotated occurrences and boundaries, supported by a separate record of the CantusCorpus–Helsen alignment.

### Kate Helsen (2009) — The use of melodic formulas in responsories: constancy and variability in the manuscript tradition

**Publication:** *Plainsong & Medieval Music*, Cambridge University Press. **Source:** [The use of melodic formulas in responsories: constancy and variability in the manuscript tradition](https://www.cambridge.org/core/journals/plainsong-and-medieval-music/article/abs/use-of-melodic-formulas-in-responsories-constancy-and-variability-in-the-manuscript-tradition/D82597960C71064CD026D94E3A24DF3B).

**Relevance:** Examines both variability and continuity among melodic formations in Paris lat. 12044. It supports the distinction between an analytical label and the multiple melodic realisations associated with that label, without prescribing a computational architecture.

### Bas Cornelissen, Willem Zuidema, and John Ashley Burgoyne (2020) — Mode Classification and Natural Units in Plainchant

**Publication:** *Proceedings of ISMIR 2020*, pp. 869–875. **Source:** [Mode Classification and Natural Units in Plainchant](https://bascornelissen.nl/work/2020/mode-classification/ISMIR2020-paper.pdf).

**Relevance:** Investigates natural units and segmentation choices in plainchant modelling and their relationship to modal classification. The present study adds explicit assessment against Helsen's musicological boundaries.

### Bas Cornelissen, Willem Zuidema, and John Ashley Burgoyne (2020) — Studying Large Plainchant Corpora Using chant21

**Publication:** Seventh International Conference on Digital Libraries for Musicology. **Source:** [Studying Large Plainchant Corpora Using chant21](https://dare.uva.nl/id/db66bda1-ccdb-4c02-9ee0-dd20a341e893).

**Relevance:** Documents computational representations for large plainchant corpora and interoperability with musicological tools. It informs symbolic processing and source-data validation.

### Vojtěch Lanz and Jan Hajič Jr. (2025) — Gregorian Melody, Modality, and Memory: Segmenting Chant with Bayesian Nonparametrics

**Publication:** *Proceedings of ISMIR 2025*, pp. 638–646. **Source:** [Gregorian Melody, Modality, and Memory: Segmenting Chant with Bayesian Nonparametrics](https://doi.org/10.5281/zenodo.17811449).

**Relevance:** The immediate methodological precedent for applying NHPYLM to Gregorian chant. The independent reassessment of its default maximum segment length and comparison with Helsen annotations constitute new experimental questions in the present study.

## B. Byzantine melodic formulae, historical sources, and computational melology

### Panayotis Mavromatis (2005) — The Echoi [Modes] of Modern Greek Church Chant in Written and Oral Transmission: A Computational Model and Its Cognitive Implications

**Publication:** PhD dissertation, Eastman School of Music, University of Rochester. **Source:** [Author's academic page](https://steinhardt.nyu.edu/people/panayotis-mavromatis).

**Relevance:** Computational investigation of melodic organisation, modal relationships, and variation in modern Greek church chant. The dissertation provides an independent computational-musicological precedent for analysing melodic patterns and sequences.

### Panayotis Mavromatis (2006) — A Hidden Markov Model of Melody Production in Greek Church Chant

**Publication:** *Computing in Musicology*, 14, pp. 93–112. **Source:** [Computing in Musicology, volume 14](https://www.ccarh.org/publications/books/cm/vol/14/).

**Relevance:** Applies hidden Markov models to Greek church chant, addressing structural selection and relationships with accentuation, syntax, and melodic continuation. It informs the proposed investigation of shared structural states.

### Panayotis Mavromatis (2009) — Minimum description length modelling of musical structure

**Publication:** *Journal of Mathematics and Music*, 3(3), pp. 117–136. **Source:** [Minimum description length modelling of musical structure](https://doi.org/10.1080/17459730903313122).

**Relevance:** Develops an MDL criterion for HMMs over finite alphabets and demonstrates its use on a melodic example from Greek church chant. It offers a model-complexity selection mechanism distinct from the descriptive dictionary code constructed in Stage 3.

### Panayotis Mavromatis (2009) — HMM Analysis of Musical Structure: Identification of Latent Variables Through Topology-Sensitive Model Selection

**Publication:** *Mathematics and Computation in Music* (MCM 2009), Springer. **Source:** [Springer conference volume](https://link.springer.com/book/10.1007/978-3-642-02394-1).

**Relevance:** Topology selection and inference of latent states provide a comparative approach to linking related melodic realisations. The complete chapter should be consulted before attempting a technical reproduction.

### Nicolae Gheorghiță (2009) — Chinonicul duminical în perioada post-bizantină (1453–1821): Liturgică și muzică

**Publication:** Bucharest: Editura Sophia. **Source:** [Chinonicul duminical în perioada post-bizantină (1453–1821): Liturgică și muzică](https://www.academia.edu/49094074/Chinonicul_duminical_%C3%AEn_perioada_post_bizantin%C4%83_1453_1821_Liturgic%C4%83_%C8%99i_muzic%C4%83).

**Relevance:** Historical and morphological study of Sunday Koinonika, formula families, notational formations, and their exegeses. It guides source selection, annotation, and independent family verification in ByzCorpus.

### Nicolae Gheorghiță (2010) — Observations on the technique of transcription (ΕΞΗΓΗΣΙΣ) into the new method of analytical music notation of the Sunday koinonikon of the 18th century

**Publication:** *Studii şi Cercetări de Istoria Artei*, TMC series, 4(48). **Source:** [Observations on the technique of transcription (ΕΞΗΓΗΣΙΣ) into the new method of analytical music notation of the Sunday koinonikon of the 18th century](https://www.scia.istoria-artei.ro/2010.php).

**Relevance:** Musicological documentation of formulaic units in Koinonika and of the relationship between older notation and the New Method. The source examines 42 Koinonika and 11 significant formations.

### Konstantinos Ch. Karagkounis (2003) — Η παράδοσις και εξήγησις του μέλους των Χερουβικών της βυζαντινής και μεταβυζαντινής μελοποιίας

**Publication:** Doctoral dissertation, Athens. **Source:** [Author's publications](https://www.kxkaragounis.gr/αρθρα-δημοσιευσεις/).

**Relevance:** Principal study of Cherubic hymns, traditional formulae and older notation, and historical changes in composition. It provides source-based musicological analyses and specific claims to be examined against original corpus witnesses.

## C. Bayesian nonparametrics and joint induction of units

### Yee Whye Teh (2006) — A Hierarchical Bayesian Language Model Based on Pitman–Yor Processes

**Publication:** *Proceedings of COLING/ACL 2006*, pp. 985–992. **Source:** [A Hierarchical Bayesian Language Model Based on Pitman–Yor Processes](https://aclanthology.org/P06-1124/).

**Relevance:** Develops the hierarchical nonparametric prior associated with recurrent subsequences and heavy-tailed distributions.

### Daichi Mochihashi, Takeshi Yamada, and Naonori Ueda (2009) — Bayesian Unsupervised Word Segmentation with Nested Pitman-Yor Language Modeling

**Publication:** *Proceedings of ACL-IJCNLP 2009*, pp. 100–108. **Source:** [Bayesian Unsupervised Word Segmentation with Nested Pitman-Yor Language Modeling](https://aclanthology.org/P09-1012/).

**Relevance:** Introduces NPYLM for unsupervised segmentation of continuous character strings using blocked Gibbs sampling. This is the mathematical foundation for adapting the method to melodic symbol sequences.

### Sharon Goldwater, Thomas L. Griffiths, and Mark Johnson (2009) — A Bayesian Framework for Word Segmentation: Exploring the Effects of Context

**Publication:** *Cognition*, 112(1), pp. 21–54. **Source:** [A Bayesian Framework for Word Segmentation: Exploring the Effects of Context](https://doi.org/10.1016/j.cognition.2009.03.008).

**Relevance:** Studies the influence of context on segment induction. It informs controls over symbolic representation and the amount of contextual information available to the model.

### Kei Uchiumi, Hiroshi Tsukahara, and Daichi Mochihashi (2015) — Inducing Word and Part-of-Speech with Pitman-Yor Hidden Semi-Markov Models

**Publication:** *Proceedings of ACL-IJCNLP 2015*, pp. 1774–1782. **Source:** [Inducing Word and Part-of-Speech with Pitman-Yor Hidden Semi-Markov Models](https://aclanthology.org/P15-1171/).

**Relevance:** Introduces joint inference of segment boundaries and latent categories through PYHSMM. It provides an architectural precedent for a musical PYHSMM associating complete formulae with family categories.

### Ryo Fujii, Ryo Domoto, and Daichi Mochihashi (2017) — Nonparametric Bayesian Semi-supervised Word Segmentation

**Publication:** *Transactions of the Association for Computational Linguistics*, 5, pp. 179–189. **Source:** [Nonparametric Bayesian Semi-supervised Word Segmentation](https://aclanthology.org/Q17-1013/).

**Relevance:** Combines CRF and NPYLM for semi-supervised learning with labelled and unlabelled sequences. It motivates limited-supervision experiments on formula families.

## D. Structured prediction, HMMs, and model selection

### John Lafferty, Andrew McCallum, and Fernando Pereira (2001) — Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data

**Publication:** *Proceedings of ICML 2001*, pp. 282–289. **Source:** [Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data](https://people.cs.umass.edu/~mccallum/pubs.html).

**Relevance:** Establishes globally normalised conditional sequence models, a methodological reference for supervised boundary prediction.

### Sunita Sarawagi and William W. Cohen (2004) — Semi-Markov Conditional Random Fields for Information Extraction

**Publication:** *Advances in Neural Information Processing Systems*, 17. **Source:** [Semi-Markov Conditional Random Fields for Information Extraction](https://proceedings.neurips.cc/paper_files/paper/2004/hash/eb06b9db06012a7a4179b8f3cb5384d3-Abstract.html).

**Relevance:** The core mathematical reference for span-level label prediction and full-span features. Directly relevant to F/semi-CRF and M1-X architecture A.

### Lingpeng Kong, Chris Dyer, and Noah A. Smith (2016) — Segmental Recurrent Neural Networks

**Publication:** ICLR 2016. **Source:** [Segmental Recurrent Neural Networks](https://arxiv.org/abs/1511.06018).

**Relevance:** A neural joint model over boundaries and segment labels. It is an architectural comparison point for learning complete musicological units.

### Andreas Stolcke and Stephen Omohundro (1992) — Hidden Markov Model Induction by Bayesian Model Merging

**Publication:** *Advances in Neural Information Processing Systems*, 5. **Source:** [Hidden Markov Model Induction by Bayesian Model Merging](https://proceedings.neurips.cc/paper_files/paper/1992/hash/5c04925674920eb58467fb52ce4ef728-Abstract.html).

**Relevance:** Establishes HMM state merging as a method for inducing model structure from data and relates to the computational approach employed by Mavromatis.

### Andreas Stolcke and Stephen Omohundro (1994) — Inducing Probabilistic Grammars by Bayesian Model Merging

**Publication:** International Colloquium on Grammatical Inference (ICGI), LNCS/LNAI 862. **Source:** [Inducing Probabilistic Grammars by Bayesian Model Merging](https://arxiv.org/abs/cmp-lg/9409010).

**Relevance:** Extends the framework for merging probabilistic structures and selecting parsimonious model descriptions.

### Jorma Rissanen (1978) — Modeling by Shortest Data Description

**Publication:** *Automatica*, 14(5), pp. 465–471. **Source:** [Modeling by Shortest Data Description](https://doi.org/10.1016/0005-1098(78)90005-5).

**Relevance:** A foundational reference for Minimum Description Length and for distinguishing model-structure selection from descriptive compression exercises.

## E. Evaluation and musicology-informed machine learning

### Gaël Richard, Vincent Lostanlen, Yi-Hsuan Yang, and Meinard Müller (2024) — Model-Based Deep Learning for Music Information Research: Leveraging Diverse Knowledge Sources to Enhance Explainability, Controllability, and Resource Efficiency

**Publication:** *IEEE Signal Processing Magazine*, 41(6), pp. 51–59. **Source:** [Model-Based Deep Learning for Music Information Research: Leveraging Diverse Knowledge Sources to Enhance Explainability, Controllability, and Resource Efficiency](https://doi.org/10.1109/MSP.2024.3415569).

**Relevance:** Positions domain-knowledge integration within music information retrieval, particularly controlled evaluation of how knowledge and data contribute to model behaviour.

### Rotem Dror, Gili Baumer, Segev Shlomov, and Roi Reichart (2018) — The Hitchhiker’s Guide to Testing Statistical Significance in Natural Language Processing

**Publication:** *Proceedings of ACL 2018*. **Source:** [The Hitchhiker’s Guide to Testing Statistical Significance in Natural Language Processing](https://aclanthology.org/P18-1128/).

**Relevance:** Guidance on significance tests for sequential prediction models, including paired comparisons, multiple comparisons and transparent uncertainty reporting.

### Bradley Efron and Robert J. Tibshirani (1993) — An Introduction to the Bootstrap

**Publication:** Chapman & Hall. **Source:** [An Introduction to the Bootstrap](https://catalogue.library.cern/literature/fc0ns-p8v38).

**Relevance:** A foundational reference for bootstrap confidence intervals; here, independent works or melodic groups constitute the resampling units.

### Jouni Paulus, Meinard Müller, and Anssi Klapuri (2010) — State of the Art Report: Audio-Based Music Structure Analysis

**Publication:** *Proceedings of ISMIR 2010*, pp. 625–636. **Source:** [State of the Art Report: Audio-Based Music Structure Analysis](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C4/C4S1_MusicStructureGeneral.html).

**Relevance:** Broader framework for musical structure and segmentation at multiple scales. Its focus is audio, so it serves as a thematic comparison with the symbolic work reported here.

## Notes on use and interpretation

1. Helsen, Gheorghiță, and Karagkounis analyse different repertoires, source materials and structural scales. Cross-tradition comparisons will rely on annotations established independently for each tradition.
2. The Mochihashi, Uchiumi and Fujii studies address segmentation of linguistic data. Their use in music is an architectural transfer to be evaluated experimentally.
3. Mavromatis provides important computational precedents for Greek church chant. Exact methodological details should be checked against the original publications before numerical comparison with new ByzCorpus results.
4. The F, LASM and Stage 1–3 numerical results come from **this project's experimental records**. The cited literature provides methodological and mathematical precedents; the measured results are original findings of the present study.
5. Redistribution of data and complete PDF documents follows the respective licences. Public documentation therefore provides bibliographic links to the underlying sources.

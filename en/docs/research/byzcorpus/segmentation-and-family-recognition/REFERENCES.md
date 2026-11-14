# References and software

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../../../docs/research/byzcorpus/segmentation-and-family-recognition/REFERENCES.md) · **English**
<!-- language-switch:end -->

[Overview](README.md) · [Repository bibliography (Greek)](../../../../../docs/bibliography/index.md)

## Semi-Markov models and segmentation

1. Sarawagi, S., & Cohen, W. W. (2004). Semi-Markov conditional random fields for information extraction. *Advances in Neural Information Processing Systems 17*, 1185–1192.
2. Mochihashi, D., Yamada, T., & Ueda, N. (2009). Bayesian unsupervised word segmentation with nested Pitman–Yor language modeling. *Proceedings of ACL-IJCNLP 2009*, 100–108. [ACL Anthology P09-1012](https://aclanthology.org/P09-1012/).
3. Fujii, R., Domoto, R., & Mochihashi, D. (2017). Nonparametric Bayesian semi-supervised word segmentation. *Transactions of the Association for Computational Linguistics*, 5, 179–189. DOI: [10.1162/tacl_a_00054](https://doi.org/10.1162/tacl_a_00054). [ACL Anthology Q17-1013](https://aclanthology.org/Q17-1013/). Combines a CRF and an NPYLM for semi-supervised word segmentation. It is the closest methodological precedent for the two-scale coupling in [Section 3](03-multiscale-boundary-information.md), although both models there operate at the same segmentation scale.

## Gregorian chant

4. Helsen, K. E. (2008). *The Great Responsories of the Divine Office: Aspects of Structure and Transmission*. Dissertation, Universität Regensburg. DOI: [10.5283/epub.10769](https://doi.org/10.5283/epub.10769).
5. Helsen, K. (2009). The use of melodic formulas in responsories: Constancy and variability in the manuscript tradition. *Plainsong and Medieval Music*, 18(1), 61–76. DOI: [10.1017/S0961137109000965](https://doi.org/10.1017/S0961137109000965).
6. Lanz, V., & Hajič, J., Jr. (2023). Text boundaries do not provide a better segmentation of Gregorian antiphons. *Proceedings of the 10th International Conference on Digital Libraries for Musicology (DLfM 2023)*, 72–76. DOI: [10.1145/3625135.3625143](https://doi.org/10.1145/3625135.3625143).
7. Lanz, V., & Hajič, J., Jr. (2025). Gregorian melody, modality, and memory: Segmenting chant with Bayesian nonparametrics. *Proceedings of the 26th International Society for Music Information Retrieval Conference (ISMIR 2025)*, 638–646. DOI: [10.5281/zenodo.17811449](https://doi.org/10.5281/zenodo.17811449). [arXiv:2507.00380](https://arxiv.org/abs/2507.00380).
8. *CantusCorpus v0.2* (Cantus Database export). [Repository](https://github.com/bacor/cantuscorpus); [release v0.2](https://github.com/bacor/cantuscorpus/releases/tag/v0.2). Dataset licence: CC BY-NC-SA 4.0.

## Byzantine chant

9. Mavromatis, P. (2005). *The Echoi of Modern Greek Church Chant in Written and Oral Transmission: A Computational Model and Its Cognitive Implications*. Doctoral dissertation, Eastman School of Music, University of Rochester.
10. Mavromatis, P. (2005). A hidden Markov model of melody production in Greek church chant. *Computing in Musicology*, 14, 93–112.
11. Gheorghiță, N. (2009). *Chinonicul duminical în perioada post-bizantină (1453–1821). Liturgică și muzică*. București: Sophia. Part VII, pp. 126–253.
12. St. Anthony's Greek Orthodox Monastery. (n.d.). *Papadic Formulae*. <https://stanthonysmonastery.org/pages/papadic-formulae>.

## Software

13. Lanz, V. *nhpylm*. <https://github.com/lanzv/nhpylm>, revision `f928c78aa74ce44cd60a2f9b7c987167524c4d45`, MIT licence. The upstream code is not redistributed here.

Musicological references on Byzantine formula families are collected in the repository's [musicological documentation (Greek)](../../../../../docs/musicology/index.md).

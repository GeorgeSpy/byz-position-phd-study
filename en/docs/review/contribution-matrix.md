# Prior research, positioning and evaluation of the contribution

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/review/contribution-matrix.md) · **English** · [Translation progress](../translation-status.md)
<!-- language-switch:end -->

[Navigation](../../NAVIGATION.md) · [Research syntheses (Greek)](../../../docs/research/index.md) · [Questions and evidence (Greek)](../../../docs/start/review-guide.md) · [Methodological bibliography (Greek)](../../../docs/bibliography/methodology.md)

## The central methodological contribution

The dissertation aims to establish **which musical identity persists when a melodic formula changes its written form, exegetical development and performance realisation**. Comparison of Cherubic and Communion chants will show which relations constitute families, where their variation lies, and which old notational distinctions are systematically rendered in exegeses.

The computational research examines how this knowledge is learned: **which input unit preserves it, what the historical relationship between sources adds, and how the musical content of supervision changes prediction**. The result connects morphological research and source criticism with comparable experiments in recognition, realisation and historical recovery.

[Full development: question, research step and resulting knowledge](knowledge-contributions.md).

### Five connected contributions

| Contribution | Question | New knowledge |
|---|---|---|
| **C3 · Musicological knowledge** | Which occurrences constitute the same formula, where do they vary, what does exegesis preserve, and how does a composer differentiate his work? | Family scope and distinctions, internal morphology of variation, historical correspondences, and the distinction between selection and realisation. |
| **C1 · Symbolic recognition** | When does a model recognise family identity in occurrences of different extent and form? | Value of the input unit and features; behaviour on hard examples and alternative admissible analyses. |
| **C2a · Musical knowledge and historical supervision** | What does a shared historical passage teach beyond shared family, and how does expert knowledge help? | Added value and required quantity of historical supervision; effects of knowledge correctness and how it is incorporated. |
| **C2b · Transformation and historical recovery** | Which regularities of exegesis can be predicted in new material, and which old distinctions remain recoverable? | Transferable transformation profiles and additional information from exegesis beyond metrophonia, context and rules. |
| **C4 · Cognitive function** | How does family relate to listeners' categorisation and expectation? | Relationship between family organisation, musical experience and judgements of similarity or the unexpectedness of a continuation. |

### The role of the probabilistic operator

[Mθέσις](../current/m-thesis.md) examines **which musicologically compatible forms characterise practice**. It describes how family and context organise the choice of a particular realisation. The result distinguishes specification selectivity from empirical preferences and identifies how preferences change with context.

### Who can use the new knowledge?

Musicologists and editors gain comparable answers about formula identity, exegetical rendering and compositional individuality. Music information retrieval researchers gain a task testing musical identity within variation. Machine learning gains an experimental design assessing the value of relational provenance and knowledge content in small, richly documented corpora.

## Relation to prior research

The table connects the proposal's starting points to specific tasks and evaluation evidence. Targets b refer to the main bibliography; targets s refer to the methodological bibliography. Bibliographic notes, research syntheses and full protocols linked in this table are in Greek; the current method pages are in English.

| Field and relevant starting points | What has been studied | Specific positioning of the proposal | Evaluation |
|---|---|---|---|
| **[Formula and morphology](../../../docs/research/musicology.md)** — [Karagkounis 2003](../../../docs/bibliography/entries/b010.md), [Gheorghiță 2010](../../../docs/bibliography/entries/b060.md), [Arvanitis 2010](../../../docs/bibliography/entries/b004.md) | Named formulas, recurrence, morphological relations and changes in realisation. | Comparative examination of family scope, morphological distinctions and regions where variation concentrates. | [M3a](../../../docs/full/07-validation.md#r052) and [annotation C](../../../docs/appendices/c.md). |
| **[Symbolic MIR](../../../docs/research/symbolic-mir.md)** — [Cornelissen et al.](../../../docs/bibliography/entries/b047.md), [Lanz–Hajič](../../../docs/bibliography/entries/b088.md), [Karsdorp et al.](../../../docs/bibliography/entries/b081.md), [Polykarpidis](../../../docs/bibliography/entries/b012.md) | Representation units, segmentation, similarity and symbolic analysis in particular notations and corpora. | Recognition of musicologically defined variable-length formulas in the New Method and controlled input selection. | [M1](../../../docs/full/05-m1.md), [representations B](../../../docs/appendices/b.md), [baselines G.5](../../../docs/appendices/g.md#r185). |
| **[Machine learning](../../../docs/research/machine-learning.md)** — [Sarawagi–Cohen](../../../docs/bibliography/entries/b119.md), [Tsuboi et al.](../../../docs/bibliography/entries/b129.md), [Mahajan et al.](../../../docs/bibliography/entries/b091.md) | Structured segment prediction, partial supervision and use of shared-object relations. | Matched B2–EISE comparison varying positive-relation provenance with an independent criterion. | [M2](../../../docs/full/06-eise.md), [matching F](../../../docs/appendices/f.md), [losses G.3](../../../docs/appendices/g.md#r182). |
| **[Old notation and historical recovery](../../../docs/musicology/06-old-notation.md)** — [Alexandrou 2012](../../../docs/bibliography/methodology.md#s016), [Stathis 1978](../../../docs/bibliography/methodology.md#s011), [Knight–Graehl](../../../docs/bibliography/methodology.md#s053), [Snyder et al.](../../../docs/bibliography/methodology.md#s076) | Palaeographical and exegetical comparison of passages; inverse transcription and decipherment in other domains. | Historically read old label among metrophonically equivalent candidates; prediction from actual exegesis beyond rules and assessment of a second exegesis. | [ATL-INV: R0–R3, Δrule, Δ2ex](../current/inverse-problem.md). |
| **[Historical transformations](../current/atl.md)** — [Mongeau–Sankoff](../../../docs/bibliography/methodology.md#s060), [Ristad–Yianilos](../../../docs/bibliography/methodology.md#s072) | Comparison and alignment of musical or other sequences using rules or learned distance. | Probabilistic transducer between parallel exegeses of a shared historical passage, with transfer to new families. | [ATL](../current/atl.md), [independent pairs](../current/inverse-problem.md#from-inventory-to-historical-map). |
| **[Musicologically informed learning and operator](../current/m-thesis.md)** — [von Rueden et al.](../../../docs/bibliography/methodology.md#s083), [Richard et al.](../../../docs/bibliography/methodology.md#s071) | Incorporating knowledge in models and using musical constraints. | A2: correct/perturbed knowledge × simple/structured use; Mθέσις: distribution of realisations and added value of family over context. | [A2 in the current source](../../../sources/proposal-v878-candidate.tex#L705), [P0–P2 and Δfamily](../current/m-thesis.md). |
| **[Cognitive function](../../../docs/research/cognition.md)** — [Pearce](../../../docs/bibliography/entries/b109.md), [Mavromatis](../../../docs/bibliography/entries/b093.md), [Herff et al.](../../../docs/bibliography/entries/b074.md) | Probabilistic musical prediction, category organisation and hierarchical structure. | Independent tests of family similarity and additional I_F information for the same continuation. | [M3c/M3b](../../../docs/full/07-validation.md#r060), [human protocol I](../../../docs/appendices/i.md), [statistics E](../../../docs/appendices/e.md). |
| **[Exegesis and performance](../../../docs/research/performance-exegesis.md)** — [Stathis](../../../docs/bibliography/entries/b018.md), [Arvanitis](../../../docs/bibliography/entries/b033.md), [Panteli–Purwins](../../../docs/bibliography/entries/b105.md) | Historical exegeses, notation/practice relationships and quantitative performance measurements. | Comparing historical A(z) and contemporary Γ(z) in corresponding formula regions with assessed reliability. | [Independent M2 criterion](../../../docs/full/06-eise.md#r045), [broader M4](../../../docs/full/07-validation.md#r063). |
| **[Complete work](../../../docs/research/historical-analysis.md)** — [Karagkounis](../../../docs/bibliography/entries/b011.md), [Ioannidis](../../../docs/bibliography/entries/b007.md) | Specific compositional organisations and relationships to earlier tradition. | Separating differentiation through family selection from differentiation through realisation; extended analysis of succession and functional placement. | [M5 and Nikolaos](../../../docs/full/09-nikolaos.md). |
| **[Data and transfer](../../../docs/research/data-transfer.md)** — [Papadic Formulae](../../../docs/bibliography/entries/b126.md), [CantusCorpus](../../../docs/bibliography/entries/b055.md), [Gusev et al.](../../../docs/bibliography/entries/b065.md) | Cataloguing, digital corpora and computational reading of different traditions. | Verifiable provenance and splits; separate study of attested transformations and a second repertoire when adequate. | [Data](../../../docs/full/08-data.md), [D](../../../docs/appendices/d.md), [§6.5](../../../docs/full/06-eise.md#r049). |

## From claim to evidence

| Central claim to test | Required evidence | Research result |
|---|---|---|
| The family specification distinguishes family identity in new occurrences. | Development material, finalised specification and independent judgements. | Discriminative adequacy, agreement, ambiguity or need for further typological analysis. |
| Supervision from attested historical relations improves agreement between the representation and an independent performance criterion. | Matched B2–EISE scope and reliable independent performance criterion. | Estimate of Δ_hist, uncertainty interval and documented scope. |
| Exegesis preserves a recoverable trace of old notation beyond known rules. | Independently read H, metrophonically equivalent candidates, rule baseline and held-out works. | Co-primary Δrec and Δrule with Holm; separate Δ2ex on the same paired subset; musicological interpretation of recoverable distinctions. |
| Learned representations allow access to the old label. | Stabilised B1, B2 and EISE, identical H and controlled probes. | Separate R4 test, with B2 as an additional reference. |
| Family identity organises the distribution of realisations under a given context. | Family specifications, recorded label provenance, eligible F,C,X and common held-out works. | Δfamily and separate assessment of selectivity, within-family preferences and musicological acceptability. |
| Family relates to human categorisation and prediction. | Eligible stimuli, surface-distance controls and human protocol. | Separate H_cat/H_pred with the proposal's multiplicity correction. |
| A work profile supports historical interpretation. | Chronologically controlled Ω, adequate coverage and specific passages. | Description of differentiation in families and realisations, with dimensions from M5-min and extended analysis. |

## Interpretation and scope

The contribution forms a shared programme of a new symbolic MIR task, historically documented supervision, quantitative recovery of old notation and prediction of realised form. Its results return to specific musical sources and open new tests of the relationship between family identity, historical notation and analytical exegesis.

[Full literature foundation (Greek)](../../../docs/full/02-literature.md) · [Overall contribution (Greek)](../../../docs/full/10-contribution.md) · [Recent positioning text (Greek)](../../../docs/research/positioning-source.md)

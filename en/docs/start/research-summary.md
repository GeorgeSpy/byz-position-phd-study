# Summary of the core research

<!-- language-switch:start -->
**Language / Γλώσσα:** [Ελληνικά](../../../docs/start/research-summary.md) · **English**
<!-- language-switch:end -->

[Home](../../README.md) · [Core research plan (PDF, Greek)](../../../documents/core-research-plan.pdf) · [M1](../research/m1-selection-decision.md) · [A2](../research/a2-knowledge-design.md) · [M2](../research/m2-eise-research-design.md)

This page presents the core of the proposal, the studies M1, A2 and M2a, in three sections: research questions, proposed approach and expected contributions. Technical specifications are in the detailed page of each study and in the appendices. Their numerical values are initial proposals and will be set together with the supervisory team after the pilot study.

## The musical problem

Byzantine chant is the monophonic vocal music of Orthodox worship, transmitted for centuries through written tradition and oral teaching together. Its melodies draw on a vocabulary of traditional formations, the **melodic formulae** (θέσεις): melodic formations of variable length that recur from work to work, adapted to the mode (echos, the modal framework of the melody), to the scale degree and to the poetic text. Occurrences that share the same identity form a **family** of formulae.

The identity of a formula is not the same as surface similarity. Related melodic paths may belong to different families, the same formula unfolds with different length and shape, and its boundaries within continuous notation are not always unambiguous. The musicological question is therefore also a demanding problem of symbolic music information retrieval (MIR) and machine learning: a system must locate units of variable length, recognise their family and abstain when the evidence is insufficient.

The proposal approaches the problem through **musicology-informed machine learning**. Musicology defines the unit of analysis and the criteria of each family. How much this knowledge is worth, and how the model uses it, are examined as controlled experimental variables. The repertoire is the papadic Cherubic hymns and Koinonika of the New Method, the analytical notation established in 1814. These are slow, melismatic chants of the Divine Liturgy, where formulae are long and hard cases are frequent.

## 1. Research questions

> **Central question.** How can a melodic formula and its family be recognised within continuous notation when their realisation varies, and what does the musicological knowledge that defines the family contribute to this recognition?

The question is divided into three studies that use the same corpus and the same symbolic infrastructure.

**RQ1 — How the notation should be read (M1).** A formula can be read as a sequence of written signs, of elementary melodic movements or of neume groups, with or without information on timing, mode and text. Which reading allows the boundaries and the family of a formula to be estimated jointly? And how many boundaries are already explained by general melodic segmentation cues that know nothing about families?

**RQ2 — What musicological knowledge contributes (A2).** A family specification may require a particular cadence, allow one of several internal developments and exclude a modal change. Does the valid specification improve recognition compared with a deliberately perturbed specification of the same form? And does logically combining these relations add anything beyond using them additively?

**RQ3 — Identity and realisation (M2a).** Does learning from pairs of real occurrences of the same family, in different works, help to recognise the family? And does it do so without losing the musically important information of the particular realisation?

The core is deliberately limited, so that it is feasible within the doctorate. A historical strand of M2 (M2b) uses, where the sources allow, **exegeses**: historical renderings of the same older passage in the New Method, such as those of Gregorios the Protopsaltes and Chourmouzios the Archivist. This strand and the other extensions are activated only if prespecified criteria of data and source sufficiency are met.

## 2. Proposed approach

### Data

The works are encoded from files of Neanes, open-source software for writing Byzantine notation. The public *Papadic Formulae* catalogue of St Anthony's Monastery in Arizona, with formulae from 758 compositions, serves as a guide for locating material and candidate families. It is not, however, a ready corpus of complete works, so the inventory of available works, sources and licences is the first step of the work.

The target is 40–60 complete works with 8–12 families and at least 25–30 occurrences per family from at least five independent works. Experts annotate the boundaries and the family of each occurrence, and at least 30% of occurrences, together with all hard cases, are annotated blind by a second expert. The pilot study of the first six months tests the whole chain on three families, the parakletike, the kylisma and the piasma, starting from Gheorghiță's comparisons in Koinonika. It also measures annotation time and expert agreement, so that the scale of the corpus is decided on the basis of measurements.

### Representing the music

Each work is converted into a single symbolic form: a sequence of atomic melodic events, linked in both directions to the written signs, so that every automatic decision can be checked in the passage that produced it. An initial conversion infrastructure already exists. It will be tested on real works by restoring the original notation from the symbolic form.

On this form M1 compares twelve readings of the notation. It combines three input units (written sign, atomic melodic event, neume group) with four cumulative layers of information: notational, temporal, modal (echos, martyriai, phthorai) and textual (syllable, word, stress). The reading selected in M1 becomes the shared input of A2 and M2a.

### Models

**M1** uses as its main model a semi-CRF, a probabilistic model that scores whole candidate segments rather than single signs. It therefore decides jointly where a formula begins and ends and to which family it belongs. The model is compared with two-stage solutions that first find boundaries and then the family. It is also compared with an event-level Transformer, with general segmentation cues (local discontinuities as in LBDM, unexpectedness as in IDyOM, repetition of melodic structures) and with unsupervised statistical segmentation.

**A2** keeps the M1 model fixed and adds only the musicological knowledge. Family specifications are written as logical rules over musical concepts, e.g. cadence, internal development or modal change, which are extracted automatically from the notation. Four conditions cross a valid or deliberately perturbed specification with its additive or logical use. The perturbed specifications keep the form, frequencies and overlaps of the valid ones, so that the comparison concerns content only. Two strong reference models learn from the same concepts without a specification.

**M2a** compares three graded conditions. The first is the symbolic M1 model, without representation learning. The second adds a neural encoder that learns from family labels and from reconstructing the realisation. The third adds a term that brings together the representations of occurrences of the same family from different works. The encoder keeps family identity and the information of the particular realisation separate, so that it can be tested whether better recognition comes at the expense of variation.

### Evaluation

Works that share historical material, e.g. copies or renderings of the same passage, are always placed in the same part of the data. Performance is therefore not artificially raised by near-identical material in training and testing. An independent test set is defined early and opened once, after all choices have been made.

M1 measures how many occurrences are found with acceptable boundaries and the correct family. A2 and M2a measure how well the model ranks the real occurrences of each family, with average precision. M2a also measures how much information of the realisation is kept in the representations.

Independent experts judge, blind to the source of the proposals, the recognitions and the hard cases (M3a). Finally, the final model is applied to complete works outside training to map how formulae are organised (M5-min). A statistical test is prespecified for the main comparisons of A2. If the data are insufficient, results are reported as estimates with their uncertainty.

### The approach at a glance

```mermaid
flowchart LR
  K["Musicological knowledge<br/>annotations and<br/>family specifications"]
  S["Sources<br/>papadic Cherubic hymns<br/>and Koinonika"] --> R["Single symbolic<br/>representation"]
  R --> M1["M1<br/>boundaries and family jointly;<br/>choice of reading"]
  K --> M1
  K --> A2
  M1 --> A2["A2<br/>valid or perturbed knowledge;<br/>additive or logical use"]
  M1 --> M2["M2a<br/>learning from occurrences<br/>of the same family"]
  A2 --> E["Evaluation<br/>independent test set,<br/>blind expert judgements,<br/>complete works"]
  M2 --> E
```

## 3. Expected contributions

### For MIR and machine learning

The thesis defines a new, standardised symbolic MIR task: joint segmentation and recognition of melodic formulae within continuous notation, with several acceptable segmentations, unknown families and the option to abstain. The task comes with an evaluation corpus and reference models.

A2 offers a controlled way to measure what expert knowledge adds to a machine-learning model. It separates the value of the content of the knowledge from the value of the way it is used, by comparison with perturbed knowledge of the same form. The design transfers to any field where experts state testable category criteria.

M2a examines how the identity of a category can be learned without erasing its internal variation, a central issue for every musical tradition organised in melodic types.

### For Byzantine musicology

The work states explicit, testable specifications of formula families and documents which occurrences belong to the same formula, by mode, genre and form. It records where the written variation of each family is concentrated and collects the hard cases with full notational references. The specifications are tested empirically. Where the data disagree with a specification, the disagreement is a musicological finding and not simply a model error. The inventory of historical exegeses of the same passage is a deliverable in its own right, useful beyond the thesis.

### Concrete results and tools

- an open conversion chain from Neanes files to a single symbolic form, with a reconstruction check;
- an annotated evaluation corpus with its annotation protocol, published where licences allow;
- a register of tested formula-family specifications;
- trained models, code and reference models for the new task;
- maps of how formulae are organised in complete works;
- publications in MIR conferences and journals and in musicology journals.

---

[Home](../../README.md) · [Core research plan (PDF, Greek)](../../../documents/core-research-plan.pdf) · [Feedback and scientific discussion (Greek)](../../../docs/review/feedback.md)

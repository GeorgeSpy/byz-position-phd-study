---
title: 'Melodic Identity and Variation: From the Byzantine Thesis to the Popevki of Znamenny Chant'
subtitle: 'Research appendix for a comparative study in musicologically informed machine learning'
author: 'Georgios Spyridakis'
date: 'October 2026'
lang: en-GB
toc-title: 'Contents'
---

# Abstract

This appendix designs a comparative study around a question shared by two distinct traditions of liturgical chant: how is a melodic unit recognised when its concrete form changes from one occurrence to the next? The point of departure is the Byzantine melodic *thesis*, as studied in the main doctoral proposal. The comparison is with Znamenny chant of the Russian liturgical tradition and its melodic types, the *popevki*. The two units are not taken to be historically or musicologically identical; they pose analogous problems of identity within variation.

The proposed architecture has a common computational backbone: a symbolic encoder, tradition-specific adapters and a semi-Markov decoder that jointly locates the boundaries and the family of each occurrence. Two components are added on top of it:

- a probabilistic variation kernel $\kappa$, which describes how an occurrence aligns with the template of a candidate family through matches, insertions and deletions;
- a scheme that evaluates the musicological specification of the family over all possible alignments rather than over a single, arbitrarily chosen one.

The relationship is bidirectional: the alignment shows where a diagnostic relation is to be judged, and the specification can help estimate the alignment more accurately.

Three experiments make up the evaluation:

- **P1** tests whether full probabilistic summation over alignments predicts the judgements of independent experts better than simpler methods that have exactly the same information.
- **P2** tests whether the specifications improve the localisation of independently annotated structural landmarks.
- **E-min** asks, separately, whether the distribution of admissible variation learned in the Byzantine tradition helps predict Znamenny occurrences.

The numerical checks that accompany the appendix confirm the correctness of the recursions on synthetic data. Musical effectiveness and transferability between traditions remain empirical questions, to be decided on real sources.

**Keywords:** Byzantine chant, melodic thesis, Znamenny chant, popevka, melodic variation, latent alignment, semi-Markov CRFs, symbolic music information retrieval, musicologically informed machine learning.

# Introduction

Recognising the same musical idea in different forms is one of the basic problems of computational musicology. A melodic formulation may be shortened, expanded, or adapted to its text and modal setting. Surface similarity between two sequences of pitches is not always enough to decide whether they belong to the same musical category. Conversely, a successful alignment of two sequences does not by itself show which changes are musically acceptable. The need to describe both the common shape of a family of melodies and its variability has already led to the use of multiple alignments and probabilistic family models in symbolic music information retrieval (Bountouridis et al., 2017a).

In Byzantine chant the problem takes a specific form through the concept of the melodic thesis. A thesis is not a fixed sequence of signs. Its recognition depends on its melodic organisation, its modal function, its position within the composition and the range of its acceptable realisations. The main proposal of the dissertation therefore defines the *thesis family* as an explicit analytical category. The category is described by documented diagnostic relations, admissible differences and exclusion criteria, and is checked by independent experts. It is not uncritically identified with any historical term.

Znamenny chant offers a demanding comparative case. Popevki form an important class of recurring melodic formulae, associated with particular combinations of signs in the neumatic notation. The most systematic collections list some five hundred types, and their total number at the height of the tradition has been estimated at around a thousand (Bakhmutova, Gusev and Titkova, 2010). Computational reading of the notation has a long history, chiefly in the group at the Sobolev Institute of Mathematics in Novosibirsk. That work shows repeatedly that the identification of a popevka cannot rest on exact matching of signs or pitches alone.

The comparison of the two traditions does not attempt to assimilate them. The popevka is not defined as an equivalent of the thesis, and Znamenny patterns of expansion and closure are not translations of Byzantine functional roles. The comparative question is a different one: **can a way of learning identity and variation be transferred when the musical categories and their historical interpretations are defined independently in each tradition?** A positive answer would show computational generalisation. It would not prove historical descent or direct influence of one tradition on the other.

To examine this question, the proposed method does not stop at comparing ready-made vector representations. For each candidate family it takes into account all possible correspondences between the occurrence and the family template. It evaluates the musicological specifications under the uncertainty of those correspondences. Finally, it tests whether the same specifications help locate the structural points of the melody more precisely.

The approach rests on well-known methods of probabilistic sequence modelling and logical inference. Its research value will be judged by its musicological grounding and by comparison with strong reference models, not by the novelty of the individual computational operations.

The exposition follows this logic:

- First the units of comparison and the sources are defined, because before testing whether an algorithm recognises the same family, one must establish, on independent evidence, what "the same family" means in each tradition.
- The mathematical specification, the experimental protocol and the relation of the work to previous research follow.
- A short technical appendix collects the numerical checks and instructions for reproduction.

## Relation to the main doctoral proposal

The extension is an optional stage of the dissertation, scheduled from month 36 and dependent on the availability of sources and experts. It adds no preconditions for completing the dissertation and does not modify its studies. Those studies are:

- M1, which selects the symbolic representation $R^\star$ for joint segmentation and thesis recognition;
- A2, which examines the value of the content and logical composition of the specifications;
- M2, which compares encoders without and with relational supervision (B1, B2) and, in its historical strand, with pairs of co-exegeses of the same passage (EISE);
- the extensions M3–M5.

The M2 historical contrast $\Delta_{\mathrm{hist}}=S_{\mathrm{EISE}}-S_{\mathrm{B2}}$, which compares supervision from historically linked exegeses of the same passage (EISE) with supervision from different occurrences within the same family (B2), and the realisation-preservation check $Q_{\mathrm{real}}$ keep the definitions given in the main proposal. The quantities introduced here ($\Delta_{\mathrm{P1}}$, $\Delta_{\mathrm{P2}}$ and the E-min contrasts) are additional and distinct; they replace none of these.

# The musical unit in the two traditions

## The thesis in the Byzantine tradition

The thesis is not a construct of modern analysis. As early as the fifteenth century Gabriel Hieromonachos describes it through the analogy of the word (Hannick and Wolfram, 1985), and Manuel Chrysaphes links it to the union of signs that makes up a melody (Conomos, 1985). Morphological research of recent decades has shown how the thesis works within particular repertories.

- Karagkounis (2003, 2005) records named theses, their recurrences and their modal adaptations. He also distinguishes formations with the same pitch content that the older notation renders with different great hypostases.
- Arvanitis (2010) shows that a thesis remains recognisable when the number of syllables, the accentuation or the notational rendering changes.
- Gheorghiță (2010) follows eleven theses across 42 eighteenth-century Sunday koinonika and compares them with the exegeses of Gregorios and Chourmouzios.

From this tradition the main proposal draws the distinction between the historical type, the analytical family, the concrete occurrence in a work and source, and the symbolic realisation of that occurrence. The extension keeps this distinction unchanged. The kinship of interest here concerns melodic units with a common diagnostic core and a variable surface. Such schemata have been studied in other repertories as well, for example in the galant schemata. There Rabinovitch and Carter-Enyi (2024) show that internal stability differs from schema to schema and discuss, as a comparative example, Mavromatis's (2005) models of Greek liturgical chant.

## The popevki of Znamenny chant

Znamenny notation is neumatic. Each sign (*znamya*, pl. *znamena*) corresponds to a melodic movement of variable extent over one syllable of the text. From the seventeenth century the signs are accompanied by auxiliary indications of pitch and performance, the *pomety*. The interpretation of earlier manuscripts without these indications remains challenging and depends on the available comparative evidence. Popevki are stable combinations of signs with a characteristic melody, organised by mode (*glas*).

Alongside them stand larger melismatic units:

- the *fity*, written in abbreviated form and expanded into an analytical form (*razvod*), with different expansions in different schools (Parfentiev and Parfentieva, 2023);
- the *litsa*.

The stratification of melodic types in repertories outside the eight-mode system has been studied by Grigorjeva (2023).

The principal collection of popevki is V. M. Metallov's *Осмогласие знаменного распева* (1899). It gives the types in staff notation only. Bakhmutova, Gusev and Titkova (2010) examined the collection systematically. They compared it with three two-notation (*dvoeznamenny*) Oktoechoi of the late seventeenth and early eighteenth centuries from the Solovetsky collection of the National Library of Russia (619/647, 618/644 and Q.I.188), that is, manuscripts with parallel neumatic and staff notation.

**Coverage (§3.2 of the study, Oktoechos 619/647, exact search):**

- The catalogue has 511 entries distributed across the eight modes.
- 243 types were found (47.55%).
- 8,600 of the 29,217 notes of the text were covered (29.43%).

**Recovery of neumatic equivalents:**

- Across the three manuscripts, neumatic equivalents were recovered for 278 of the 511 types (54.40%).
- With approximate search allowing up to two changes the proportion rises to about 75%.
- Text coverage remains, on average, below 60%.

The three figures have different denominators and cannot serve as a single performance benchmark. A small discrepancy in the study shows how much care is needed: for the first mode the text reports coverage of 34.2%, while the table gives 34.6%, the value that agrees with the ratio $1{,}242/3{,}593$.

The same study documents four phenomena that bear directly on the design.

1. **Transposition.** In the first two manuscripts modes 3 and 5 are written a fourth lower. Metallov also gives the popevki of the fifth mode transposed, without a note to that effect. An explicit record of the pitch-normalisation policy per source and mode is therefore needed. A single normalisation estimated after the fact on the whole corpus would distort the comparison and use information from the test data.
2. **Melody does not suffice for identity.** The authors ask whether a sequence of pitches that matches the melody of the popevka *khamila* (хамила) should count as that popevka when its neumatic rendering lacks the sign of the same name. Some popevka names derive from signs of the notation. The family label may thus be partly a function of the notation itself, which calls for an explicit record of the provenance of every label.
3. **Structure of the popevka.** The identity of a popevka lies mainly in its cadence (*kadans*). Extension by lead-ins (*podvod*), with the cadence preserved, is often named as a new popevka ("small", "middle", "great"). Cadence and lead-in are therefore useful hypotheses about the local structure of the unit. The nested versions require a careful definition of the scale of analysis.
4. **Multiple neumatic renderings.** Most popevki have more than one neumatic rendering. Recurring connective signs, which do not belong to the popevki themselves, appear between them.

The appendix of the study lists multiple neumatic renderings and aggregate frequencies. Without reference to a specific work, passage and folio, these are not ready-made training or test examples.

Subsequent studies in this research area investigate further questions:

- In 2015, chains of signs with a unique or dominant melodic interpretation per mode are sought and tested on independent material (Bakhmutova, Gusev and Titkova, 2015).
- In 2020, approaches to reading manuscripts without *pomety* are presented (Gusev et al., 2020).
- In 2022, admissible variation is quantified by comparing hymns of the same title across different two-notation manuscripts (Bakhmutova, Gusev and Miroshnichenko, 2022).

These studies go beyond the decoding of notation: the 2010 study already addresses the structural organisation and naming of popevki, while the 2022 study quantifies admissible melodic variation. The additional question pursued here is whether independently annotated melodic families can be linked bidirectionally to probabilistic alignments, and whether the resulting learning transfers between traditions.

## What can and cannot be compared

The comparison is organised so that each tradition keeps its own vocabulary:

- **Unit of identity.** On the Byzantine side it is the thesis and its family, as defined in the main proposal. On the Znamenny side it is the popevka, both as a historical neumatic type and as a melodic category, with separate identifiers. The only shared assumption is that in both cases there is recurring musical identity within change, documented locally.
- **Structural roles.** The roles within the unit are defined separately in each tradition by an expert. In Znamenny chant, lead-in, cadence and transitional function are candidate roles with direct support in the sources. A partial mapping of roles between traditions is allowed only where functional analogy is documented, with a stated degree of confidence. No role is mapped by default.
- **Abbreviated and analytical notation.** Byzantine exegesis and the Znamenny *razvod* each have their own period and practice. They are compared only when the same passage and the nature of the expansion are documented.
- **Scale of analysis.** Theses, syllables and phrases may cross one another; so may popevki, sign repetitions and connective material. The full register keeps the overlaps. The first implementation is trained on a declared, non-overlapping projection of it.

Family labels follow two separate paths:

- The **melodic** label ($F_{\mathrm{mel}}$) is given by experts who see only the predefined melodic and textual information. They judge without access to the family specifications or to model predictions.
- The **historical** label ($F_{\mathrm{hist}}$) keeps the historical name or neumatic classification together with its evidence.

The correspondence between them may be many-to-many. The historical term is not required to satisfy a modern melodic criterion. The historical label is never used as a hidden input to melodic recognition.

# Research questions

The comparative question of the Introduction breaks down into four sub-questions, each with its own estimand.

1. **Recognition in Znamenny material.** When the family of a popevka is defined by independent musicological judgement, does joint estimation of boundaries and family perform better than exact search, edit distance and dictionaries of fixed sign chains?
2. **Value of full summation over alignments (P1).** When the application of a specification is judged over all possible alignments, are the experts' blind judgements predicted better? The comparison is with methods that use the same alignment information, compressed more simply.
3. **The specification as a guide to alignment (P2).** When the variation kernel is estimated under the constraint of the specification, does it locate more precisely the structural points that experts have annotated independently?
4. **Transfer of the organisation of variation (E-min).** Does the Byzantine distribution of admissible variation per structural role help predict Znamenny occurrences beyond what a flat starting point, an unrelated musical tradition and the general effect of position within the unit provide?

Questions 2 and 3 concern the relation between musicological knowledge and learning within the Znamenny material and do not presuppose successful transfer. Question 4 concerns transfer and does not presuppose questions 2 and 3.

# Proposed architecture

## Objects and available information

Let $d\in\lbrace B,Z\rbrace$ denote the tradition (Byzantine or Znamenny). Each work is a sequence of elementary symbolic events $X=(x_1,\ldots,x_T)$. A candidate segment $s=(a,b]$ has length $n=b-a$, with $1\le n\le L$. $F_d$ is the local vocabulary of known families in the tradition. $C$ contains the context known before prediction, such as the declared mode, the position in the text and the accentuation. Features computed from $X$ itself remain functions of the observation and are not treated as exogenous constants.

For each candidate family $f\in F_d$, the template $\Pi_f$ consists of $J_f$ landmarks. Each landmark has a local structural role $r_{f,j}\in\mathcal R_d$. The template is derived solely from training examples and expert judgement, and it is a testable hypothesis about that family. For families without a single common core (polythetic families), a finite mixture of templates $p_f=\sum_v\omega_{f,v}p_{f,v}$ is allowed, with the same capacity limit in all compared models. A family is not excluded because a single template cannot describe it; the failure is recorded as a result.

During recognition, $f$ ranges over all candidate families. The role of each template landmark is known from the candidate family, while its position within the observed segment is latent. The correct family and the correct internal boundaries are used only under explicitly declared training and evaluation conditions, so that they do not leak into the recogniser as input.

The symbolic bridge between the traditions encodes diatonic degree and motion, nominal duration and admissible syllabic information. A local layer per tradition keeps the finer notational distinctions. The common alphabet $V$ is finite and defined on the training data, with a common policy for unseen symbols. Measurements in bits per event always refer to this encoding.

## The variation kernel $\kappa$

The kernel $\kappa$ is a profile hidden Markov model (profile HMM) with three kinds of state: match $M_j$, insert $I_j$ and delete $D_j$, together with a start state $\mathrm{BEGIN}$ and an end state $\mathrm{END}$.

- An alignment $\pi$ traverses the template and the observed sequence monotonically.
- States $M_j$ and $I_j$ emit one event, while $D_j$ emit none.
- Substitution is the emission of a different symbol from $M_j$. Expansion or contraction over several events is expressed as a sequence of such elementary operations.
- Assigning a more specific musicological name to a composite operation requires additional evidence and does not follow uniquely from the alignment.

The probabilities of the outgoing transitions of each state sum to one, including the transition to the end. In the last column $J=J_f$:
```math
t(M_J,\mathrm{END})+t(M_J,I_J)=1,\qquad t(I_J,\mathrm{END})+t(I_J,I_J)=1,\qquad t(D_J,\mathrm{END})=1.
```
There are no cycles of silent states, and every insert self-transition has probability $t(I_j,I_j)\lt 1$. The joint probability of sequence and alignment is
```math
p_\kappa(x,\pi\vert f,C)=\prod_{e\in\pi}t_\kappa(e\vert r,C)\prod_{e\in\pi_{\mathrm{emit}}}e_\kappa\big(x_{i(e)}\vert e,\Pi_f,C\big),
```
where the first product includes the transition to the end. Because each step is drawn from a locally normalised distribution and the chain terminates almost surely, the distribution is normalised over all lengths, sequences and alignments:
```math
\sum_{n\ge0}\sum_{x\in V^n}\sum_\pi p_\kappa(x,\pi\vert f,C)=1.
```

Transition parameters are shared per validated role, while emission distributions are defined around the template. For transfer from the Byzantine tradition a Dirichlet prior is used:
```math
\theta_{Z,r}\sim\mathrm{Dir}\big(\alpha_r\,\mu_{B,\mu(r)}\big).
```
Here $\mu(r)$ is the documented partial mapping of Znamenny role $r$ to a Byzantine role, and $\mu_{B,\mu(r)}$ the mean transition probabilities estimated in the Byzantine tradition. Roles without a mapping get a local, non-informative distribution. All comparison conditions share the same topology and the same number of parameters on the Znamenny material. The concentration $\alpha_r$ is chosen on development data, and the full curve for fixed values of it is also reported, so that full adaptation to the Znamenny material does not hide the effect of the source.

### Length and normalisation

We define the marginal probability of a sequence of length $n$ and the total mass of that length:
```math
A_f(x,n)=\sum_\pi p_\kappa(x,\pi\vert f,C),\qquad a_f(n,C)=\sum_{x\in V^n}A_f(x,n).
```
In E-min the length is treated as known, and the conditional distribution $p_\kappa(x\vert f,C,n)=A_f(x,n)/a_f(n,C)$ is used, so that length information is common to all comparisons.

The full prediction, which includes length, is $\pi_f(n\vert C)\,A_f/a_f$. Alternatively the intrinsic length of the profile is used, in which case the joint probability is simply $A_f$. Multiplying $A_f$ by an independent length distribution requires renormalisation. For a window of lengths $1\le n\le L$ the denominator is $\sum_{n=1}^La_f(n,C)$. The three versions are reported separately.

## Diagnostic concepts and specification

The diagnostic concepts $U=(U_1,\ldots,U_N)$ are binary variables, such as "the cadence falls on the degree that the family prescribes" or "the lead-in rises above the landmark". The family specification is the set $S_f\subseteq\lbrace0,1\rbrace^N$ of their admissible combinations. Each concept declares:

- the landmark or region at which it is judged;
- when it is observable and when it is applicable;
- how deletion of its landmark is treated;
- what emission history it needs.

For a given alignment $\pi$ we define
```math
q(u\vert x,\pi,C)=\prod_{j=1}^Nq_j(u_j\vert x,\pi,C),\qquad Q_f(x,\pi)=\sum_{u\in S_f}q(u\vert x,\pi,C).
```
Independence of the concepts is assumed only **given the alignment**. When the alignment is marginalised, the result is a joint distribution over the concepts that in general does not factorise:
```math
q^\star_f(u\vert x,C)=\sum_\pi p_\kappa(\pi\vert x,f,C)\,q(u\vert x,\pi,C).
```
On the joint space $(x,\pi,u)$ four distinct quantities are defined:
```math
\begin{gathered}
B_f(x,n)=\sum_\pi p_\kappa(x,\pi\vert f,C)\,Q_f(x,\pi),\\
m_f(x)=\frac{B_f(x,n)}{A_f(x,n)}=\sum_{u\in S_f}q^\star_f(u\vert x,C),\\
z_f(n,C)=\sum_{x\in V^n}B_f(x,n),\qquad Z_f(n,C)=\frac{z_f(n,C)}{a_f(n,C)}.
\end{gathered}
```
$B_f$ is the joint probability of observing $x$ and satisfying the specification. $m_f$ is the probability of satisfaction given $x$. $z_f$ is the joint mass of length and satisfaction, and $Z_f$ the prior probability of satisfaction given the length.

If the corpus consists of occurrences selected precisely because they satisfy the specification, their correct distribution is
**(1)**

```math
p^S_f(x\vert n,C)=\frac{B_f(x,n)}{z_f(n,C)}=\frac{p_\kappa(x\vert f,n,C)\,m_f(x)}{Z_f(n,C)}.
```
For a window of lengths $[1,L]$ the corresponding probability of satisfaction is $Z^{[1,L]}_f(C)=\sum_{n=1}^Lz_f(n,C)/\sum_{n=1}^La_f(n,C)$. The notation distinguishes this restricted quantity from the mass over all possible lengths.

### The reference mass $r_f$ and the normalisation $Z_f$

The first form of this approach, the ECSI of the main proposal (Evidence-Conditioned Selective Invariance), compares the mass $m_f$ with a reference mass $r_f(C)=\sum_{u\in S_f}r(u\vert C)$. This mass derives from a predefined reference distribution $r$ over the concepts and corrects the bias towards broader specifications. In a discriminative model the difference $\log m_f-\log r_f$ is a perfectly legitimate feature.

The ratio $m_f/r_f$ acquires the meaning of a Bayes factor, however, only when $q$ is a posterior under the same reference distribution, that is, $q(u\vert x,C)=r(u\vert C)\,\ell(x\vert u,C)/p_r(x\vert C)$, with a common likelihood $\ell$. The well-known encompassing-prior identity then holds (Klugkist, Kato and Hoijtink, 2005):
```math
\frac{m_f(x)}{r_f(C)}=\frac{p_r(x\vert U\in S_f,C)}{p_r(x\vert C)}.
```
Simple empirical calibration of a classifier, or use of training frequencies, is not enough for this identity to hold. In the model of equation (1) the corresponding normalising mass is $Z_f(n,C)$, not an $r_f$ independent of $\kappa$.

The difference between the two choices is a constant for each pair $(f,C)$. If the model has a free bias per family and $(n,C)$ stay fixed, the constant is absorbed and the final scores are unchanged. Calibration and the comparison with the unknown family are then unchanged as well. Recalibration is needed in the following cases:

- when the shift is not fully absorbed;
- when $(n,C)$ vary;
- when the biases are constrained.

### Information overlap

The factorisation $p_\kappa(x,\pi)\,q(u\vert x,\pi)$ is consistent even when a concept is a deterministic function of the aligned emission. Conditioning on the event of satisfaction changes the distribution precisely through the denominator of (1), and a discriminative CRF accepts correlated features by definition.

The table that assigns information to the kernel or to the specification serves the **experimental isolation** of each part's contribution; it does not forbid shared inputs. An error arises only when the same observation is counted twice as two independent generative pieces of evidence, or is given a Bayesian interpretation it does not have.

## Exact computation: product dynamic programming

The specification $S_f$ is compiled into a deterministic finite automaton:

- Its states $w$ are the residual Boolean functions after evaluation of the concepts already judged.
- The width of the automaton, the maximum number of states at any level, is denoted $W_f$.
- The transition $\delta(w,u_{[e]})$ updates the state with the block of concepts $u_{[e]}$ judged on a profile transition $e$.

Each full assignment $u\in\lbrace0,1\rbrace^N$ is counted exactly once, even when it satisfies more than one alternative branch of the specification.

### Observed sequence

For a fixed sequence $x$, the state of the dynamic programme comprises:

- the number $i$ of events consumed;
- the template column $j$;
- the state type $\sigma\in\lbrace M,I,D\rbrace$;
- the logical state $w$;
- whatever finite path statistics $c$ are needed.

A transition $e$ updates the mass as follows:
**(2)**

```math
\alpha(\sigma')+=\alpha(\sigma)\,t_\kappa(e)\,e_\kappa(x_i\vert e)^{\mathbf 1_{\mathrm{emit}}}\sum_{u_{[e]}}q_{[e]}(u_{[e]}\vert x,e,C)\,\mathbf 1\lbrace w'=\delta(w,u_{[e]})\rbrace.
```
Deletions are computed in column order, since there are no cycles of silent states, and the transition to the end multiplies the final mass. Summing over all final logical states gives $A_f(x,n)$; summing only over accepting states gives $B_f(x,n)$. Induction on the partial order $(i,j)$ proves that each alignment and each concept assignment contributes exactly once. The implementation works in log space.

### Summing over emissions for $z_f$

To compute $z_f$ the sequence is not given, and every possible emission must be summed. If the concepts depend on the last $\ell_h$ emitted symbols, the state also includes the history $h\in V^{\le\ell_h-1}$. For each candidate emission $v\in V$:
**(3)**

```math
\begin{aligned}\alpha(i{+}1,j',\sigma',w',h',c')+=\;&\alpha(i,j,\sigma,w,h,c)\,t_\kappa(e)\,e_\kappa(v\vert e)\\&\times\sum_{u_{[e]}}q_{[e]}(u_{[e]}\vert h,v,c,e,C)\,\mathbf 1\lbrace w'=\delta(w,u_{[e]})\rbrace,\end{aligned}
```
with $h'$ the suffix of length $\ell_h-1$ of $h\oplus v$ and $c'$ the updated statistics. Insertions update the history even when no new concept is judged; deletions leave it unchanged. If the history is not updated on insertions, concepts that depend on preceding symbols are computed incorrectly. This error is caught by the numerical checks.

Some concepts need additional state:

- A concept about the mean value of the symbols requires the pair $(n,\sum_ix_i)$, with up to $n(\vert V\vert-1)+1$ possible sums.
- Counting insertions requires a bounded counter.
- A relation between two distant landmarks requires storing the value or position of the first until the relation is judged.

When the concepts are computed by a bidirectional neural encoder of the varying $X$, exact computation of $z_f$ falls outside this lattice. Either a finite generative concept interface or an explicitly declared numerical approximation is then chosen. The discriminative version of the model can use the full encoder without needing $Z_f$.

### Prefix reuse and cost

If the internal factors of (2) do not depend on the end of the segment, one pass from each start gives the results for all possible ends. If they do, a separate pass per end is required. Concepts concerning the whole segment can be judged at the end of the pass, provided they do not alter the earlier factors. The specification compiler checks this condition automatically.

Let $k$ be the maximum size of a concept block, $H$ the number of history states and $R$ the number of additional statistic states. Then:

| Computation | Cost |
|------|----------|
| One observed segment of length $n$ | $\mathcal O(nJ_fW_fR\,2^k)$ |
| All ends from a fixed start (with reuse) | $\mathcal O(LJ_fW_fR\,2^k)$ |
| Whole work of length $T$ | $\mathcal O(TL\sum_fJ_fW_fR\,2^k)$ |
| Whole work, when factors depend on the end | $\mathcal O(TL^2\sum_fJ_fW_fR\,2^k)$ |
| Generative normalisation for one $(f,C)$ and all lengths up to $L$ | $\mathcal O(LJ_fW_fRH\vert V\vert\,2^k)$, with $H\le\vert V\vert^{\ell_h-1}$ |

A single rolling pass needs $\mathcal O(J_fW_fRH)$ memory; storage for gradient computation needs $\mathcal O(LJ_fW_fRH)$.

The width $W_f$ can grow exponentially when the specification links distant landmarks. A bound such as $W_f\le16$ is a practical computational budget, not a mathematical constant. In practice the actual size of each specification's state space is recorded.

If a Monte Carlo approximation with sampled alignments is used:

- the estimator $\hat m_f$ is unbiased;
- its logarithm $\log\hat m_f$ is biased by Jensen's inequality and may vanish.

The outer dynamic programme remains exact only with respect to the scores it is given.

## The A0 backbone and structured prediction

The common backbone, called A0, computes local states and two representations for each segment:
```math
\begin{gathered}h_t=g_\theta\big(A_d(R_d(X))\big)_t,\qquad r_s=\mathrm{Pool}(h_{a+1:b}),\\ z_{\mathrm{id}}(s)=q_{\mathrm{id}}(r_s),\qquad z_{\mathrm{real}}(s)=q_{\mathrm{real}}(h_{a+1:b}).\end{gathered}
```
The symbols mean the following:

- $R_d$ is the symbolic representation of the tradition: for the Byzantine it is the $R_B^\star$ selected by M1; for the Znamenny it is defined by a local protocol at the same elementary unit.
- $A_d$ is the tradition adapter.
- $g_\theta$ is the shared encoder.
- $z_{\mathrm{id}}$ is the family-identity representation and $z_{\mathrm{real}}$ the representation of the concrete realisation.

For each known family $f$, the segment score is
**(4)**

```math
\phi(s,f)=\phi^0(s,f)+\beta_\kappa\log\frac{p_\kappa(x_s\vert f,n,C)}{p_0(x_s\vert n,C)}+\beta_S\big[\log m_f(x_s)-\log r_f(C,n)\big],
```
where $\phi^0$ is the base score of the backbone and $p_0$ a background model. The coefficients $\beta_\kappa,\beta_S$ are applied **after** marginalisation. The term equals $(\beta_\kappa-\beta_S)\log A_f+\beta_S\log B_f$, plus the length, background and reference terms. Moving the coefficients inside the sum over alignments would define a different model.

The main recogniser is a discriminative semi-Markov CRF (semi-CRF):

- the coefficients are tuned on development data;
- normalisation is over all possible segmentations;
- calibration is empirical.

The choice $r_f=Z_f$ reproduces the generatively consistent term when $\beta_\kappa=\beta_S=1$. Any other positive value of $r_f$ defines an explicitly declared discriminative comparison model. The base score $\phi^0$ may contain neural features. Equation (4) does not acquire a generative interpretation merely because one of its terms has the form of a log probability ratio.

The output $y$ is a set of non-overlapping segments labelled $f\in F_Z\cup\lbrace U\rbrace$, where $U$ denotes a valid melodic unit of unknown family, with its own prediction head. Every event not covered by a segment receives a single skip decision with score $\chi_t$. Documented connective material acts as an independent constraint during supervision. The score and probability of a segmentation are
```math
s(y,X)=\sum_{(s,f)\in y}\phi(s,f)+\sum_{t\notin\cup y}\chi_t,\qquad P(y\vert X)=\frac{\exp s(y,X)}{\mathcal Z(X)},
```
and the empty segmentation is allowed. With $\alpha_0=0$ in log space, the forward recursion is
**(5)**

```math
\alpha_b=\mathrm{LSE}\Big(\alpha_{b-1}+\chi_b,\ \big\lbrace\alpha_a+\phi((a,b],f):\ \max(0,b-L)\le a\lt b,\ f\in F_Z\cup\lbrace U\rbrace\big\rbrace\Big),
```
where LSE is the log-sum-exp operation, and $\log\mathcal Z(X)=\alpha_T$.

- Viterbi decoding replaces LSE with a maximum and keeps back-pointers.
- With the backward variable $\eta_b$, the marginal probability of each segment is $\exp(\alpha_a+\phi(s,f)+\eta_b-\alpha_T)$.
- The cost is $\mathcal O(TLK)$ in time, with $K=\vert F_Z\vert+1$, and $\mathcal O(T)$ in memory, beyond storage of the scores. The cost of the neural segment summaries is reported separately.

### Background, transitions and partial supervision

**Background.** Full coverage of the sequence by explicit background segments $O$ of length exactly 1 corresponds bijectively to the skip mechanism of (5). If background segments of several lengths were allowed, the same uncovered stretch would have many equivalent encodings (eight for four consecutive events), and the output distribution would be distorted.

**First-order transitions.** To carry the memory of the last family across gaps, the state $\alpha_t(f,g)$ is defined with a gap flag $g\in\lbrace0,1\rbrace$ and an initial BOS state. A skip updates $\alpha_{t+1}(f,1)\leftarrow\mathrm{LSE}(\alpha_{t+1}(f,1),\ \alpha_t(f,g)+\chi_{t+1})$. A new segment $(a,b]$ labelled $f$ is added as
**(6)**

```math
\alpha_b(f,0)\leftarrow\mathrm{LSE}\Big(\alpha_b(f,0),\ \phi((a,b],f)+\mathrm{LSE}_{f',g}\big[\alpha_a(f',g)+T_a(f',f,g)\big]\Big).
```
The cost depends on the form of the transition $T_a$:

- If $T_a$ does not depend on the end $b$, the inner sum is computed once per $(a,f)$, at cost $\mathcal O(TK^2+TLK)$.
- If it also depends on the length of the new segment, the cost becomes $\mathcal O(TLK^2)$.
- Full dependence on the entire preceding segment requires $\mathcal O(TL^2K^2)$.
- Dependence on the exact gap length requires storing the previous end and reaches $\mathcal O(T^2L^2K^2)$, unless the gap is bounded.

A first-order model in which background resets the family memory is different from (6). The first implementation uses the zero-order recursion (5).

**Partial supervision.** The full musicological register keeps overlaps and alternative readings. A fixed projection selects disjoint windows $W_j$, on which the non-overlapping segment loss is applied. If $\mathcal C_j$ are the outputs consistent with the annotation of the window, the segmentation loss is
```math
\mathcal L_{\mathrm{seg}}(X)=\frac{\sum_j\big[\log\mathcal Z_j-\log\mathcal Z^A_j\big]}{\sum_j\vert W_j\vert},\qquad \mathcal Z^A_j=\sum_{y\in\mathcal C_j}\exp s(y,X).
```
A fully unannotated region contributes zero loss. Alternative boundaries and joint constraints are encoded in a finite annotation automaton that extends the state space of (5). The compiler checks:

- that $\mathcal C_j\neq\emptyset$;
- the compatibility of the boundaries;
- coverage with respect to $L$.

A constraint of the form "exactly one of these occurrences" needs an explicit counter, because independent segment masks cannot express it.

### Generative interpretation of the CRF

Consider a prior over valid segmentations of length $T$ with the following weights:

- $(1-\rho)$ for each background event;
- $\rho\,\pi_f\,\pi_f(n)$ for each segment of family $f$ and length $n$.

The distribution is normalised by the constant $C_T$ that constrains the segmentation to end exactly at $T$. Each segment emits from the normalised distribution $p_f(x_s\vert n,C)$, and each background position from $q_0(x_t\vert x_{\lt t},C)$. Then $\sum_{X,y}p(X,y\vert T,C)=1$, provided $C$ is exogenous.

Dividing by the common weight $(1-\rho)^T\prod_tq_0(x_t\vert x_{\lt t},C)$ yields the score
```math
\begin{aligned}\phi_G(s,f)=\;&\log\rho+\log\pi_f+\log\pi_f(n)-n\log(1-\rho)\\&+\log p_f(x_s\vert n,C)-\sum_{t\in s}\log q_0(x_t\vert x_{\lt t},C),\end{aligned}
```
with $\chi_t=0$. The common terms and $C_T$ cancel in $P(y\vert X)$, which thus coincides exactly with the semi-CRF for $\beta=1$. Three points need care:

- The term $-n\log(1-\rho)$ depends linearly on length.
- If the background is Markov, the denominator uses the true left context even at segment boundaries. Restarting the background in each segment changes the model.
- With the selected distribution of (1), the term $-\log Z_f(n,C)$ is added as well.

## Bidirectional learning and the selection mechanism

**Initialisation.** Training starts from local concept labels for the classifiers $q_j$ and a normalised kernel $\kappa$. The concept classifiers stay fixed in the first comparison where the specification trains the kernel, because unconstrained joint maximisation on positive examples alone leads to degenerate solutions ($q_j\approx1$) that bypass the musicological problem. Later joint training keeps:

- an independent concept loss;
- hard negative examples;
- calibration on held-out data;
- a fixed specification.

With the shorthand $a(x)=p_\kappa(x\vert n,C,f)$, $b(x)=a(x)\,m_f(x)$ and $Z=\sum_{x\in V^n}b(x)$, the correct objective depends on how the corpus was assembled:

| Sampling regime | Contribution to the log-likelihood |
|-----------|-----------|
| Representative sampling of $X$ with recorded judgement $Y\in\lbrace0,1\rbrace$ | $\log a(x)+Y\log m_f(x)+(1-Y)\log(1-m_f(x))$ |
| Observation of $(X,Y=1)$ without negatives excluded by design | $\log b(x)$, together with the other outcomes of the same design |
| Corpus collected conditional on $Y=1$ | $\log b(x)-\log Z$ |
| Data $X$ with weak applicability judgements, no generative claim | $Y\log m_f(x)+(1-Y)\log(1-m_f(x))$ |
| Selective collection with known inclusion probability $s(x,y,C)$ | weighting by the full selection mechanism; $Z$ alone may not suffice |

Conditioning on a known family does not imply that the occurrences were selected through the specification itself. In E-min the family model is trained directly as $p_\kappa(X\vert F,C,n)$. The likelihood of selected positives is used only when the kernel defines a pre-existing population of candidates and inclusion in the corpus depends on acceptance through the same specification. If the family judgement rests on richer evidence, a separate selection variable is defined.

**E-step.** For a positive example, the alignment has the conditional distribution
```math
p(\pi\vert x,S,f,C)=\frac{p_\kappa(x,\pi\vert f,C)\,Q_f(x,\pi)}{B_f(x,n)},
```
and the constant $Z$ cancels.

**M-step.** For selected occurrences, the gradient with respect to the kernel parameters (with $q$ fixed) keeps the negative term of the normalisation:
**(7)**

```math
\nabla_\kappa\ell_{\mathrm{sel}}=\mathbb E_{\pi\vert x,S}\big[\nabla_\kappa\log p_\kappa(x,\pi)\big]-\mathbb E_{X,\pi\vert S,n,C}\big[\nabla_\kappa\log p_\kappa(X,\pi)\big],
```
plus the prior terms. Simple renormalisation of expected counts, as in Baum–Welch, in general does **not** maximise this function. Either exact differentiable computation is used, or generalised EM with a check that the correct function increases monotonically.

**Deterministic and probabilistic rules.** With deterministic diagnostic rules, conditioning amounts to a Kullback–Leibler projection onto the set of admissible pairs $(\pi,u)$. With probabilistic $Q_f$ it is a reweighting of alignments, not an exclusion. Exact equivalence with posterior regularisation presupposes the same variable space and the same constraints.

**Identifiability limit.** Consider two alignments that give the same distribution $p(X)$ but different constant acceptance probabilities, $Q_0=0.2$ and $Q_1=0.8$. For a mixture weight $\theta\in[0,1]$:

- the distribution of $X$ is unchanged;
- the acceptance probability is $m_\theta=0.2+0.6\theta$;
- even the distribution of selected positives is unchanged, since $B_\theta(X)/z_\theta=p(X)$.

Selected positive examples alone therefore identify **neither** $\theta$ nor the alignment. The missing information comes from representatively observed judgements $Y\in\lbrace0,1\rbrace$ or from independent landmark annotations.

**Total loss.** Discriminative training of the backbone minimises
```math
\mathcal L_{\mathrm{total}}=\mathcal L_{\mathrm{seg}}+\lambda_F\mathcal L_F+\lambda_{\mathrm{pair}}\mathcal L^{\mathrm{id}}_{\mathrm{pair}}+\lambda_{\mathrm{rec}}\mathcal L_{\mathrm{mask}}+\lambda_q\mathcal L_q,
```
with a separate, explicitly declared stage for estimating the kernel $\kappa$. Condition B2 keeps only positive family pairs. The gradient reaches the shared encoder only if the $Q_{\mathrm{real}}$ gate is checked under common conditions.

## Greater expressiveness within the same system

The only optional extension considered replaces the product of independent concepts within a small block $B_k$ ($\vert B_k\vert\le k$) with a joint distribution $q_{B_k}(u_{B_k}\vert x,\pi,C)$. The $2^{\vert B_k\vert}$ configurations are summed in (2), while the profile topology, the specification and the outer dynamic programme stay the same. For $q(00)=q(11)=1/2$ the joint block gives $P(U_1=U_2)=1$, whereas independent concepts with the same marginals give $1/2$. The joint distribution thus represents dependencies that the product cannot, even with a certain alignment. The block size is chosen on musicological grounds and with independent concept supervision, never on test data.

The difference between full summation and simpler pooling of marginals also appears for two concepts **at the same** landmark, when the position of the landmark is uncertain. If the probabilities of the two concepts, as functions of the alignment, jointly take the value 0.1 or 0.9 with equal weights, full summation gives $\mathbb E[Y^2]=0.41$, while pooling gives $(\mathbb EY)^2=0.25$. The exact condition for the two methods to differ is non-zero mixed moments of the concept probabilities with respect to the alignment. The concepts need not belong to different landmarks.

# Data, annotation and leakage control

## Sources

The first phase is an inventory, not training. The existence of a catalogue record or a digitisation does not mean that an available, licensed and aligned corpus exists. The table summarises what is known today about the sources used in previous research and what must be documented before training.

| Source | What is known | What is required before training |
|-----|--------|--------|
| Oktoechos 619/647 | Catalogue record in the National Electronic Library of Russia, V+57 folios, digitised 2023 | Access to images of specific folios, terms of use, quality sample, double transcription |
| Oktoechos 618/644 | Used in the 2010 and 2022 studies | Current catalogue identity, access to images, check of earlier confusions in numbering |
| Oktoechos Q.I.188 | Used in the same studies | Catalogue record, folio range, dating, relation to the other witnesses |
| Metallov (1899) | Catalogue record; analytical use in the 2010 study | Usable digital copy; use as external prior knowledge, with comparison with and without it |
| Electronic dictionaries of previous research | Mentioned in the literature | Version, actual availability, data schema, passages, licence, overlap check with test data |

Each source is described in a record that registers:

- identity: shelfmark, institution, persistent identifier, access date, folio range;
- historical data: dating with its uncertainty, scribal tradition, copying relation to other witnesses;
- rights: terms of use per kind of derivative;
- digital status: digitisation, recognition software version, cryptographic hash of image and transcription;
- persons responsible for checking.

Rights are recorded as evidence and are not inferred from the age of the manuscript.

Quality control includes:

- two independent transcriptions of selected folios and collation with the image;
- recording of uncertainty per sign;
- a procedure for resolving disagreements that keeps the original versions.

Each elementary event is linked to the corresponding graphs of the source and to the syllable of the text. Bidirectional mapping between notation and symbols, duration sums and consistency of the pitch policy are checked. Historical discrepancies are not silently smoothed out.

## Annotation

Evaluation follows the logic of the independent musicological validation (M3a) of the main proposal:

1. Two experts who did not write the specifications first judge blind the boundaries and membership of each occurrence (member, non-member, unresolved).
2. In a separate round they judge the application of the diagnostic concepts and the positions of the landmarks.
3. Agreement is reported per type of decision, with uncertainty per source group.
4. Disagreements are classified as disagreements of boundary, level of analysis, melodic structure, modal context, historical naming or source uncertainty.

The templates $\Pi_f$ and the roles are estimated only on training data and locked before testing. The recogniser sees one specification for each **candidate** family, not the correct one. If each new family requires local supervision, the requirement is declared as a few-shot condition and costed. For an unknown family without a specification, the output is $U$ or abstention.

Five states are distinguished, with separate records and separate losses:

- **known family**: a documented member of a known family;
- **unknown family** ($U$): a valid unit outside the training vocabulary;
- **connective or background** ($O$): documented material outside the analytical unit;
- **unresolved**: a pending judgement, treated as latent supervision;
- **abstention**: a model decision when the calibrated confidence does not reach the predefined threshold.

For each diagnostic concept four values are kept: true, false, unobserved, not applicable. Deletion of a template landmark follows a declared policy: it may be a documented violation of a required landmark or an admissible absence, and it does not automatically become "false" for every feature. The classifiers $q$ are trained with the appropriate masks, and the specification defines applicability before evaluation.

The register of occurrences follows a minimal, machine-checkable schema. Each record contains:

- identifiers of source, work, passage and dependence group;
- the two family labels and the provenance of the annotation;
- the admissible inputs and the selection mechanism;
- the pitch policy;
- candidate boundaries, landmarks and uncertainty;
- usage rights.

The value "unresolved" is allowed in documentation, but training is blocked when a usage licence is missing or when two dependence groups overlap. The full inventory is the first genuine musicological deliverable of the extension.

## Leakage control

Historical corpora have many hidden routes from the label to the input. The main ones and their mandatory handling are as follows.

| Risk | Handling |
|------|---------|
| Family defined by the sign chain | Record of the provenance of each label; separate melodic and historical paths; the correct family is never an input in P1 |
| Same hymn in different witnesses, copies, parallel passages | Placement in the same dependence group and the same side of the split |
| Dictionary or catalogue containing test passages | Check of the provenance of entries; comparison with and without the external knowledge |
| Templates and roles from test families | Estimation only on training data; access to candidate specifications declared as a closed set or as a few-shot condition |
| Known boundaries | Allowed in E-min and in known-boundary measurement; excluded from the joint segmentation test |
| Mode, length or text as a shortcut | Reference models with mode only, length and position only, text only; hard negatives within the same mode |
| Normalisation with test data | Pitch, time and symbol dictionaries defined on training data only; manual correction only with source evidence |
| Selection of favourable specifications | Record of version, judge and lock date; selection only on training and development data |
| Calibration, thresholds, abstention | Separate development set with the same positive rate or a declared correction; the test set is opened once |
| Unannotated test data | Excluded from adaptation; any transductive version is examined separately |
| *Pomety* and target signs in historical recovery | If they belong to the target notation, removed from context and from every derived feature |
| Historical label in historical recovery | Excluded when it derives from the hidden notation |
| Witness or passage identifier | Only for splitting and checking; as features only generalisable metadata are allowed |
| Judges' familiarity with the catalogue | Record of each judge's sources, independent resolution of disagreements, analysis without the familiar entries |
| Exclusion of ambiguous examples | Report of proportion and characteristics; multiple acceptable answers and coverage-sensitive measures |

## Preservation of realisation information ($Q_{\mathrm{real}}$)

The main proposal (§7) defines three tests on held-out occurrences:

1. reconstruction of hidden symbolic features, with the same masking policy and the same available information in all conditions;
2. discrimination of two realisations of the same family by their melodic and temporal articulation, with balancing of length and text where needed;
3. linear prediction of local properties, such as range and syllabic distribution, by a probe of limited capacity.

The probes are applied to the representations $h_t$, $z_{\mathrm{id}}$, $z_{\mathrm{real}}$ with a frozen encoder, the same splits, the same number of parameters and the same targets. The reference point is a model on the raw input. Dimension and pooling are declared; zero-padding does not count as additional information. The gate is pre-registered non-inferiority against the corresponding base condition on **all** tests, with margins from a pilot measurement of repeatability.

$Q_{\mathrm{real}}$ is not replaced by an information ratio and is not judged on reconstruction alone. The pull of family identity on $z_{\mathrm{id}}$ can affect the shared representation $h$ even when a separate $z_{\mathrm{real}}$ exists. With a frozen encoder and identical preprocessing the probes see the same data; baseline sufficiency is reported nonetheless. If the system selects different segments or excludes occurrences, coverage changes and a new evaluation is required.

The log-likelihood of the kernel, operation counts and alignment marginals are examined as additional representations. Two different sequences can have the same summary, and the existence of an alignment that produces the observation does not guarantee that the stored representation makes it recoverable.

## Historical recovery and identifiability

Historical recovery targets the distribution
```math
p\big(H^{(w)}_Z\vert X_Z,C_{\mathrm{adm}}\big),
```
where:

- $H^{(w)}_Z$ is the surviving notation of the particular witness $w$;
- $C_{\mathrm{adm}}$ contains only the admissible context available before prediction.

The witness identifier specifies which target is evaluated; it is not a key the model can memorise. Each task declares whether duration, syllabic alignment and *pomety* are observed or hidden.

Let $\mathcal H(X,C)$ be the set of candidate historical notations. Exact identification is possible only when the admissible observations distinguish the candidates. If $p(X,C\vert H_1)=p(X,C\vert H_2)$, no estimator with these inputs distinguishes them better than the prior allows. Moreover, many kernel alignments can produce the same distribution of $X$. Uniqueness of the numerical solution $q^\star$ for given parameters does not imply a unique historical explanation.

The set $\mathcal G_o$ of acceptable answers includes the acceptable readings of the **same** image or a documented equivalent transcription. A different notation in another witness does not automatically become a correct answer for witness $w$. Evaluation uses the set log loss $-\log\sum_{H\in\mathcal G_o}p(H\vert X,C)$. When an empirical distribution of judges exists, cross-entropy with respect to it is used.

Four conditions are compared:

1. a dictionary-and-context reference model;
2. an encoder of the raw input;
3. probes on the frozen representations $h$ and $z$;
4. an independent supervised inverse model with the same information.

The following are reported:

- exact recovery and symbol edit error;
- set coverage and prediction-set size;
- log loss;
- the risk–coverage curve.

A family label $R$ produced from $X$ itself is an admissible summary. But if $R=f(X)$, then $I(H;R\vert X,C)=0$: any advantage of the probe indicates easier access to information within a model, not new historical information.

The abstention threshold is chosen on development data. Accuracy on the accepted subset and total coverage are reported. Conformal coverage guarantees would require source-level exchangeability, which cannot be assumed for three historically related witnesses. The Byzantine index $\Delta_{\mathrm{hist}}$ remains tied to the independent performative criterion of the main proposal and lends its name to none of the Znamenny quantities.

# Experimental design

## Splits, labels and annotation budgets

**Unit of record.** This is the occurrence, with identifiers of source, work, passage, witness and folio, event range and boundary uncertainty.

**Unit of independence.** This is the connected group formed by relations of same hymn or passage, copying, parallel witness and near-identical excerpts. All connected occurrences go to the same outer group. A shared family dictionary does not automatically join all works; it is checked, however, whether the dictionary copied a specific test source.

**Splits.** The dependence graph is defined before any training. Development uses internal group cross-validation, and an external test set stays locked until the end. If the independent groups suffice, splits holding out an entire source or an entire family are added. With three related witnesses, strong generalisation to new sources is not established merely because there are many occurrences. Impossible crossings are declared, and the analysis remains estimative.

**Kinds of label.** Labels are divided into:

- melodic family and historical neumatic type;
- alternative boundaries;
- local roles and individual concepts;
- specification-applicability judgements and landmark positions;
- notation of a particular witness.

Different judges or separate blind rounds prevent those who evaluate from simply reproducing the specifications. Which source each judge saw is recorded.

**Annotation budgets.** Four fractions of the annotated training groups are defined: 10%, 25%, 50% and 100%. The fractions are nested and common to all conditions. The main confirmatory point is 25%, provided the pilot shows that it secures the predefined family coverage. Otherwise, before the test set is opened, the smallest feasible fraction is defined and a new version of the pre-registration is issued. Five common training seeds estimate algorithmic variability; they do not count as five independent musical samples.

## P1: the value of full summation

For each candidate family and each segment, judges give a specification-applicability judgement, $Y_S\in\lbrace0,1,?\rbrace$, or a distribution of judgements. The judgement concerns the particular specification and is distinct from the family label. Hard negatives share with the positives:

- the same mode;
- a related cadence;
- similar length and surface.

If they are over-represented, the weighting is recorded, so that calibration has a clear reference rate.

The concept classifiers, the kernel, the specifications and the alignment distribution $p(\pi\vert X,f)$ are shared and fixed in the comparison. With $p_j(\pi)=q_j(U_j=1\vert X,\pi)$, two ways of computing are compared:

- **full summation (AC):**
```math
m_{\mathrm{AC}}=\sum_\pi p(\pi\vert X,f)\sum_{u\in S_f}\prod_jq_j(u_j\vert X,\pi);
```
- **pooling of marginals (Pool):**
```math
m_{\mathrm{Pool}}=\sum_{u\in S_f}\prod_j\bar q_j(u_j),\qquad \bar q_j=\mathbb E_\pi q_j.
```

The two methods receive exactly the same inputs and differ only in how they combine the same posterior. The main quantity is
```math
\Delta_{\mathrm{P1}}=\mathrm{LL}(\mathrm{Pool})-\mathrm{LL}(\mathrm{AC}),\qquad
\mathrm{LL}(p)=-\mathbb E\big[Y_S\log_2p+(1-Y_S)\log_2(1-p)\big],
```
in bits per judgement, positive in favour of full summation. Each method is calibrated separately, with the same calibrator family and the same development budget. Also reported are:

- raw log loss and the Brier score;
- calibration slope and intercept;
- the coverage curve.

Probability clipping for numerical safety is common and declared.

As a secondary mechanism analysis, the subset $\mathcal D_\tau=\lbrace\vert m_{\mathrm{AC}}-m_{\mathrm{Pool}}\vert\gt \tau\rbrace$ is examined. The threshold is set on development data, without test labels. Only on this subset can the two methods differ materially. Melismatic density and alignment entropy are reported as factors that may modify the result, without substituting for the difference in predictions. Contested judgements are kept with the distribution of judges, and results on the consensus subset are also reported together with its coverage.

## P2: the specification as a guide to alignment

**Sampling regime.** Before estimation, each dataset declares whether it is:

- a representative sample of candidates with positive and negative judgements;
- a collection of selected accepted occurrences;
- simple family sampling.

The family label does not by itself prove selection through the same specification. For the main strand of P2 a sample of candidates with checked judgements $Y_S$ is preferred, so that the conditional objective is used on the same $X$. The selected-positives version is a second, pre-declared strand, with the exact term $\log B-\log z$. Musical evaluation uses held-out annotations of roles and positions that were not used in training.

**Comparisons.** Five comparisons isolate different aspects of the result:

- **Plain EM versus estimation under the specification**, with the same $X$, templates and initialisation, while plain EM ignores the judgements. Measures the overall benefit of using the knowledge.
- **Estimation under the specification versus an equivalent constrained optimisation** of the same function. A numerical equivalence check: the two must reach the same optimum.
- **Estimation under the specification versus a flexible learned estimator** with the same concept and landmark labels, the same features and the same budget. Measures the value of structured coupling.
- **Valid versus controlled-perturbation specification**, with the same logical form, applicability, frequencies and missingness. Measures the value of the musicological content.
- **Shared kernel versus an independent kernel per family**, with controlled capacity. Measures the value of the shared role structure.

**Quantity and accompanying reports.** $\Delta_{\mathrm{P2}}$ is the reduction in mean landmark position error, measured in elementary events, with acceptable alternative positions. It is accompanied by:

- the predictive log loss of the alignment;
- non-inferiority of the normalised cross-entropy of the content.

Landmark deletion is evaluated as a separate category. A reduction in alignment entropy is only descriptive: it may simply mean overconfidence. Stability per source and parameter profiles are reported, so that different historical interpretations of the same distribution stay visible.

## E-min: transfer of the organisation of variation

E-min is a purely symbolic experiment. All conditions share:

- known boundaries and the same target;
- templates $\Pi_f$ from training data;
- topology and alphabet.

Each prior is updated with the same number of Znamenny occurrences and the same tuning budget. The family is known in this conditional task; its recognition is examined separately. The measure is cross-entropy per event:
```math
\mathrm{CE}_{\mathrm{event}}(M)=-\frac{\sum_o\log_2p_M(X_o\vert F_o,C_o,n_o)}{\sum_on_o},\qquad p_M=A_M/a_M(n).
```
The main measurement is a corpus-level ratio, with group resampling of numerators and denominators. Also reported are the mean per family, the value per occurrence, the entropy of the length and the full joint entropy. The unit of measurement does not change after the results have been seen.

| Prior | Construction | What it tests |
|-----|--------|-------|
| Flat | Symmetric distribution of equal concentration | Local learning without structure from the source |
| Byzantine | Mean transition and emission probabilities per validated role | Transfer of the distribution of variation |
| Unrelated tradition | Another documented tradition with the same symbolic bridge and exposure | General musical prior versus the particular source; if no comparable corpus is found, the specificity claim remains open |
| Shuffled roles | Reassignment of events and roles within compatible strata, preserving marginals; ten predefined reassignments | The link between role and variation; simple renaming of roles is not an adequate null |
| Role-pooled | Same source occurrences, shared kernel without roles | The added value of role dependence |
| Position only | Relative position and length, without a musicological role label | General regularities of beginning and end |

The contrasts are:

- $\Delta_{\mathrm{struct}}=\mathrm{CE}_{\mathrm{flat}}-\mathrm{CE}_B$
- $\Delta_{\mathrm{spec}}=\mathrm{CE}_{\mathrm{unrel}}-\mathrm{CE}_B$
- $\Delta_{\mathrm{role}}=\mathrm{CE}_{\mathrm{shuf}}-\mathrm{CE}_B$
- $\Delta_{\mathrm{pool}}=\mathrm{CE}_{\mathrm{pooled}}-\mathrm{CE}_B$
- $\Delta_{\mathrm{pos}}=\mathrm{CE}_{\mathrm{pos}}-\mathrm{CE}_B$

The main claim requires both $\Delta_{\mathrm{struct}}\gt \epsilon_s$ and $\Delta_{\mathrm{pool}}\gt \epsilon_r$. Specificity of the Byzantine source additionally requires a positive $\Delta_{\mathrm{spec}}$. Superiority over the position-only prior supports the musicological interpretation of the roles. This matters because cadential stability is most likely a property shared by the melodic types of many traditions.

**Practical details.** Exposure is equalised in events, lengths, number of roles, works, sources and annotation hours. The concentration of the prior is tuned on development data. A curve for the fixed values 0, 2, 8 and 32 is also reported, as a sensitivity grid with no particular empirical meaning. Local supervision for templates, roles and specifications counts towards the total cost.

**Interpretation.** Positive transfer shows that the particular structure is useful for the particular material; it does not prove historical kinship. Negative transfer may be due to:

- a wrong role mapping or an unsuitable alphabet;
- a difference in how the data were selected;
- insufficient Znamenny material;
- an unsuitable topology.

Competing explanations are checked with the priors above, with learning curves and with fit diagnostics.

## Comparison models and staging

The experiments are activated in stages, so that each additional comparison is run only when the previous ones are valid.

| Stage | Conditions | Shared information |
|----|----------|--------|
| A. Symbolic feasibility | Weighted edit distance, learned substitution matrix, family profile HMM, E-min priors | Same templates, boundaries, target and alphabet |
| B. A0 backbone | Training from scratch, self-supervised pretraining on Znamenny material, unrelated-source encoder, source with shuffled relations, B1 and B2 transfer | Same adaptation, architecture, masking, exposure and tuning |
| B′. Conditional | EISE transfer and corresponding B2 control | Only with valid checkpoints and historically documented supervision at the source |
| C. Knowledge | Valid or perturbed specification × flat or structured use, and a strong reference model with contrastive learning and prototypes | Same concepts, applicability, labels and encoder |
| D. Composition | Kernel only, Add, Vit, Pool, Pool2, MC, A1+γ, AC | Same kernel, concept classifiers, specification and access to alignment summaries |
| E. Learning | Plain EM, estimation under valid or perturbed specification, equivalent constrained optimisation, direct landmark estimator | P2, with separate held-out landmarks |
| F. Extension | Joint concept blocks, independent blocks, free joint head | Same labels, maximum block size and budget |
| G. History | Probes on frozen representations, raw-input model, kernel summaries, supervised inverse model | Same admissible context and witness notation |

The stage D conditions are defined as follows:

- **Add**: combines kernel and specification without alignment information, with a fixed heuristic placement of landmarks. Isolates the overall benefit of access to the alignment.
- **Vit**: judges the concepts on the single most probable alignment.
- **Pool**: pools concept marginals, as in P1.
- **Pool2**: additionally receives pairwise moments, without assuming that these determine every higher-order specification.
- **MC**: uses common alignment samples with sequential filtering and backward sampling, and reports error, log bias and cost.
- **A1+γ**: a free joint concept head with the same event features and the same alignment summaries $\gamma$, with equal-parameter and equal-time checks.

If a comparison model is given the full joint distribution $q^\star$, it can reproduce full summation exactly. This is an equivalence limit and a useful check.

## Statistical analysis

**Error allocation.** The extension has a total type I error budget of 0.05. It is split in advance into 0.025 for the P1–P2 chain and 0.025 for E-min. The tests of the main proposal keep their own pre-registration.

**P1–P2 chain.** The order is fixed: P1 overall, then P2 (positions and non-inferiority of the entropy), then downstream recognition (valid versus perturbed specification and $Q_{\mathrm{real}}$). Each confirmatory step opens only if the previous one succeeded. Compound claims require all their members to pass at 0.025. If P1 fails, P2 remains scientifically useful but exploratory, pending independent confirmation. Secondary contrasts are reported with Holm correction within declared families or with intervals only.

**E-min.** $\Delta_{\mathrm{struct}}$ and $\Delta_{\mathrm{pool}}$ form a single conjunctive claim at 0.025. Only after it does a Holm family open for the remaining contrasts.

**Intervals.** They are obtained by paired bootstrap of the independent groups, recomputing the exact aggregate quantity. As a computational budget, 10,000 replicates are proposed, with a pilot check of coverage; the number of replicates does not substitute for an adequate number of groups. With few groups, conservative sensitivity analyses are used. The strongest comparison model is selected only on development data.

**Margins and equivalence.** The margins $\epsilon_s,\epsilon_r,\delta_{\mathrm{P1}},\delta_{\mathrm{P2}},\delta_{\mathrm{real}}$ are set after the independent pilot and before testing, by the criteria of:

- the smallest useful improvement;
- judge repeatability;
- computational cost;
- precision of the units.

A non-significant difference does not mean equivalence. The equivalence test (TOST) requires the whole interval to lie within the pre-declared bounds.

**Power.** A preliminary simulation gave a first picture of power. Its parameters were:

- 10,000 replicates, one-sided level 0.025;
- hypothetical standard deviation of the difference 0.20;
- eight measurements per group;
- true difference 0.05.

The parameters will be re-estimated in the pilot. The unit is the judgement for P1 and the event for E-min.

| Independent groups | Power, intra-class correlation 0.1 | Power, intra-class correlation 0.5 |
|---:|---:|---:|
| 12 | 0.397 | 0.172 |
| 24 | 0.724 | 0.345 |
| 48 | 0.960 | 0.618 |
| 96 | 1.000 | 0.895 |

For joint success of six positive gates with a standardised effect size of 0.5, power is:

- 0.075–0.261 with 24 groups;
- 0.626–0.743 with 48 groups;
- about 0.989 with 96 groups.

These values come from hypothetical scenarios and do not estimate the available Znamenny sample. The power target of 0.80 is a design decision; the required number of sources will follow from the real data. If $G$ is the number of independent groups, the standard error is $\mathrm{sd}(\bar d_g)/\sqrt G$, with no second design correction.

A second simulation examined nine scenarios of known roles and alignments in a simplified binary model. It showed that the E-min comparison models distinguish positive from negative transfer according to the true structure. It does not measure real performance on Byzantine or Znamenny material.

## Decision gates

| Gate | Condition to continue | If the condition is not met | Current status |
|------|--------|--------|-----|
| G0. Sources | Rights, independent labels, dependence groups, adequate role coverage | Restriction to an estimative study; stop if provenance cannot be checked or the main targets are circular | Inventory designed; corpus not assembled |
| G1. Computation | Agreement with reference checks, normalisation, gradients, measured memory at real sizes | Fix the compiler or use a tested approximation | Synthetic checks passed; real sizes pending |
| G2. P1 | Lower bound of the improvement above $\delta_{\mathrm{P1}}$ | If equivalence is established, use the cheaper Pool | Not yet run on musical material |
| G3. P2 | Improvement in positions and non-inferiority of the entropy with the correct objective | Local kernel without updating from the specification | Synthetic consistency confirmed; musical material pending |
| G4. Recognition | Benefit over the strongest comparison model, valid versus perturbed specification, $Q_{\mathrm{real}}$ | Restrict the claim to calibration and alignment | Not yet run |
| E-min | Both $\Delta_{\mathrm{struct}}$ and $\Delta_{\mathrm{pool}}$, with adequate groups | Negative or uncertain transfer is reported; the local study continues | Simulations passed; musical material pending |

The pilot of 10–20 passages estimates cost, quality, frequencies and the suitability of the unit. The indicative targets, at least five family specifications and one hundred landmark annotations, serve planning and are not statistical thresholds. A negative result does not invalidate the programme. It makes it possible to separate problems of the data from those of the musicological hypothesis, the model and the transfer.

# Relation to previous research

Computational study of Znamenny notation has been developed mainly by the group of I. V. Bakhmutova, V. D. Gusev and T. N. Titkova at the Sobolev Institute of Mathematics in Novosibirsk.

- Their first articles, in the late 1990s, introduced variable-length context alphabets for decoding the notation.
- They also proposed larger structural units as units of reading.
- The 2010 study of Metallov's collection, discussed above, raised the questions of coverage, variation and naming of the popevki.
- In 2015 the same authors sought, in two-notation manuscripts, sign chains with a unique or dominant interpretation per mode, and tested them on independent material.
- In 2020, with L. A. Miroshnichenko, they presented approaches to reading manuscripts without *pomety*.
- In 2022 they quantified admissible variation by comparing hymns of the same title across different witnesses.

Throughout this line the object measured is the reading of the notation. The present work turns to a different object: family identity, judged independently, and its relation to variation.

In symbolic music information retrieval, the question of melodic families has been studied mainly in folk songs.

- Volk and van Kranenburg (2012) showed that experts assign melodies to families by explicit criteria, but that no single feature acts as a universal core.
- Bountouridis and colleagues (2017a) built profile HMMs from multiple alignments of melody families, with match, insert and delete states, Baum–Welch training and pseudocounts, and used them for retrieval and classification. Using the marginal probability of a profile HMM as a family likelihood thus has a direct musical precedent. In a second paper (Bountouridis et al., 2017b) they learned substitution matrices from alignment columns and showed that melodic stability varies with position within the melody; they also examined the transfer of these matrices between corpora.
- Karsdorp, van Kranenburg and Manjavacas (2019) learned melodic similarity metrics with shared family membership as the source of positive pairs.
- Conklin (2021) evaluated the mining of recurring patterns in neume sequences of Mozarabic chant against musicological annotation.
- Lanz and Hajič (2025) showed that the segmentation of Gregorian chant that is optimal for memorisation does not coincide with the theory of centonate composition.

Given this, the kernel $\kappa$ is not presented as a new conception. The contribution under investigation lies in three places:

- in making variation depend on independently documented structural roles;
- in transferring this dependence between traditions;
- in linking it to the musicological specifications.

The computational operations of the scheme are also well known.

- **Structured prediction.** Joint estimation of boundaries and labels with a semi-Markov CRF goes back to Sarawagi and Cohen (2004). Training from partial annotation is also established (Tsuboi et al., 2008).
- **Probability of satisfying a logical constraint.** Xu et al. (2018) formulated it as a semantic loss. Ahmed et al. (2022) embedded it in probabilistic circuits that normalise the prediction under the constraint. Van Krieken et al. (2024) showed that the independence assumption on concepts pushes models towards deterministic solutions, and that mixtures of independent distributions fix the problem only in part. The distribution $q^\star_f$ is exactly such a mixture, with alignments as its components.
- **Exact dynamic programming over an HMM–automaton product.** It has been used to control text generation under logical constraints (Zhang et al., 2023, 2024). As an operation it reduces to weighted automaton composition (Mohri, Pereira and Riley, 2002).
- **Neurosymbolic automata.** They link neural perception with symbolic automata and exact inference, but with a known position for each symbol (Manginas, Paliouras and De Raedt, 2025). Relational neurosymbolic Markov models generalise to latent relational states with approximate inference (De Smet et al., 2025). With a fixed alignment, the scheme of this appendix reduces to a neurosymbolic automaton over the sequence of landmarks. The latent position of the concepts adds a musically interpretable grounding, not a new general principle.
- **Constraints on latent alignment during learning.** These are known as posterior regularisation (Ganchev et al., 2010) and have been applied to word alignment with HMMs (Graça, Ganchev and Taskar, 2010).
- **Music graphs.** Libraries and graph convolution layers for symbolic music (Karystinaios and Widmer, 2024; Karystinaios, Foscarin and Widmer, 2024) provide an alternative encoder with the same admissible features.

The minimal mathematical difference between full summation and pooling of marginals can be written exactly. For a conjunctive rule $U_1\wedge U_2$ and a fixed alignment posterior,
```math
m_{\mathrm{AC}}-m_{\mathrm{Pool}}=\mathrm{Cov}_\pi\big(q_1(\pi),q_2(\pi)\big),
```
while for a disjunctive rule the sign is reversed, and for a general specification higher-order mixed moments appear. With a single concept or a certain alignment the difference vanishes. This is a known property of mixtures. The experimental comparison must therefore distinguish three things:

- the information available;
- the way it is compressed;
- the cost of using it.

In the opposite direction, the relation $p(\pi\vert X,S)\propto p(\pi\vert X)\,Q(X,\pi)$ reshapes the distribution of alignments. Musical identity thus indicates which uncertain placements agree with the criteria of the family. The value of this mechanism is established only if the new placements agree with independent musicologists on passages not used in training.

The contribution of the programme is therefore judged at four levels, each with its own criterion.

- **A research resource for symbolic music information retrieval.** Requires a checked corpus, independent family labels, joint estimation of boundaries and family, whole-source hold-out, strong reference models and full recording of uncertainty. Simple relabelling of a dictionary's chains or a random split of related occurrences is not enough.
- **A compositional architecture for musicologically informed learning.** Requires a positive P1 or an independently confirmed P2 against fair comparison models (Pool, Vit, A1+γ, EM), a specific musicological finding and success at the $Q_{\mathrm{real}}$ gate. Superiority only over Add, which has no alignment information, is not enough.
- **Transfer of the organisation of variation.** Requires a positive E-min against the role, position and unrelated-tradition controls, with robustness on new sources. An overall improvement from encoder transfer, which mixes weights, labels and kernel, is not enough.
- **General machine learning.** Requires an additional theoretical or algorithmic result for the restricted model family defined here, empirical evaluation in a second domain with latent alignment, and identical supervision across comparisons. The result may be:
    - a representation or non-identifiability theorem;
    - a non-trivial bound on sample complexity or state complexity against probabilistic circuits and weighted automata.

  Constructing a product automaton, or observing that a joint distribution is more expressive than a product, is not enough.

# Timeline and publications

The extension is activated from month 36, provided the core of the dissertation has advanced and resources are available. Durations are preliminary estimates and do not assume that the corpus and licences are already secured.

| Phase | Duration and roles | Deliverable | Decision |
|-------|-----|---------|-----|
| E0. Sources and pilot | 4–6 weeks; Znamenny chant expert, data manager, second judge | Source records, licence check, 10–20 passages, double labels, boundary uncertainty, cost per checked event | G0 |
| E1. Symbolic implementation | 4–6 weeks; machine learning researcher, weekly expert review | Templates and roles from training data, reference models, exact computation of $B_f$ and $z_f$, validity checks | G1 |
| E2. Pre-registration | 3–5 weeks, partly in parallel with E1 | Variance and correlation estimates, margins, power and cost simulation, final splits | Confirmatory or estimative scale, before testing |
| E3. P1, P2, E-min | 6–10 weeks; CPU computation, annotation of held-out passages | Equal-information comparisons, objective check, learning curves | G2, G3, E-min |
| E4. Backbone and recognition | 6–10 weeks; shared GPU budget | Encoder transfer, specifications on Znamenny material, calibration, unknown family, $Q_{\mathrm{real}}$ | G4 |
| E5. Historical recovery | 4–8 weeks, if source-linked notation exists | Per-witness recovery, multiple acceptable answers, risk–coverage curves | Evaluation with explicit identifiability limits |
| E6. Optional extension | One additional cycle | Joint concept blocks against a free head of equal budget | Only if residual dependence is documented |

Parallel execution concerns only the allocation of resources and does not override the order of confirmatory tests. New sources after testing require a new corpus version and a new test set.

The computational budget is set at up to twenty development configurations per method family and five common seeds in the final evaluation, with early stopping of inadequate conditions by pre-declared criteria. Each run records:

- symbols, annotated events and source groups;
- trainable parameters;
- compute time and peak memory;
- hours of human annotation.

Savings come from:

- caching of profiles and concepts;
- common fixed distributions for P1 and common predictions for Pool, Vit and AC;
- activating neural transfer only after the symbolic protocol has been verified.

$Z_f$ is computed only where a normalised density is required.

Depending on the results, four publication directions are foreseen, which may be merged into fewer so that the same experiment is not fragmented.

- **A research resource for symbolic music information retrieval.** A checked, legally available reference corpus for the popevki, with provenance documentation, independent labels, source-wise splits and strong reference models. It has value of its own even if transfer from the Byzantine tradition fails.
- **Musicologically informed learning.** Identity and variation as a two-way relation, through P1 and P2 and the musicological analysis of the cases where the alignment changes. A calibration benefit will not be presented as a recognition benefit, and local success will not be confused with transfer.
- **Comparative musicology of variation.** E-min and the historically documented role mapping: which part of admissible variation transfers, with how much local supervision. Every historical claim will rest on the primary sources, independently of predictive performance.
- **General machine learning.** Only if E6 yields the additional theoretical or algorithmic result and an evaluation in a second domain.

# Interpretation and limits

The appendix delivers three things: a defined research object, an executable framework on synthetic data and a predefined experimental plan. It provides no evidence of effectiveness on real popevki. The numerical checks confirm:

- internal identities and normalisations;
- edge cases;
- agreement with exhaustive enumeration in finite spaces.

The next piece of evidence must come from independently assembled musical cases, from independent judgement of specification applicability and from agreement between model and experts on a locked test set.

The small size of a pilot does not justify strong generalisation claims because many events come from the same witnesses; the unit of independence is the source group. Successful transfer does not prove historical descent of one tradition from the other. Every conclusion about historical notations concerns a particular surviving witness, not a single archetype. Identifiability limits and alternative musicological readings are part of the result, not noise to be removed after inspection.

# References

## Musicological sources and studies

Arvanitis, I. (2010). *O rythmos ton ekklesiastikon melon mesa apo tin palaiographiki erevna kai tin exigisi tis palaias simeiografias* [The rhythm of ecclesiastical chants through palaeographic research and the exegesis of the old notation] (Doctoral dissertation). Ionian University. <https://doi.org/10.12681/eadd/21885>

Bakhmutova, I. V., Gusev, V. D., & Miroshnichenko, L. A. (2022). Количественные оценки допустимой вариативности в задаче нотолинейной реконструкции знаменных песнопений [Quantitative estimates of admissible variability in the staff-notation reconstruction of Znamenny chants]. *Проблемы музыкальной науки / Music Scholarship*, 49(4), 98–106. <https://doi.org/10.17674/2782-3601.2022.4.098-106>

Bakhmutova, I. V., Gusev, V. D., & Titkova, T. N. (2010). Компьютерный анализ и восстановление знаменной составляющей подборки В. М. Металлова [Computer analysis and reconstruction of the Znamenny component of V. M. Metallov's collection]. *Сибирский музыкальный альманах* (Novosibirsk), 62–81.

Bakhmutova, I. V., Gusev, V. D., & Titkova, T. N. (2015). Использование билингв «знамя – нота» для выявления инвариантных структурных единиц знаменного распева [Using "sign–note" bilingual sources to identify invariant structural units of Znamenny chant]. *Проблемы музыкальной науки / Music Scholarship*, 2(19), 5–11. <https://doi.org/10.17674/1997-0854.2015.2.19.005-011>

Conomos, D. E. (Ed.). (1985). *The treatise of Manuel Chrysaphes, the Lampadarios* (Monumenta Musicae Byzantinae, Corpus Scriptorum de Re Musica 2). Vienna: Verlag der Österreichischen Akademie der Wissenschaften.

Gheorghiță, N. (2010). Observations on the technique of transcription (exegesis) into the New Method of analytical music notation of the Sunday koinonikon of the 18th century. *Studii și Cercetări de Istoria Artei. Teatru, Muzică, Cinematografie*, 4(48), 9–26.

Grigorjeva, V. (2023). Principles of stratification of melodic formulas of Old Russian out-of-ichos chants. *St. Tikhon's University Review. Series V: Christian Art*, 50, 9–23. <https://doi.org/10.15382/sturv202350.9-23>

Gusev, V. D., Bakhmutova, I. V., Miroshnichenko, L. A., & Titkova, T. N. (2020). Possible approaches to deciphering Russian ancient Znamenny chant. *Journal of New Music Research*, 49(3), 298–306. <https://doi.org/10.1080/09298215.2020.1762666>

Hannick, C., & Wolfram, G. (Eds.). (1985). *Gabriel Hieromonachos: Abhandlung über den Kirchengesang* (Monumenta Musicae Byzantinae, Corpus Scriptorum de Re Musica 1). Vienna: Verlag der Österreichischen Akademie der Wissenschaften.

Karagkounis, K. Ch. (2003). *I paradosi kai exigisi tou melous ton Cheroubikon tis byzantinis kai metabyzantinis melopoiias* [The tradition and exegesis of the melos of the Cherubic hymns in Byzantine and post-Byzantine composition] (Meletai 7). Athens: Institute of Byzantine Musicology.

Karagkounis, K. Ch. (2005). *Paraleipomena peri tou Cheroubikou hymnou* [Supplements on the Cherubic hymn]. Volos.

Mavromatis, P. (2005). *The echoi of modern Greek church chant in written and oral transmission: A computational model and its cognitive implications* (Doctoral dissertation). Eastman School of Music, University of Rochester.

Metallov, V. M. (1899). *Осмогласие знаменного распева* [The eight modes of Znamenny chant]. Moscow.

Parfentiev, N. P., & Parfentieva, N. V. (2023). Stroganovs' master of church-singing art Faddey Subotin at the court of Tsar Alexei Mikhailovich. *Journal of Siberian Federal University. Humanities & Social Sciences*, 16(7), 1112–1126.

Rabinovitch, G., & Carter-Enyi, A. (2024). Melodic organization and sequential ordering of galant schemata: Implications for eighteenth-century European musicianship. *Music Theory Online*, 30(1). <https://doi.org/10.30535/mto.30.1.7>

## Computational musicology and machine learning

Ahmed, K., Teso, S., Chang, K.-W., Van den Broeck, G., & Vergari, A. (2022). Semantic probabilistic layers for neuro-symbolic learning. *Advances in Neural Information Processing Systems 35*.

Bountouridis, D., Brown, D., Koops, H. V., Wiering, F., & Veltkamp, R. C. (2017a). Melody retrieval and classification using biologically-inspired techniques. In *Computational Intelligence in Music, Sound, Art and Design (EvoMUSART 2017)*, LNCS 10198, 49–64. <https://doi.org/10.1007/978-3-319-55750-2_4>

Bountouridis, D., Brown, D. G., Wiering, F., & Veltkamp, R. C. (2017b). Melodic similarity and applications using biologically-inspired techniques. *Applied Sciences*, 7(12), 1242. <https://doi.org/10.3390/app7121242>

Conklin, D. (2021). Mining contour sequences for significant closed patterns. *Journal of Mathematics and Music*. <https://doi.org/10.1080/17459737.2021.1903591>

De Smet, L., Venturato, G., De Raedt, L., & Marra, G. (2025). Relational neurosymbolic Markov models. *Proceedings of the AAAI Conference on Artificial Intelligence*, 16181–16189.

Ganchev, K., Graça, J., Gillenwater, J., & Taskar, B. (2010). Posterior regularization for structured latent variable models. *Journal of Machine Learning Research*, 11, 2001–2049.

Graça, J. V., Ganchev, K., & Taskar, B. (2010). Learning tractable word alignment models with complex constraints. *Computational Linguistics*, 36(3), 481–504.

Karsdorp, F., van Kranenburg, P., & Manjavacas, E. (2019). Learning similarity metrics for melody retrieval. *Proceedings of ISMIR 2019*, 478–485.

Karystinaios, E., Foscarin, F., & Widmer, G. (2024). Perception-inspired graph convolution for music understanding tasks. *Proceedings of IJCAI 2024*, 7681–7689.

Karystinaios, E., & Widmer, G. (2024). GraphMuse: A library for symbolic music graph processing. *Proceedings of ISMIR 2024*. arXiv:2407.12671.

Klugkist, I., Kato, B., & Hoijtink, H. (2005). Bayesian model selection using encompassing priors. *Statistica Neerlandica*, 59(1), 57–69. <https://doi.org/10.1111/j.1467-9574.2005.00279.x>

Lanz, V., & Hajič Jr., J. (2025). Gregorian melody, modality, and memory: Segmenting chant with Bayesian nonparametrics. *Proceedings of ISMIR 2025*. <https://doi.org/10.5281/zenodo.17811449>

Manginas, N., Paliouras, G., & De Raedt, L. (2025). NeSyA: Neurosymbolic automata. *Proceedings of IJCAI 2025*, 5950–5958.

Mohri, M., Pereira, F., & Riley, M. (2002). Weighted finite-state transducers in speech recognition. *Computer Speech & Language*, 16(1), 69–88.

Sarawagi, S., & Cohen, W. W. (2004). Semi-Markov conditional random fields for information extraction. *Advances in Neural Information Processing Systems 17*, 1185–1192.

Tsuboi, Y., Kashima, H., Mori, S., Oda, H., & Matsumoto, Y. (2008). Training conditional random fields using incomplete annotations. *Proceedings of COLING 2008*, 897–904.

van Krieken, E., Minervini, P., Ponti, E. M., & Vergari, A. (2024). On the independence assumption in neurosymbolic learning. *Proceedings of ICML 2024*, PMLR 235, 49078–49097.

Volk, A., & van Kranenburg, P. (2012). Melodic similarity among folk songs: An annotation study on similarity-based categorization in music. *Musicae Scientiae*, 16(3), 317–339. <https://doi.org/10.1177/1029864912448329>

Xu, J., Zhang, Z., Friedman, T., Liang, Y., & Van den Broeck, G. (2018). A semantic loss function for deep learning with symbolic knowledge. *Proceedings of ICML 2018*, PMLR 80, 5502–5511.

Zhang, H., Dang, M., Peng, N., & Van den Broeck, G. (2023). Tractable control for autoregressive language generation. *Proceedings of ICML 2023*, PMLR 202.

Zhang, H., Kung, P.-N., Yoshida, M., Van den Broeck, G., & Peng, N. (2024). Adaptable logical control for large language models. *Advances in Neural Information Processing Systems 37*.

# Technical appendix: numerical checks and reproduction

## What has been executed

The mathematical specification is accompanied by small reference implementations, result files, a draft data schema, protocol settings and a reproducible check suite. All runs concern synthetic distributions and small spaces enumerated exhaustively. To date:

- no neural music encoder has been trained;
- no B1, B2 or EISE checkpoints have been loaded;
- no corpus has been assembled from the manuscripts.

| Object of check | File | Result |
|----------|------------|--------------|
| Semi-Markov recursions | `toy_semimarkov_checks.py` | 291 checks passed; maximum deviation about $3.6\times10^{-15}$ |
| Basic profile HMM | `profile_hmm_regression_oracle.py` | 5 groups passed; counterexample showing that normalisation fails without the transition to the end |
| Alignments and diagnostic concepts | `alignment_product_oracle.py` | 16 groups passed, including the expected failure of naive prefix reuse |
| Emission history in the computation of $Z_f$ | `oracle_Zf_context_counterexample.py` | Reproduces the three errors of a computation that did not update the history |
| Profile, outer dynamic programme, generative model | `profile_semantics_oracle.py` | 221 checks passed; maximum deviation $1.56\times10^{-10}$, including finite-difference gradients |
| Product dynamic programme with history | `ecsi_kappa_context_oracle.py` | 308 checks passed; relative errors of $Z_f$ below $4\times10^{-16}$ |
| Kernel estimation | `bidirectional_learning_oracle.py` | 43 checks passed; EM monotonicity, agreement with direct optimisation, selected-sample consistency |
| Power and transfer | `power_and_transfer_simulation.py` | 50 power scenarios and 9 transfer scenarios; all checks passed |

The first four files are in the `original_oracles/` subfolder. The numbers correspond to programmatic checks or groups of checks, as recorded in the result files. They are not independent musical experiments. The largest overall deviation in the file of the product dynamic programme with history (about $8.44\times10^{-7}$) is due to the convergence tolerance of a numerical optimiser, not to an error in the recursion.

## Small-scale kernel estimation

The estimation check uses:

- a binary emission row in a two-column profile;
- a two-symbol alphabet and known length 3;
- fixed concepts and topology.

The counts come from the exact population of a selected-data model with true parameter $\theta=0.72$; they are not an independent real sample.

| Objective | Estimate of $\theta$ | Interpretation |
|--------|-----|-----------|
| Plain EM on content | 0.9686 | Selected data do not represent the population of the unconstrained profile |
| Joint EM on positives | 0.99999 (at the boundary) | Maximises a different function |
| Correct selection likelihood | 0.72000 | Recovers the parameter of the model that generated the data |

The EM objectives increase at every iteration and agree with direct one-dimensional optimisation. The total $z$ agrees with exhaustive enumeration to within $2.78\times10^{-17}$. The joint-block check reproduces an equality probability of 1 against 0.5 with identical marginals.

## Invariants before musical application

Before training on musical material, every implementation must verify:

- **Normalisation.** Every row of transition and emission probabilities sums to one, including the transition to the end, on random profiles and lengths up to 100.
- **Single counting.** Each alignment and each concept assignment is counted once. Enumeration equals the dynamic programme for all 255 non-empty specifications over three concepts.
- **Bounds.** $B\le A$, $z\le a$ and $0\le m,Z\le1$ hold for every real specification and every training point.
- **History.** Insertions update the emission history.
- **Prefix reuse.** Allowed only when the internal factors do not depend on the segment end.
- **Selected density.** Sums to one for fixed length, and the gradient (7) agrees with finite differences.
- **Background.** The correspondence between skip and length-1 background is bijective.
- **Partial supervision.** The loss agrees with enumeration and vanishes on a fully unannotated region.
- **Generative interpretation.** The generative posterior and the CRF coincide under the correct assumptions.
- **No circular inputs.** The list of admissible features and the provenance of labels are checked automatically.

## Measured cost

In a single Python run, the dynamic programme for an observed sequence took:

- about 0.09 seconds for $(J,\vert V\vert,n,W)=(4,8,32,2)$;
- about 0.40 seconds for $(8,16,64,2)$.

Summing over emissions with a previous-symbol state for $(4,8,16,2)$ took about 1.6 seconds. These are synthetic cases. The real $J$, $L$ and $W$ have not been measured, and the pilot will record their distributions together with the cost of scoring all candidate segments.

The minimal working implementation is considered complete when:

1. one real family and its hard negatives have checked records;
2. the normalised profile and the specification give the same result in the reference check and in the compiled dynamic programme;
3. Pool, Vit and AC use the same data;
4. the zero-order decoder handles full works, partial labels, the unknown family and skips;
5. reports are organised by source group and include all three $Q_{\mathrm{real}}$ tests.

## Reproduction

Python 3 with NumPy and SciPy is required; the exact versions are recorded in `validation_summary.json`. From the extension's `support/` folder:

```bash
python3 run_all_checks.py
```

The command runs all checks and records exit codes, times and log files. The original reference implementations are kept unchanged in the `original_oracles/` subfolder, separate from the corrected code. The primary articles and digitisations are not redistributed; the checks do not need them, because they contain their own small examples.

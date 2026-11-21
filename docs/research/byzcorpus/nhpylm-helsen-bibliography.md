# Βιβλιογραφία και τεκμηρίωση — Μελωδική κατάτμηση, NHPYLM και οικογένειες θέσεων

**Ερευνητική βιβλιογραφία του ByzCorpus, 18 Νοεμβρίου 2026**

[Μαθηματική μελέτη NHPYLM–Helsen](nhpylm-helsen-mathematical-study.md) · [Πειραματική τεκμηρίωση](nhpylm-helsen-extended-experiments.md) · [ByzCorpus](README.md) · [Μ1-X](../m1-x-design.md) · [English bibliography](../../../en/docs/research/byzcorpus/nhpylm-helsen-bibliography.md) · [BibTeX](nhpylm-helsen-references.bib)

## Βιβλιογραφική τοποθέτηση

Η βιβλιογραφία οργανώνεται γύρω από τέσσερις διακριτές ερευνητικές περιοχές: (α) τις μουσικολογικές αναλύσεις που προσδιορίζουν τις δομικές μονάδες στις ψαλτικές παραδόσεις, (β) την μη εποπτευόμενη επαγωγή στατιστικών τμημάτων, (γ) την κοινή πρόβλεψη ορίων και κατηγοριών πλήρους μονάδας και (δ) τη σχεδίαση έγκυρων συγκριτικών πρωτοκόλλων. Η ανάλυση του Helsen αποτελεί άμεση μουσικολογική αναφορά για την αξιολόγηση σε γρηγοριανά responsoria. Η βυζαντινή εργασία θα βασιστεί σε ανεξάρτητες επισημειώσεις θέσεων και σε πηγοκριτικά ελεγμένες εμφανίσεις από Κοινωνικά και Χερουβικά.

Το κεντρικό ερευνητικό ερώτημα είναι η σχέση ανάμεσα στα μικρά στατιστικά τμήματα και στη δομική ταυτότητα μεγαλύτερων μελωδικών μονάδων που εμφανίζονται σε διαφορετικές πραγματώσεις. Το ερώτημα αυτό συνδυάζει ανάλυση ορίων, μοντελοποίηση παραλλαγής και αναγνώριση οικογενειών σε συνεχή συμβολική ακολουθία. Η σχετική υπολογιστική συνεισφορά εξετάζεται με κοινά δεδομένα, ίδια πρωτόκολλα και άμεσο έλεγχο της προστιθέμενης αξίας κάθε αρχιτεκτονικού μηχανισμού.

## Κριτική αντιστοίχιση προηγούμενης έρευνας και νέων ερωτημάτων

| Πεδίο | Βασικά προηγούμενα | Ποιο ερώτημα υποστηρίζουν | Επόμενη πειραματική χρήση |
|---|---|---|---|
| Γρηγοριανή μορφολογία | Helsen 2008, 2009 · Lanz & Hajič 2025 · Cornelissen κ.ά. 2020 | Μελωδική τμηματοποίηση και φυσικές μονάδες | Ομαδοποιημένη αξιολόγηση ορίων, μελωδικής ομοιότητας και οικογενειακών ετικετών |
| Βυζαντινή θέση και εξήγηση | Gheorghiță 2009, 2010 · Καραγκούνης 2003 · Μαυρομάτης 2005/2006/2009 | Ιστορική και μουσικολογική ταυτότητα θέσης και οργάνωση πραγματώσεων | Ανεξάρτητη επισημείωση, οικογενειακές κατηγορίες και έλεγχος μελωδικών σχέσεων |
| Μη παραμετρικά μοντέλα | Teh 2006 · Mochihashi κ.ά. 2009 · Goldwater κ.ά. 2009 | Επαγωγή μικρών επαναλαμβανόμενων μονάδων | NHPYLM baseline, κατανομή μηκών, bits ανά φθόγγο |
| Κοινή κατάτμηση–κατηγορία | Uchiumi κ.ά. 2015 · Fujii κ.ά. 2017 | Συνδυασμός ορίων, λανθανουσών ετικετών και περιορισμένης εποπτείας | Μουσικό PYHSMM, καμπύλες εποπτείας, οικογένειες |
| Πρόβλεψη πλήρους span | Lafferty κ.ά. 2001 · Sarawagi & Cohen 2004 · Kong κ.ά. 2016 | Ακριβή όρια μαζί με ταυτότητα τμήματος | Semi-CRF A/C_fac, LASM, ablations |
| Επιλογή δομής | Stolcke & Omohundro 1992/1994 · Rissanen 1978 · Mavromatis 2009 | Μάθηση κοινών καταστάσεων και επιλογή πολυπλοκότητας | HMM/MDL ως αρχιτεκτονικός έλεγχος |
| Ερμηνεία αποτελεσμάτων | Efron & Tibshirani 1993 · Dror κ.ά. 2018 · Richard κ.ά. 2024 | Ζευγαρωτές συγκρίσεις, διάστημα αβεβαιότητας και ενημερωμένη μηχανική μάθηση | Κριτήρια αναπαραγωγής και αποτίμηση μουσικολογικής γνώσης |

Οι μουσικολογικές εργασίες προσδιορίζουν το ιστορικό και αναλυτικό αντικείμενο. Η παρούσα ερευνητική επέκταση εστιάζει σε συστηματική υπολογιστική επαλήθευση, κοινή αναγνώριση ορίων και οικογενειών και σύγκριση μηχανισμών μάθησης σε νέα πλήρη έργα.


## A. Γρηγοριανό μέλος, ψηφιακά σώματα και τμηματοποίηση

### Katherine Eve Helsen (2008) — The Great Responsories of the Divine Office: Aspects of Structure and Transmission

**Δημοσίευση:** Διδακτορική διατριβή, Universität Regensburg. **Πηγή:** [The Great Responsories of the Divine Office: Aspects of Structure and Transmission](https://doi.org/10.5283/epub.10769).

**Συμβολή στη μελέτη:** Βασική πρωτογενής πηγή για τις μουσικολογικές κατηγορίες και το συνοδευτικό παράρτημα. Στη συγκριτική μελέτη χρησιμοποιούνται συγκεκριμένες επισημειωμένες εμφανίσεις και όρια, με ξεχωριστή τεκμηρίωση στοίχισης CantusCorpus–Helsen.

### Kate Helsen (2009) — The use of melodic formulas in responsories: constancy and variability in the manuscript tradition

**Δημοσίευση:** Plainsong & Medieval Music (Cambridge University Press). **Πηγή:** [The use of melodic formulas in responsories: constancy and variability in the manuscript tradition](https://www.cambridge.org/core/journals/plainsong-and-medieval-music/article/abs/use-of-melodic-formulas-in-responsories-constancy-and-variability-in-the-manuscript-tradition/D82597960C71064CD026D94E3A24DF3B).

**Συμβολή στη μελέτη:** Αναλύει την ποικιλότητα και τη σταθερότητα μελωδικών σχημάτων στο χειρόγραφο Paris lat. 12044. Ενισχύει τη σύνδεση αναλυτικής ετικέτας και πολλαπλών πραγματώσεων χωρίς να προεξοφλεί συγκεκριμένη υπολογιστική αρχιτεκτονική.

### Bas Cornelissen, Willem Zuidema και John Ashley Burgoyne (2020) — Mode Classification and Natural Units in Plainchant

**Δημοσίευση:** Proceedings of ISMIR 2020, 869–875. **Πηγή:** [Mode Classification and Natural Units in Plainchant](https://bascornelissen.nl/work/2020/mode-classification/ISMIR2020-paper.pdf).

**Συμβολή στη μελέτη:** Θεμελιώνει τη χρήση φυσικών μονάδων/τμηματοποιήσεων στη μοντελοποίηση του γρηγοριανού μέλους και τη σχέση της αναπαράστασης με την τροπική ταξινόμηση. Η δική μας εργασία εξετάζει ρητά τα μουσικολογικά όρια Helsen.

### Bas Cornelissen, Willem Zuidema και John Ashley Burgoyne (2020) — Studying Large Plainchant Corpora Using chant21

**Δημοσίευση:** 7th International Conference on Digital Libraries for Musicology. **Πηγή:** [Studying Large Plainchant Corpora Using chant21](https://dare.uva.nl/id/db66bda1-ccdb-4c02-9ee0-dd20a341e893).

**Συμβολή στη μελέτη:** Τεκμηριώνει την υπολογιστική αναπαράσταση μεγάλων σωμάτων γρηγοριανής ψαλτικής και τη διαλειτουργικότητα με μουσικολογικά εργαλεία. Σχετίζεται με τη συμβολική επεξεργασία και τον έλεγχο πηγών.

### Vojtěch Lanz και Jan Hajič Jr. (2025) — Gregorian Melody, Modality, and Memory: Segmenting Chant with Bayesian Nonparametrics

**Δημοσίευση:** Proceedings of ISMIR 2025, 638–646. **Πηγή:** [Gregorian Melody, Modality, and Memory: Segmenting Chant with Bayesian Nonparametrics](https://doi.org/10.5281/zenodo.17811449).

**Συμβολή στη μελέτη:** Κεντρικό άμεσο προηγούμενο εφαρμογής NHPYLM στο γρηγοριανό μέλος. Ο επανέλεγχος του προεπιλεγμένου L_max και η συγκριτική αξιολόγηση με Helsen αποτελούν αυτοτελή νέα πειραματικά ερωτήματα του παρόντος έργου.


## Β. Βυζαντινή θέση, ιστορικές πηγές και υπολογιστική μελολογία

### Panayotis Mavromatis (2005) — The Echoi [Modes] of Modern Greek Church Chant in Written and Oral Transmission: A Computational Model and Its Cognitive Implications

**Δημοσίευση:** PhD dissertation, Eastman School of Music, University of Rochester. **Πηγή:** [The Echoi [Modes] of Modern Greek Church Chant in Written and Oral Transmission: A Computational Model and Its Cognitive Implications](https://steinhardt.nyu.edu/people/panayotis-mavromatis).

**Συμβολή στη μελέτη:** Υπολογιστική περιγραφή μελωδικής οργάνωσης, τροπικών σχέσεων και διαφοροποιήσεων πραγμάτωσης στη νεότερη ελληνική ψαλτική. Η διατριβή αποτελεί ανεξάρτητο μουσικοϋπολογιστικό προηγούμενο για τη μελέτη μελωδικών σχημάτων και ακολουθιών.

### Panayotis Mavromatis (2006) — A Hidden Markov Model of Melody Production in Greek Church Chant

**Δημοσίευση:** Computing in Musicology, 14, 93–112. **Πηγή:** [A Hidden Markov Model of Melody Production in Greek Church Chant](https://www.ccarh.org/publications/books/cm/vol/14/).

**Συμβολή στη μελέτη:** Εφαρμογή HMM σε ελληνικό εκκλησιαστικό μέλος με επιλογή δομής και συσχέτιση με τονισμό, σύνταξη και μελωδικές συνέχειες. Στο ερευνητικό σχέδιο αξιοποιείται ως προηγούμενο εκμάθησης κοινών δομικών καταστάσεων.

### Panayotis Mavromatis (2009) — Minimum description length modelling of musical structure

**Δημοσίευση:** Journal of Mathematics and Music, 3(3), 117–136. **Πηγή:** [Minimum description length modelling of musical structure](https://doi.org/10.1080/17459730903313122).

**Συμβολή στη μελέτη:** Αναπτύσσει κριτήριο MDL για HMM πεπερασμένου αλφαβήτου και δείχνει εφαρμογή σε μελωδικό τύπο ελληνικού εκκλησιαστικού μέλους. Η εργασία παρέχει εναλλακτικό μηχανισμό επιλογής δομικής πολυπλοκότητας, διακριτό από τον περιγραφικό κώδικα λεξικού του Stage 3.

### Panayotis Mavromatis (2009) — HMM Analysis of Musical Structure: Identification of Latent Variables Through Topology-Sensitive Model Selection

**Δημοσίευση:** Mathematics and Computation in Music (MCM 2009), Springer. **Πηγή:** [HMM Analysis of Musical Structure: Identification of Latent Variables Through Topology-Sensitive Model Selection](https://link.springer.com/book/10.1007/978-3-642-02394-1).

**Συμβολή στη μελέτη:** Η επιλογή τοπολογίας και λανθανουσών καταστάσεων προσφέρει συγκριτική οδό για μοντέλα που συνδέουν διαφορετικές μελωδικές πραγματοποιήσεις. Η αναφορά χρειάζεται ανάγνωση στο πλήρες κεφάλαιο πριν από τεχνική αναπαραγωγή.

### Nicolae Gheorghiță (2009) — Chinonicul duminical în perioada post-bizantină (1453–1821): Liturgică și muzică

**Δημοσίευση:** Bucharest: Editura Sophia. **Πηγή:** [Chinonicul duminical în perioada post-bizantină (1453–1821): Liturgică și muzică](https://www.academia.edu/49094074/Chinonicul_duminical_%C3%AEn_perioada_post_bizantin%C4%83_1453_1821_Liturgic%C4%83_%C8%99i_muzic%C4%83).

**Συμβολή στη μελέτη:** Ιστορική και μορφολογική μελέτη των κυριακάτικων Κοινωνικών, των οικογενειών τύπων, των συμβολικών σημείων και των εξηγήσεών τους. Η μουσικολογική ανάλυση καθοδηγεί την επιλογή πηγών, την οριοθέτηση και τον ανεξάρτητο έλεγχο οικογενειών στο ByzCorpus.

### Nicolae Gheorghiță (2010) — Observations on the technique of transcription (ΕΞΗΓΗΣΙΣ) into the new method of analytical music notation of the Sunday koinonikon of the 18th century

**Δημοσίευση:** Studii şi Cercetări de Istoria Artei, seria TMC, 4(48). **Πηγή:** [Observations on the technique of transcription (ΕΞΗΓΗΣΙΣ) into the new method of analytical music notation of the Sunday koinonikon of the 18th century](https://www.scia.istoria-artei.ro/2010.php).

**Συμβολή στη μελέτη:** Πρωτογενής μουσικολογική τεκμηρίωση της θέσης ως βασικής μονάδας στα Κοινωνικά και της σχέσης παλαιάς γραφής–Νέας Μεθόδου. Παρουσιάζει αναδρομική σύγκριση 42 Κοινωνικών και 11 σημαντικών σχημάτων.

### Κωνσταντίνος Χ. Καραγκούνης (2003) — Η παράδοσις και εξήγησις του μέλους των Χερουβικών της βυζαντινής και μεταβυζαντινής μελοποιίας

**Δημοσίευση:** Διδακτορική διατριβή, Αθήνα. **Πηγή:** [Η παράδοσις και εξήγησις του μέλους των Χερουβικών της βυζαντινής και μεταβυζαντινής μελοποιίας](https://www.kxkaragounis.gr/αρθρα-δημοσιευσεις/).

**Συμβολή στη μελέτη:** Πηγή για τα Χερουβικά, τη σχέση παραδοσιακών θέσεων και ιστορικής γραφής και τη διαχρονική μεταβολή της μελοποιίας. Προσφέρει μουσικολογική τεκμηρίωση και θέσεις για επαλήθευση στις πρωτογενείς πηγές του corpus.


## Γ. Μη παραμετρικά μοντέλα και κοινή επαγωγή μονάδων

### Yee Whye Teh (2006) — A Hierarchical Bayesian Language Model Based on Pitman–Yor Processes

**Δημοσίευση:** Proceedings of COLING/ACL 2006, 985–992. **Πηγή:** [A Hierarchical Bayesian Language Model Based on Pitman–Yor Processes](https://aclanthology.org/P06-1124/).

**Συμβολή στη μελέτη:** Θεμελιώνει την ιεραρχική μη παραμετρική προτεραιότητα που σχετίζεται με τη στατιστική επανάληψη ακολουθιών και την εκμάθηση κατανομών με βαριά ουρά.

### Daichi Mochihashi, Takeshi Yamada και Naonori Ueda (2009) — Bayesian Unsupervised Word Segmentation with Nested Pitman-Yor Language Modeling

**Δημοσίευση:** Proceedings of ACL-IJCNLP 2009, 100–108. **Πηγή:** [Bayesian Unsupervised Word Segmentation with Nested Pitman-Yor Language Modeling](https://aclanthology.org/P09-1012/).

**Συμβολή στη μελέτη:** Πρωτογενής πρόταση του NPYLM για μη εποπτευόμενη τμηματοποίηση λέξεων από συνεχείς συμβολοσειρές με blocked Gibbs sampling. Προσφέρει τη μαθηματική βάση της μεταφοράς σε μελωδικές συμβολοσειρές.

### Sharon Goldwater, Thomas L. Griffiths και Mark Johnson (2009) — A Bayesian Framework for Word Segmentation: Exploring the Effects of Context

**Δημοσίευση:** Cognition, 112(1), 21–54. **Πηγή:** [A Bayesian Framework for Word Segmentation: Exploring the Effects of Context](https://doi.org/10.1016/j.cognition.2009.03.008).

**Συμβολή στη μελέτη:** Θεωρητική μελέτη του ρόλου της συμφραστικής πληροφορίας στην επαγωγή τμημάτων. Στην παρούσα μελέτη ενισχύει τον σχεδιασμό ελέγχων της συμβολικής αναπαράστασης και των συμφραζομένων.

### Kei Uchiumi, Hiroshi Tsukahara και Daichi Mochihashi (2015) — Inducing Word and Part-of-Speech with Pitman-Yor Hidden Semi-Markov Models

**Δημοσίευση:** Proceedings of ACL-IJCNLP 2015, 1774–1782. **Πηγή:** [Inducing Word and Part-of-Speech with Pitman-Yor Hidden Semi-Markov Models](https://aclanthology.org/P15-1171/).

**Συμβολή στη μελέτη:** Παρουσιάζει κοινή επαγωγή ορίων και λανθανουσών κατηγοριών μέσω PYHSMM. Παρέχει αρχιτεκτονικό προηγούμενο για υποψήφιο μουσικό PYHSMM που θα συνδέει πλήρεις θέσεις και οικογενειακές κατηγορίες.

### Ryo Fujii, Ryo Domoto και Daichi Mochihashi (2017) — Nonparametric Bayesian Semi-supervised Word Segmentation

**Δημοσίευση:** Transactions of the Association for Computational Linguistics, 5, 179–189. **Πηγή:** [Nonparametric Bayesian Semi-supervised Word Segmentation](https://aclanthology.org/Q17-1013/).

**Συμβολή στη μελέτη:** Συνδυάζει CRF και NPYLM σε ημιεποπτευόμενη μάθηση, αξιοποιώντας επισημειωμένα και μη επισημειωμένα δεδομένα. Χρήσιμο άμεσο προηγούμενο για πειράματα περιορισμένης εποπτείας σε οικογένειες θέσεων.


## Δ. Δομημένη πρόβλεψη, HMM και επιλογή δομής

### John Lafferty, Andrew McCallum και Fernando Pereira (2001) — Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data

**Δημοσίευση:** Proceedings of ICML 2001, 282–289. **Πηγή:** [Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data](https://people.cs.umass.edu/~mccallum/pubs.html).

**Συμβολή στη μελέτη:** Θεμελιώνει τις ακολουθιακές υπό συνθήκη κατανομές με παγκόσμια κανονικοποίηση, ως αναφορά για το εποπτευόμενο μοντέλο ορίων.

### Sunita Sarawagi και William W. Cohen (2004) — Semi-Markov Conditional Random Fields for Information Extraction

**Δημοσίευση:** Advances in Neural Information Processing Systems, 17. **Πηγή:** [Semi-Markov Conditional Random Fields for Information Extraction](https://proceedings.neurips.cc/paper_files/paper/2004/hash/eb06b9db06012a7a4179b8f3cb5384d3-Abstract.html).

**Συμβολή στη μελέτη:** Βασική μαθηματική αναφορά για προβλέψεις ετικετών σε ολόκληρα τμήματα με χαρακτηριστικά span. Σχετίζεται άμεσα με το F/semi-CRF και την αρχιτεκτονική Α της Μ1-X.

### Lingpeng Kong, Chris Dyer και Noah A. Smith (2016) — Segmental Recurrent Neural Networks

**Δημοσίευση:** ICLR 2016. **Πηγή:** [Segmental Recurrent Neural Networks](https://arxiv.org/abs/1511.06018).

**Συμβολή στη μελέτη:** Εξετάζει νευρωνική κοινή κατανομή ορίων και ετικετών τμημάτων. Συνιστά σχετικό αρχιτεκτονικό baseline για σύγκριση εκμάθησης πλήρους μονάδας.

### Andreas Stolcke και Stephen Omohundro (1992) — Hidden Markov Model Induction by Bayesian Model Merging

**Δημοσίευση:** Advances in Neural Information Processing Systems 5. **Πηγή:** [Hidden Markov Model Induction by Bayesian Model Merging](https://proceedings.neurips.cc/paper_files/paper/1992/hash/5c04925674920eb58467fb52ce4ef728-Abstract.html).

**Συμβολή στη μελέτη:** Θεμελιώνει τη συγχώνευση καταστάσεων HMM ως μέθοδο επαγωγής δομής από δεδομένα. Σχετίζεται με την υπολογιστική προσέγγιση που αξιοποίησε ο Μαυρομάτης.

### Andreas Stolcke και Stephen Omohundro (1994) — Inducing Probabilistic Grammars by Bayesian Model Merging

**Δημοσίευση:** International Colloquium on Grammatical Inference (ICGI), LNCS/LNAI 862. **Πηγή:** [Inducing Probabilistic Grammars by Bayesian Model Merging](https://arxiv.org/abs/cmp-lg/9409010).

**Συμβολή στη μελέτη:** Δίνει γενικότερο πλαίσιο για συγχώνευση δομών σε πιθανοτικά μοντέλα και επιλογή απλούστερων περιγραφών.

### Jorma Rissanen (1978) — Modeling by Shortest Data Description

**Δημοσίευση:** Automatica, 14(5), 465–471. **Πηγή:** [Modeling by Shortest Data Description](https://doi.org/10.1016/0005-1098(78)90005-5).

**Συμβολή στη μελέτη:** Κλασική θεμελίωση του Minimum Description Length. Αποτελεί πηγή για τη διάκριση ανάμεσα σε κατάλληλη επιλογή δομής και σε απλή περιγραφική συμπίεση.


## Ε. Αξιολόγηση και μουσικολογικά πληροφορημένη μηχανική μάθηση

### Gaël Richard, Vincent Lostanlen, Yi-Hsuan Yang και Meinard Müller (2024) — Model-Based Deep Learning for Music Information Research: Leveraging Diverse Knowledge Sources to Enhance Explainability, Controllability, and Resource Efficiency

**Δημοσίευση:** IEEE Signal Processing Magazine, 41(6), 51–59. **Πηγή:** [Model-Based Deep Learning for Music Information Research: Leveraging Diverse Knowledge Sources to Enhance Explainability, Controllability, and Resource Efficiency](https://doi.org/10.1109/MSP.2024.3415569).

**Συμβολή στη μελέτη:** Ευρύτερη θέση της μουσικολογικά ενημερωμένης μάθησης στο πεδίο MIR: συνδυασμός γνώσης και δεδομένων με ελεγχόμενη αξιολόγηση της συμβολής τους.

### Rotem Dror, Gili Baumer, Segev Shlomov και Roi Reichart (2018) — The Hitchhiker’s Guide to Testing Statistical Significance in Natural Language Processing

**Δημοσίευση:** Proceedings of ACL 2018. **Πηγή:** [The Hitchhiker’s Guide to Testing Statistical Significance in Natural Language Processing](https://aclanthology.org/P18-1128/).

**Συμβολή στη μελέτη:** Πρωτόκολλο σχεδιασμού στατιστικών συγκρίσεων για μοντέλα ακολουθιών. Υποστηρίζει ζευγαρωτές συγκρίσεις, διαχωρισμό πολλαπλών υποθέσεων και σαφή αναφορά αβεβαιότητας.

### Bradley Efron και Robert J. Tibshirani (1993) — An Introduction to the Bootstrap

**Δημοσίευση:** Chapman & Hall. **Πηγή:** [An Introduction to the Bootstrap](https://catalogue.library.cern/literature/fc0ns-p8v38).

**Συμβολή στη μελέτη:** Θεμελιώνει τις μεθόδους επαναδειγματοληψίας για διαστήματα εμπιστοσύνης. Η παρούσα αξιολόγηση χρησιμοποιεί ανεξάρτητα έργα ή μελωδικές ομάδες ως μονάδα επαναδειγματοληψίας.

### Jouni Paulus, Meinard Müller και Anssi Klapuri (2010) — State of the Art Report: Audio-Based Music Structure Analysis

**Δημοσίευση:** Proceedings of ISMIR 2010, 625–636. **Πηγή:** [State of the Art Report: Audio-Based Music Structure Analysis](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C4/C4S1_MusicStructureGeneral.html).

**Συμβολή στη μελέτη:** Ευρύτερο πλαίσιο αξιολόγησης μουσικής δομής και διαφορετικών κλιμάκων τμηματοποίησης. Αφορά ηχητική ανάλυση και χρησιμοποιείται μόνο ως θεματικό σημείο αναφοράς, με σαφή διάκριση από την παρούσα συμβολική εργασία.

## Σημειώσεις χρήσης βιβλιογραφίας

1. Οι πηγές Helsen, Gheorghiță και Καραγκούνη συνδέονται με συγκεκριμένες μουσικολογικές αναλύσεις, διαφορετικό υλικό και διαφορετική κλίμακα κατάτμησης. Η σύγκριση των παραδόσεων θα γίνει με ανεξάρτητες επισημειώσεις ανά παράδοση.
2. Οι εργασίες Mochihashi, Uchiumi και Fujii αφορούν τμηματοποίηση γλωσσικών δεδομένων. Η εφαρμογή σε μουσική αποτελεί μεταφορά και προσαρμογή προς πειραματική αξιολόγηση.
3. Οι εργασίες Μαυρομάτη αξιοποιούνται ως υπολογιστικά προηγούμενα για την ελληνική ψαλτική. Τα αποτελέσματά τους θα εξεταστούν στις ακριβείς πηγές πριν από αριθμητική σύγκριση με το νέο corpus.
4. Οι συνθήκες F, LASM και οι αριθμητικές μετρήσεις των Stages 1–3 προέρχονται από **τα πειραματικά αρχεία αυτής της έρευνας**. Οι βιβλιογραφικές εργασίες τεκμηριώνουν τη μεθοδολογική συγγένεια και τις βασικές μαθηματικές μεθόδους· οι μετρημένες επιδόσεις παραμένουν πρωτογενή αποτελέσματα της παρούσας μελέτης.
5. Η αναδιανομή δεδομένων και πλήρων PDF πραγματοποιείται σύμφωνα με τις αντίστοιχες άδειες· στην παρούσα δημόσια τεκμηρίωση παρατίθενται βιβλιογραφικοί σύνδεσμοι.

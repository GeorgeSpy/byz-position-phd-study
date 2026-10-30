# Σχέδιο υλοποίησης και εκτελεσμένοι έλεγχοι

## 1. Τι παραδίδεται και τι έχει πράγματι εκτελεστεί

Η τεχνική υποδομή περιλαμβάνει μαθηματική προδιαγραφή, μικρές υλοποιήσεις αναφοράς, μηχανικά αναγνώσιμα αποτελέσματα, σχήμα δεδομένων, ρυθμίσεις πρωτοκόλλου και επαναλήψιμο πρόγραμμα ελέγχων. Η εκτέλεση αφορά **συνθετικές κατανομές και μικρούς εξαντλητικούς χώρους**. Δεν εκπαιδεύτηκε μουσικός encoder, δεν φορτώθηκε πραγματικό B1/B2/EISE checkpoint και δεν κατασκευάστηκε νέο corpus από χειρόγραφα.

| Έλεγχος | Αρχείο | Αποτέλεσμα |
|---|---|---|
| Ημι-Μαρκοβιανές αναδρομές | `original_oracles/toy_semimarkov_checks.py` | 291 έλεγχοι PASS, μέγιστη αριθμητική απόκλιση περίπου $3,6\cdot10^{-15}$. |
| Πρωτογενής έλεγχος profile-HMM | `original_oracles/profile_hmm_regression_oracle.py` | 5 αρχικές ομάδες PASS. Το αντιπαράδειγμα ολικής κανονικοποίησης αποκαλύπτει το ελλιπές END. |
| Έλεγχος στοιχίσεων και λογικής μάζας | `original_oracles/alignment_product_oracle.py` | 16 ομάδες PASS με τις δικές τους υποθέσεις, συμπεριλαμβάνοντας αναμενόμενη αποτυχία naive prefix reuse. |
| Νέο ανεξάρτητο counterexample | `original_oracles/oracle_Zf_context_counterexample.py` | Αναπαραγωγή και των τριών αποτυχιών του παλιού Z. |
| Νέα profile/outer/generative suite | `profile_semantics_oracle.py` | 221 έλεγχοι PASS· μέγιστη απόκλιση $1,56\cdot10^{-10}$, που περιλαμβάνει finite-difference gradients. |
| Διορθωμένο context product DP | `ecsi_kappa_context_oracle.py` | 308 έλεγχοι PASS· corrected relative Z errors κάτω από $4\cdot10^{-16}$. |
| Μικρή πραγματική βελτιστοποίηση κ | `bidirectional_learning_oracle.py` | 43 έλεγχοι PASS· EM monotonicity, direct-objective συμφωνία, selected consistency και DP. |
| Σχεδιασμός ισχύος / transfer | `power_and_transfer_simulation.py` | 50 σενάρια ισχύος και 9 συνθετικά transfer σενάρια· assertions PASS. |

Οι αριθμοί είναι πλήθη assertions ή ομάδων, όπως δηλώνονται στα αντίστοιχα JSON. Δεν αποτελούν αριθμό ανεξάρτητων μουσικών πειραμάτων. Το συνολικό μέγιστο σφάλμα στο context JSON είναι περίπου $8,44\cdot10^{-7}$ λόγω ελέγχου αριθμητικού optimizer μιας MLE, όχι λόγω απόκλισης του DP. Τα per-test records επιτρέπουν τον χωριστό έλεγχο.

## 2. Αρχεία και αναπαραγωγή

Απαιτείται Python 3 με NumPy και SciPy. Οι πραγματικές εκδόσεις περιβάλλοντος καταγράφονται στο `validation_summary.json`. Από τον φάκελο του πακέτου:

```bash
python3 run_all_checks.py
python3 -m compileall -q .
```

Ο πρώτος runner εκτελεί τα οκτώ scripts και αποθηκεύει exit codes, χρόνους και logs. Συμπληρωματικοί έλεγχοι σύνταξης Python/JSON και συνδέσμων τεκμηρίωσης εκτελούνται χωριστά, όπου υπάρχουν τα αντίστοιχα εργαλεία. Οι δοκιμές παλαιότερων εξισώσεων διατηρούνται ως έλεγχοι παλινδρόμησης και εκτελούνται χωριστά από τη διορθωμένη υλοποίηση. Η αναπαραγωγή ενημερώνει τα τοπικά result JSON· τα benchmarks μπορεί να διαφέρουν σε χρόνο/μνήμη ανά μηχάνημα.

Οι επιστημονικές δημοσιεύσεις και οι ιστορικές εικόνες δεν αναδιανέμονται ως μέρος του κώδικα. Το [μητρώο βιβλιογραφικών και πηγολογικών περιορισμών](SOURCE_ACCESS_AND_UNRESOLVED_EVIDENCE.md) διαχωρίζει τα τεκμήρια από τα συνθετικά παραδείγματα. Οι αριθμητικές δοκιμές περιλαμβάνουν τις δικές τους αναγκαίες ελεγχόμενες εισόδους.

## 3. Προτεινόμενα modules παραγωγής

| Module / interface | Είσοδοι | Έξοδοι και contract |
|---|---|---|
| `data/source_registry` | Source cards, δικαιώματα, image/token hashes. | Versioned records· αποτυχία όταν λείπει απαιτούμενη άδεια/προέλευση. |
| `data/splits` | Work/locus/copy/parallel edges. | Connected components και train/dev/test· μηδενική διατομή. |
| `music/role_inventory` | Τοπικό εγχειρίδιο, expert labels, partial crosswalk. | Role IDs ανά παράδοση· αβέβαιη αντιστοίχιση χωριστή από βέβαιη. |
| `profile/normalized_profile` | Train-only templates, priors, emissions/transitions. | Κανονισμένες γραμμές, END και termination certificate. |
| `logic/card_compiler` | S, owners, applicability, missing/deletion policy, dependency declarations. | Residual automaton, width, context statistics και δυνατότητα prefix reuse. |
| `inference/observed_product` | X, f, κ, q, compiled card. | log A, log B, m και posterior marginals· log-space. |
| `inference/normalizer_product` | f,C,n, finite alphabet και diagnostic state. | log a, log z, log Z· απαγορεύεται fixed-X diagnostic shortcut. |
| `learning/sampling_objective` | Dataset sampling metadata και labels. | Joint, conditional-Y ή selected objective, με σωστό gradient. |
| `models/a0` | R★/R_Z, adapter, encoder checkpoint. | h, z_id, z_real και base span scores· checkpoint lineage. |
| `inference/segment_crf` | Span scores, skip scores, annotation constraints. | log partition, marginals και Viterbi· empty output επιτρεπτό. |
| `evaluation/comparators` | Κοινό posterior/q/S και resource budget. | Add, Vit, Pool, Pool2, MC, A1+γ, AC· κοινό calibration interface. |
| `evaluation/probes_statistics` | Frozen features, group IDs, blind labels. | Q_real, inverse, paired intervals, gates και complete coverage ledger. |

Τα paths είναι προτεινόμενη λογική οργάνωση νέων modules· δεν δηλώνεται ότι υπάρχουν ήδη στο GitHub ή ότι γράφτηκε production trainer μέσα στο παρόν ZIP.

## 4. Ακριβής σειρά υπολογισμού

```text
compile_card(card):
    validate applicability, owners, deletion/missing policy
    derive residual logical states
    list sufficient emitted-history and path statistics
    certify prefix_reuse only when internal factors ignore final end
    return automaton, state_contract, measured_width

observed_scores(X, f, parameters):
    run profile × logical-state DP in log space
    sum all terminal states including END -> log_A
    sum accepted terminal states including END -> log_B
    return log_A, log_B, exp(log_B - log_A)

generative_normalizer(f, C, length, parameters):
    reject undeclared full-sequence diagnostic dependencies
    initialize profile × logic × emitted_history × statistics
    for each topologically ordered state:
        for each allowed profile edge:
            if emitting: sum over every vocabulary symbol
            update emitted_history also for INSERT
            update logical state using the declared diagnostics
            accumulate with logsumexp
    apply END and terminal diagnostics
    return log_a, log_z, log_z - log_a

train_kappa(batch):
    read the recorded sampling regime
    choose the corresponding objective from mathematical spec §7
    keep q fixed for the first semantic learning comparison
    compute exact positive and, when required, negative expectations
    update parameters and verify the correct objective increases

decode(X):
    calculate candidate-family span scores
    apply beta weights after internal marginalization
    run zero-order skip semi-CRF forward/backward or Viterbi
    use separately calibrated U and abstention decisions
```

Οι β πολλαπλασιάζουν τους ήδη υπολογισμένους log A/log m. Η μεταφορά τους μέσα στο άθροισμα διαδρομών αλλάζει το μοντέλο. Ο κενός semantic support με $z=0$ απορρίπτεται ως μη ορίσιμη γεννητική δέσμευση. Η χρήση epsilon clipping δηλώνεται ως αλλαγή μοντέλου, αν αλλάζει πιθανότητες, και δεν καλύπτει λανθασμένη προδιαγραφή.

## 5. Invariants και tests πριν από μουσική εφαρμογή

| Invariant | Έλεγχος αναφοράς | Επιπλέον production acceptance |
|---|---|---|
| Κάθε transition/emission row αθροίζει στο 1. | Τυχαία profiles, END, μικρή απαρίθμηση, μήκη έως 100. | Float32/64, batch shapes, μηδενικές πιθανότητες και μεγάλα μήκη. |
| Κάθε διαδρομή/ανάθεση μετρά μία φορά. | Brute force = DP· 255 specifications. | Compiler property tests, disjunction overlaps, αδύνατο/ταυτολογικό S. |
| $B\le A$, $z\le a$, $0\le m,Z\le1$. | Ακριβής απαρίθμηση observed/global cases. | Όλα τα πραγματικά compiled cards και κάθε training checkpoint. |
| INSERT ενημερώνει emitted context. | Τρεις seed regressions του ανεξάρτητου υπομνήματος. | Παράθυρα 2/3, OOV, deleted landmark και μακρινά relations. |
| Prefix reuse μόνο με invariant internal factors. | Αντιπαράδειγμα end-dependent diagnostic και διορθωμένες separate passes. | Static dependency check και randomized equality με per-span implementation. |
| Selected density αθροίζει στο 1. | Όλα τα strings μικρού fixed length. | Κοινή length conditioning, selection mechanism και gradient checks. |
| Σωστός selected gradient. | Analytic expectation έναντι finite differences. | Autograd έναντι ανεξάρτητου oracle σε κάθε parameter family. |
| Skip ↔ O1 bijection. | Exhaustive tilings και background multiplicity counterexample. | U/O/unresolved partial labels, long all-background sequence, empty output. |
| Partial annotation loss. | Constrained partition έναντι enumeration. | Alternative boundaries με joint constraints· fully unknown loss=0. |
| Gap memory συμβατή με factorization. | Zero-order, gap flag, full-span insufficiency examples. | Η πρώτη έκδοση παραμένει zero-order· κάθε πρόσθετη μετάβαση απαιτεί νέο contract. |
| Generative/CRF posterior υπό σωστές προϋποθέσεις. | Joint normalization, β=1, survival και Markov boundary cases. | Ίδιο background measure, horizon και length prior σε integration tests. |
| Καμία κυκλική είσοδος. | Συνθετικός component leakage detector. | Πραγματικό manifest audit, annotation-origin tests και feature allowlist. |
| Q_real και ιστορικό H χωριστά. | Μη ενέσιμη operation summary, ambiguity toy cases. | Frozen probes/actual source-linked H και empirical NI gate. |

## 6. Εκτελεσμένη μάθηση και όρια του αποτελέσματος

Το `bidirectional_learning_oracle.py` εκτιμά μία δυαδική emission row σε profile δύο στηλών, αλφάβητο δύο συμβόλων και γνωστό μήκος 3. Τα diagnostics και η topology είναι σταθερά. Οι fractional counts προέρχονται από τον ακριβή πληθυσμό του selected model με αληθή θ=0,72· δεν προσποιούνται ανεξάρτητο πραγματικό δείγμα.

| Objective | Εκτίμηση θ | Ερμηνεία |
|---|---:|---|
| Plain EM στο περιεχόμενο | 0,9685563 | Το επιλεγμένο δείγμα δεν είναι αντιπροσωπευτικό του αρχικού unconstrained profile. |
| Positive joint EM | 0,9999999, στο δηλωμένο αριθμητικό όριο | Μεγιστοποιεί διαφορετική objective. |
| Σωστή selected likelihood | 0,71999999997 | Ανακτά την παράμετρο του υποτιθέμενου μοντέλου παραγωγής. |

Οι EM objectives αυξάνουν σε όλες τις εκτελεσμένες επαναλήψεις και συμφωνούν με direct one-dimensional optimization της **ίδιας** objective. Το global z από το corrected DP συμφωνεί με την ανεξάρτητη απαρίθμηση με απόκλιση $2,78\cdot10^{-17}$. Οι AC/Pool/Vit probabilities υπολογίζονται με το ίδιο αρχικό posterior. Η joint-block δοκιμή αναπαράγει πιθανότητα ισότητας 1 έναντι 0,5 για ίδια περιθώρια.

Δεν υλοποιήθηκε neural A1+γ ή πλήρης εκπαίδευση όλων των parameter rows. Το παραπάνω είναι ουσιαστικό consistency/selection test και ανεξάρτητος μαθησιακός έλεγχος· οι αντίστοιχες μουσικές συγκρίσεις απαιτούν τα δεδομένα της G0.

## 7. Μετρημένο κόστος και MVP

Σε μία εκτέλεση Python, observed product για $(J,\vert V\vert ,n,W)=(4,8,32,2)$ χρειάστηκε περίπου 0,086 s και για $(8,16,64,2)$ περίπου 0,398 s. Η άθροιση εκπομπών με previous-symbol state για $(4,8,16,2)$ χρειάστηκε περίπου 1,594 s. Η `tracemalloc` μέτρηση ήταν περίπου 139 kB, 542 kB και 302 kB αντίστοιχα· μετρά Python allocations, όχι πλήρες RSS ή μελλοντική GPU μνήμη. Τα ακριβή run-specific timings παραμένουν στο `ecsi_kappa_context_results.json` και μπορεί να αλλάξουν με επανεκτέλεση.

Αυτές οι διαστάσεις είναι **συνθετικά stress cases**. Δεν έχουν μετρηθεί πραγματικά J,L,W στη νέα απογραφή. Ο production πιλότος θα καταγράψει την κατανομή τους, τα ανοιχτά logical dependencies, το context-state πλήθος και το κόστος όλων των υποψηφίων spans. Οι ασυμπτωτικές εκφράσεις του [02](02_SELECTED_ARCHITECTURE_MATHEMATICAL_SPEC_GR.md) είναι το ακριβές συμβόλαιο, όχι υπόσχεση συγκεκριμένου throughput.

Το MVP ολοκληρώνεται όταν: (α) μία πραγματική οικογένεια και hard negatives έχουν ελεγμένα records, (β) normalized profile/semantic card εκτελούνται με ίδιο αποτέλεσμα σε oracle και compiled DP, (γ) Pool/Vit/AC χρησιμοποιούν τα ίδια δεδομένα, (δ) ένας full-work zero-order decoder χειρίζεται partial labels/U/skip, (ε) τα reports παράγονται με source groups και τις τρεις Q_real δοκιμές. Η μετάβαση σε περισσότερες οικογένειες ακολουθεί την G0–G1. Το frozen symbolic P1 μπορεί να προηγηθεί του GPU σκέλους χωρίς να αλλάζει η επιλεγμένη τελική αρχιτεκτονική.

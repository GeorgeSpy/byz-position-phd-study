# Α2 — Πρώτοι συνθετικοί έλεγχοι εφικτότητας (3 Νοεμβρίου 2026)

[Συνθετικοί έλεγχοι Α2](../../../README.md) · [Ερευνητικός σχεδιασμός Α2](../../../../../a2-knowledge-design.md) · [Παράρτημα K](../../../../../../appendices/k.md)

Ο φάκελος φυλάσσει αυτούσια τα 18 αρχεία της πρώτης δέσμης συνθετικών ελέγχων Α2, όπως υποβλήθηκαν στις 3 Νοεμβρίου 2026. Η δέσμη κάλυπτε τρία υποσυστήματα: γεννήτορα διαταραχών, ομαδοποιημένη στατιστική διαδικασία και εκπαίδευση κεφαλών. Οι νεότεροι έλεγχοι του φακέλου [`support`](../../../README.md) την αντικαθιστούν και δεν χρησιμοποιούν τα αποτελέσματά της.

| Αρχείο αυτής της δέσμης | Νεότερο αντίστοιχο |
|---|---|
| `synthetic_concepts.py`, `synthetic_scores.py` | `a2_ap.py` |
| `feasibility_generator.py` | `generator_feasibility.py` |
| `feasibility_stats.py` | `oc_jackknife_t.py`, `oc_bootstrap_t.py` |
| `feasibility_heads.py` | `heads_allocation.py` |
| `test_feasibility.py` | `test_ap.py`, `test_generator.py` |

Τα αρχεία είναι πανομοιότυπα με την αρχική υποβολή. Τα αποτυπώματα SHA-256 του `results/run_manifest.json` επαληθεύονται. Οι εντολές του manifest αναφέρουν την αρχική θέση `docs/research/a2/support/`. Από τον παρόντα φάκελο οι δοκιμές εκτελούνται με:

```bash
python -m unittest -v test_feasibility
```

Οι εκτελέσεις στατιστικής διαδικασίας είχαν 300 δείγματα ανά σενάριο. Με αυτό το μέγεθος τα διαστήματα Monte Carlo άφηναν ανοικτή την επιβεβαιωτική πύλη βαθμονόμησης· στο αραιό σενάριο εκδόθηκαν έγκυρες αναλύσεις σε 152/300 δείγματα. Τα τρέχοντα αποτελέσματα βρίσκονται στο [`results/summary.md`](../../summary.md).

---

**English.** First A2 synthetic feasibility checks (3 November 2026), kept byte-identical for the record; the SHA-256 fingerprints in `results/run_manifest.json` verify. They are superseded by the current checks in [`support`](../../../README.md) (mapping in the table above) and are not used in the current results.

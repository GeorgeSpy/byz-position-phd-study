"""Summarize the A2 design-stage checks into results/summary.md (Markdown tables)."""
import json
from pathlib import Path

import numpy as np

RES = Path(__file__).resolve().parent / 'results'


def load(name):
    p = RES / name
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip().startswith('{')]


def f(x, d=3):
    if x is None:
        return '—'
    if isinstance(x, (list, tuple)):
        return ' / '.join(f(v, d) for v in x)
    if isinstance(x, float) and np.isnan(x):
        return '—'
    return f'{x:.{d}f}'


def ci(v):
    return '—' if v is None or v[0] is None else f'[{v[0]:.3f}, {v[1]:.3f}]'


def label(c):
    return c['scenario'] + (' · ισοβαθμίες' if c['ties'] else '') + (' · F/D συμμετρικά' if c['symmetrize_fd'] else '')


out = ['# Α2 — Σύνοψη συνθετικών ελέγχων', '',
       'Παράγεται από το `summarize.py`. Οι τιμές αναφοράς και τα δείγματα Monte Carlo έχουν ανεξάρτητες ροές τυχαιότητας.', '']
oc = load('oc_jackknife_t.jsonl')
plain = [r for r in oc if not r.get('allocation')]
alloc = [r for r in oc if r.get('allocation')]
out += ['## 1. Κύρια υποψήφια διαδικασία: jackknife-t(G−1), Holm 0,025', '',
        '| Σενάριο | G | R | α | Επαναλήψεις αναφοράς | Σχεδιασμένα / ορισμένα / εκδοθέντα | FWER (όλα τα σχεδιασμένα) [95% MC] | Ισχύς H1 / H2 | Κάλυψη 95% (Δ_know / Δ_logic) | Αληθής τιμή |',
        '|---|---|---|---|---|---|---|---|---|---|']
for r in plain:
    c = r['cfg']
    fw = f"{r['fwer_unconditional']:.4f} {ci(r['fwer_unconditional_cp95'])}" if any(r['null_exact']) else '—'
    out.append(f"| {label(c)} | {c['G']} | {r['R']} | {c['alpha']:g} | {r['reference_reps']} | {r['M_planned']} / {r['M_defined']} / {r['M_issued']} | {fw} | "
               f"{f(r['power_unconditional'])} | {f(r['coverage95_two_sided'])} | {f(r['truth'], 4)} |")
out += ['', 'Οι μηδενικές τιμές είναι ακριβείς κατά κατασκευή: H1 με ίδιους νόμους V/P, H2 με ανταλλαγή F/D ανά ομάδα. '
        'Οι μη μηδενικές τιμές είναι αναφορές μεγάλου G (400 ομάδες). Το FWER και η ισχύς μετρώνται σε όλα τα σχεδιασμένα δείγματα· τα μη εκδοθέντα μετρώνται ως μη απόρριψη.', '']
if alloc:
    out += ['## 2. Κατανομή ομάδων στο H με κάλυψη οικογενειών', '',
            'Κάθε δείγμα παράγει δεξαμενή 2,5·G ομάδων και επιλέγει τις G ομάδες του H με τον προκαθορισμένο κανόνα: κάθε οικογένεια σε τουλάχιστον m_H ομάδες (`a2_ap.allocate_h`). '
            'Η κάλυψη αναφέρεται μόνο για ακριβείς μηδενικές· για τα υπόλοιπα δίνονται μέση εκτίμηση και τυπική απόκλιση.', '',
            '| Σενάριο | G | m_H | Σχεδιασμένα / κατανεμημένα / ορισμένα / εκδοθέντα | FWER [95% MC] | Ισχύς H1 / H2 | Κάλυψη 95% (μηδενικές) | Μέση εκτίμηση ± SD | Ανάπτυξη με οικογένεια σε <2 ομάδες |',
            '|---|---|---|---|---|---|---|---|---|']
    for r in alloc:
        c = r['cfg']
        fw = f"{r['fwer_unconditional']:.4f} {ci(r['fwer_unconditional_cp95'])}" if any(r['null_exact']) else '—'
        me = ' / '.join(f'{m:.4f} ± {s:.4f}' for m, s in zip(r['mean_estimate'], r['sd_estimate'])) if r['mean_estimate'] else '—'
        out.append(f"| {label(c)} | {c['G']} | {r['allocation']['m_H']} | {r['M_planned']} / {r['M_allocated']} / {r['M_defined']} / {r['M_issued']} | {fw} | "
                   f"{f(r['power_unconditional'])} | {f(r['coverage95_two_sided'])} | {me} | {f(r['dev_some_family_below_2_groups_rate'])} |")
    out.append('')

# earlier batches (shared random stream) for the record
eb = []
for name in ('earlier_batches/batch1_shared_stream_refreps5.jsonl', 'earlier_batches/batch2_shared_stream_refreps20.jsonl'):
    for r in load(name):
        if r['R'] == 5:
            eb.append((name.split('/')[1].split('_')[0], r))
if eb:
    out += ['## 3. Προηγούμενες παρτίδες με κοινή ροή τυχαιότητας (R=5, G=12, σπόρος 108)', '',
            'Στις δύο πρώτες εκτελέσεις η ίδια γεννήτρια έδινε πρώτα την αναφορά και μετά τα δείγματα· η αλλαγή των επαναλήψεων αναφοράς άλλαζε και τα δείγματα. '
            'Είναι επομένως διαφορετικές παρτίδες Monte Carlo και όχι διόρθωση μόνο της αναφοράς.', '',
            '| Παρτίδα | Επαναλήψεις αναφοράς | Δείγματα | FWER [95% MC] | Κάλυψη 95% (Δ_know / Δ_logic) | Αναφορά Δ_know |',
            '|---|---|---|---|---|---|']
    for b, r in eb:
        out.append(f"| {b} | {r.get('reference_reps')} | {r['M_planned']} | {r['fwer_unconditional']:.4f} {ci(r['fwer_unconditional_cp95'])} | {f(r['coverage95_two_sided'])} | {r['truth'][0]:.4f} |")
    same = [r for r in plain if r['R'] == 5]
    if len(same) >= 2:
        out += ['', 'Στην τρέχουσα εκτέλεση, με ανεξάρτητες ροές, τα ίδια 1000 δείγματα αξιολογήθηκαν με δύο τιμές αναφοράς:', '',
                '| Επαναλήψεις αναφοράς | Αναφορά Δ_know | Κάλυψη 95% Δ_know | FWER |', '|---|---|---|---|']
        for r in same:
            out.append(f"| {r['reference_reps']} | {r['truth'][0]:.4f} | {r['coverage95_two_sided'][0]:.3f} | {r['fwer_unconditional']:.4f} |")
    out.append('')

boot = load('oc_bootstrap_t.jsonl')
if boot:
    out += ['## 4. Ευαισθησία: bootstrap-t ανά δείγμα (B=199, αυστηρός κανόνας)', '',
            '| Σενάριο | G | Σχεδιασμένα / ορισμένα / εκδοθέντα | FWER (όλα) [95% MC] | FWER με απόρριψη μη ορισμένων αναδειγματοληψιών (διαγνωστικό) | Ισχύς H1 / H2 | Κάλυψη 95% |',
            '|---|---|---|---|---|---|---|']
    for r in boot:
        c = r['cfg']
        out.append(f"| {c['scenario']} | {c['G']} | {r['M_planned']} / {r['M_defined']} / {r['M_issued_strict']} | "
                   f"{r['fwer_strict_unconditional']:.4f} {ci(r['fwer_strict_unconditional_cp95'])} | {f(r['fwer_lenient_conditional_diagnostic'], 4)} | "
                   f"{f(r['power_strict_unconditional'])} | {f(r['coverage95_strict'])} |")
    out.append('')

gen_all = [(0, load('generator_feasibility.jsonl')), (1, load('generator_feasibility_move.jsonl'))]
if any(g for _, g in gen_all):
    out += ['## 5. Γεννήτορας διαταραχών', '',
            '| Προτίμηση μετακίνησης | K | Πλούσια τράπεζα | Τράπεζες με 10 αποδεκτές P | Τερματισμός | Διάμεσες προτάσεις (επιτυχείς) | Συχνότερες απορρίψεις | Μόνο αλλαγή στο E | Συμφωνία v V–P | Επικάλυψη ζευγών P | d_F διάμεσο | Μέγ. πρωτεύον / δυϊκό υπόλοιπο / κενό | Ελάχ. δυϊκό φράγμα |',
            '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for mp, gen in gen_all:
        cells = {}
        for r in gen:
            cells.setdefault((r['K'], r['rich']), []).append(r)
        for (K, rich), rs in sorted(cells.items()):
            ok = [r for r in rs if r['accepted'] >= 10]
            term = {}
            for r in rs:
                term[r.get('termination')] = term.get(r.get('termination'), 0) + 1
            rej = {}
            for r in rs:
                for k, v in r['reasons'].items():
                    rej[k] = rej.get(k, 0) + v
            top = ', '.join(f'{k} {v}' for k, v in sorted(rej.items(), key=lambda x: -x[1])[:3] if v)
            med = lambda key: (np.median([r[key] for r in ok if r[key] is not None]) if ok else None)
            mx = lambda key: (max((r.get(key) if r.get(key) is not None else np.nan) for r in ok) if ok else np.nan)
            out.append(f"| {mp} | {K} | {'ναι' if rich else 'όχι'} | {len(ok)}/{len(rs)} | {', '.join(f'{k} {v}' for k, v in term.items())} | {f(med('proposals'), 0)} | {top} | "
                       f"{f(med('only_E_change_mean'))} | {f(med('v_agree_mean'))} | {f(med('pair_overlap'))} | {f(med('dF_median'))} | "
                       f"{mx('lp_max_primal_residual'):.1e} / {mx('lp_max_dual_residual'):.1e} / {mx('lp_max_duality_gap'):.1e} | {f(min([r.get('lp_min_dual_bound', np.nan) for r in ok]) if ok else None)} |")
    allg = [r for _, g in gen_all for r in g]
    out += ['', 'Όλες οι V έχουν μάρτυρα φ=1 και ενεργοποίηση v: '
            + str(all(r['V_witness_all'] and r['V_active_all'] for r in allg)) + '.', '']

hs_all = [(100, load('heads_C100.jsonl')), (0.05, load('heads_C005.jsonl'))]
if any(h for _, h in hs_all):
    out += ['## 6. Πού εκπαιδεύονται οι κεφαλές (w, λ)', '',
            'A_train: κεφαλές στις ομάδες της βάσης (προηγούμενη αναθεώρηση). B_dev: κεφαλές στο εσωτερικό σύνολο ανάπτυξης (παρούσα αναθεώρηση). '
            'C_cross: ευαισθησία με ομαδοποιημένη διασταυρούμενη εκτίμηση· στην πρόβλεψη συνδυάζει πέντε μοντέλα.', '',
            '| Βάση | Κατανομή | λ̂ διάμεσος (10–90%) | SD του λ̂ | λ̂<0,1 | λ̂=2 | Δ_logic στο H (μέσος ± SE) | Μη ορισμένα | Σύγκλιση βάσεων |',
            '|---|---|---|---|---|---|---|---|---|']
    for C, hs in hs_all:
        for a in ('A_train', 'B_dev', 'C_cross'):
            lam = np.array([h[a]['lam'] for h in hs])
            dl = np.array([h[a]['d_logic'] for h in hs], float)
            und = int(np.isnan(dl).sum())
            dl = dl[~np.isnan(dl)]
            conv = np.mean([h.get('base_models_converged', True) for h in hs])
            out.append(f"| {'υπερπροσαρμοσμένη (C=100)' if C == 100 else 'κανονικοποιημένη (C=0,05)'} | {a} | {np.median(lam):.2f} ({np.quantile(lam, .1):.2f}–{np.quantile(lam, .9):.2f}) | "
                       f"{lam.std(ddof=1):.2f} | {(lam < .1).mean():.2f} | {(lam >= 2 - 1e-3).mean():.2f} | {dl.mean():.4f} ± {dl.std(ddof=1) / np.sqrt(len(dl)):.4f} | {und}/{len(hs)} | {conv:.2f} |")
    out.append('')
# reconstruction of every decision from the stored estimates and standard errors
from scipy.stats import t as _t
def _holm(p, alpha=.025):
    rej = np.zeros(2, bool); i = int(np.argmin(p))
    if p[i] <= alpha / 2:
        rej[i] = True
        if p[1 - i] <= alpha:
            rej[1 - i] = True
    return rej
jk = load('oc_jackknife_t.jsonl')
if jk:
    ok = 0; near = 0; nrep = 0
    for r in jk:
        a = np.array(r['per_rep_index_estimate_se'] or np.zeros((0, 5)), float)
        G = r['cfg']['G']
        rej = np.zeros((r['M_planned'], 2), bool)
        for row in a:
            pv = 1 - _t.cdf(row[1:3] / row[3:5], G - 1)
            rej[int(row[0])] = _holm(pv)
            near += int((np.abs(pv - .025) < 1e-5).any() or (np.abs(pv - .0125) < 1e-5).any())
        nrep += len(a)
        ok += int(np.array_equal(rej.sum(0), np.array(r['rejections'])))
    out += ['## 7. Ανακατασκευή των αποφάσεων', '',
            f'Από τις αποθηκευμένες εκτιμήσεις και τα τυπικά σφάλματα, με πλήρη αριθμητική ακρίβεια, ξαναϋπολογίζονται τα $p$ και εφαρμόζεται ξανά η διόρθωση Holm για {nrep} εκδοθέντα δείγματα. '
            f'Οι απορρίψεις ταυτίζονται με τις καταγεγραμμένες σε {ok} από τα {len(jk)} σενάρια. '
            f'Σε {near} δείγματα κάποιο $p$ απέχει λιγότερο από $10^{{-5}}$ από ένα όριο του Holm· γι’ αυτό οι τιμές δεν στρογγυλοποιούνται.', '']
for name in ('test_ap.txt', 'test_generator.txt'):
    p = RES / name
    if p.exists():
        out.append(f'- `{name}`: {p.read_text().strip()}')
print('\n'.join(out))

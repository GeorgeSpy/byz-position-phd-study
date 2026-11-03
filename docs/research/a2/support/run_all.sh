#!/usr/bin/env bash
# Full reproduction of the A2 design-stage checks (about 35–40 min on one core).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results
python3 test_ap.py | tee results/test_ap.txt
python3 test_generator.py | tee results/test_generator.txt
./run_oc.sh all
python3 generator_feasibility.py --banks 4 --cap-sec 20 > results/generator_feasibility.jsonl
python3 generator_feasibility.py --banks 4 --cap-sec 20 --move-pref 1 > results/generator_feasibility_move.jsonl
python3 heads_allocation.py --C 100  --n 60 > results/heads_C100.jsonl
python3 heads_allocation.py --C 0.05 --n 60 > results/heads_C005.jsonl
rm -f results/oc_bootstrap_t.jsonl
python3 oc_bootstrap_t.py --scenario null    --G 12 --M 150 --B 199 --seed 201 --symmetrize-fd >> results/oc_bootstrap_t.jsonl
python3 oc_bootstrap_t.py --scenario partial --G 12 --M 150 --B 199 --seed 202 --symmetrize-fd >> results/oc_bootstrap_t.jsonl
python3 summarize.py > results/summary.md

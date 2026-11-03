#!/usr/bin/env bash
# Operating characteristics of the primary candidate procedure (jackknife-t(G-1), Holm 0.025).
# Reference values and Monte Carlo datasets use independent random streams (a2_ap.streams).
# Every line stores its seed, configuration and software versions.
# Usage: ./run_oc.sh [a|b|all]  (a and b can run in parallel; all = a then b)
set -euo pipefail
cd "$(dirname "$0")"
part=${1:-all}
run() { out=$1; shift; python3 oc_jackknife_t.py "$@" >> "$out"; }
part_a() {
  local o=results/oc_jackknife_t_a.jsonl; rm -f "$o"
  run $o --scenario null       --G 12 --M 2000 --seed 101 --symmetrize-fd
  run $o --scenario partial    --G 12 --M 2000 --seed 102 --symmetrize-fd
  run $o --scenario logic_only --G 12 --M 2000 --seed 103
  run $o --scenario alt        --G 12 --M 1000 --seed 104
  run $o --scenario partial    --G 8  --M 2000 --seed 105 --symmetrize-fd
  run $o --scenario null       --G 20 --M 3000 --seed 106 --symmetrize-fd
  run $o --scenario partial    --G 8  --M 1000 --seed 107 --symmetrize-fd --alpha 0.2 --ties
  run $o --scenario null       --G 6  --M 1000 --seed 109 --symmetrize-fd
  run $o --scenario alt        --G 8  --M 1000 --seed 110
}
part_b() {
  local o=results/oc_jackknife_t_b.jsonl; rm -f "$o"
  run $o --scenario partial    --G 12 --M 1000 --seed 108 --symmetrize-fd --R 5
  run $o --scenario partial    --G 12 --M 1000 --seed 108 --symmetrize-fd --R 5 --ref-reps 5   # same datasets, weaker reference
  run $o --scenario alt        --G 20 --M 1000 --seed 111
  run $o --scenario alt        --G 12 --M 1000 --seed 112 --alpha 10
  run $o --scenario null       --G 30 --M 1000 --seed 114 --symmetrize-fd
  run $o --scenario logic_only --G 20 --M 2000 --seed 115
  # prespecified allocation of groups to H with family coverage (pool of 2.5 G groups)
  run $o --scenario null       --G 12 --M 2000 --seed 121 --symmetrize-fd --allocate-h --m-H 3
  run $o --scenario partial    --G 12 --M 2000 --seed 122 --symmetrize-fd --allocate-h --m-H 3
  run $o --scenario partial    --G 8  --M 1000 --seed 123 --symmetrize-fd --alpha 0.2 --ties --allocate-h --m-H 2
  run $o --scenario logic_only --G 20 --M 2000 --seed 124 --allocate-h --m-H 3
}
case $part in
  a) part_a ;;
  b) part_b ;;
  all) part_a; part_b ;;
esac
if [ -f results/oc_jackknife_t_a.jsonl ] && [ -f results/oc_jackknife_t_b.jsonl ]; then
  cat results/oc_jackknife_t_a.jsonl results/oc_jackknife_t_b.jsonl > results/oc_jackknife_t.jsonl
fi

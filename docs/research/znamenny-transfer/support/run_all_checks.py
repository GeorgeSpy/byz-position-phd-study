#!/usr/bin/env python3
"""Run the complete synthetic audit. No network, no repository modification."""
from pathlib import Path
import json
import platform
import subprocess
import sys
import time
import numpy
import scipy

ROOT=Path(__file__).resolve().parent

def main():
    jobs=[
        ('original_oracles/toy_semimarkov_checks.py',['--output',str(ROOT/'semimarkov_baseline_results.json')],'semimarkov_baseline_rerun.txt'),
        ('original_oracles/profile_hmm_regression_oracle.py',[],'profile_hmm_regression_rerun.txt'),
        ('original_oracles/alignment_product_oracle.py',[],'alignment_product_rerun.txt'),
        ('original_oracles/oracle_Zf_context_counterexample.py',[],'oracle_Zf_context_counterexample_rerun.txt'),
        ('profile_semantics_oracle.py',[],'profile_semantics_run.txt'),
        ('ecsi_kappa_context_oracle.py',[],'ecsi_kappa_context_run.txt'),
        ('bidirectional_learning_oracle.py',[],'bidirectional_learning_run.txt'),
        ('power_and_transfer_simulation.py',[],'power_and_transfer_run.txt'),
    ]
    results=[]
    for script,args,log in jobs:
        start=time.perf_counter()
        r=subprocess.run([sys.executable,str(ROOT/script),*args],cwd=ROOT,capture_output=True,text=True)
        (ROOT/log).write_text(r.stdout+('\nSTDERR\n'+r.stderr if r.stderr else ''))
        record={'script':script,'returncode':r.returncode,'seconds':time.perf_counter()-start,'log':log}
        results.append(record); print(json.dumps(record),flush=True)
    passed=all(r['returncode']==0 for r in results)
    summary={'status':'passed' if passed else 'failed','synthetic_only':True,
             'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,
             'platform':platform.platform(),'runs':results,
             'empirical_music_training':'not_run','repository_and_proposal_mutations':'none',
             'expected_failures':'The original supplemental counterexample must demonstrate failure of the old normalizer; exit code 0 means this regression was reproduced.'}
    (ROOT/'validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (ROOT/'original_oracle_rerun_status.json').write_text(json.dumps(results[:4],indent=2)+'\n')
    assert passed, 'See individual logs.'

if __name__=='__main__':main()

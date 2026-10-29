#!/usr/bin/env python3
"""Assumption-driven design simulations, not empirical Znamenny results.
Requires numpy and scipy. Fixed seeds. Run from any directory.
"""
from pathlib import Path
import json
import numpy as np
from scipy.stats import t

ROOT=Path(__file__).resolve().parent

def power():
    rng=np.random.default_rng(20261029)
    R=10000;rows=[]
    # Paired loss differences: group random effect + event residual.
    # sigma=0.2 bits/event, m=8 events/group; hypothetical, not estimated.
    for G in [12,24,48,96]:
        for icc in [.1,.5]:
            m=8;sigma=.2
            groups=rng.normal(size=(R,G))*sigma*np.sqrt(icc)
            residual=rng.normal(size=(R,G))*sigma*np.sqrt((1-icc)/m)
            noise=groups+residual
            se=noise.std(axis=1,ddof=1)/np.sqrt(G)
            c=t.ppf(.975,G-1);ci=t.ppf(.975,G-1)
            for delta in [0.,.02,.05,.1]:
                means=noise.mean(axis=1)+delta
                rate=float(np.mean(means-c*se>0))
                coverage=float(np.mean(abs(means-delta)<=ci*se))
                rows.append({'groups':G,'events_per_group':m,'event_sd':sigma,'icc':icc,'true_delta_bits':delta,'rejection_probability':rate,'MC_standard_error':float(np.sqrt(rate*(1-rate)/R)),'two_sided_95_coverage':coverage,'event_effective_N':G*m/(1+(m-1)*icc),'cluster_SE_formula':'sd(cluster means)/sqrt(G); no second design-effect correction'})
    # Six gates in a single intersection-union claim: standardized margins.
    joint=[]
    for G in [24,48,96]:
        for corr in [0.,.5]:
            common=rng.normal(size=(R,G,1));ind=rng.normal(size=(R,G,6))
            noise=np.sqrt(corr)*common+np.sqrt(1-corr)*ind
            se=noise.std(axis=1,ddof=1)/np.sqrt(G)
            for scenario,mu in [('all_positive',[.5]*6),('one_boundary_null',[0.]+[.5]*5),('all_null',[0.]*6)]:
                lower=noise.mean(axis=1)+np.array(mu)-t.ppf(.975,G-1)*se
                rate=float(np.mean(np.all(lower>0,axis=1)))
                joint.append({'groups':G,'gate_correlation':corr,'scenario':scenario,'standardized_mean_above_null':mu,'joint_rejection_probability':rate,'MC_standard_error':float(np.sqrt(rate*(1-rate)/R))})
    assert all(.015<r['rejection_probability']<.035 for r in rows if r['true_delta_bits']==0)
    assert all(r['joint_rejection_probability']<.035 for r in joint if 'null' in r['scenario'])
    return {'replications':R,'univariate':rows,'six_gate_IUT':joint,'limitations':['Gaussian independent clusters, equal group sizes, known hypothetical ICC and SD.','No evidence that real data have these parameters.','No simulation replaces pilot-based effect margins or source-group audit.','Test uses t intervals under the simulation assumptions; real ratio/F1 endpoints require paired cluster bootstrap simulation.']}

def transfer():
    rng=np.random.default_rng(991);R=5000;strength=8.;rows=[]
    # Bernoulli emission submodel with observed roles/alignment, a normalized special case.
    # This is deliberately not a fit of latent profile alignments.
    for scenario,truth in [('shared_role_law',np.array([.1,.6])),('reversed_role_law',np.array([.6,.1])),('role_independent',np.array([.35,.35]))]:
        for n in [2,8,32]:
            target=rng.binomial(n,truth,size=(R,2))
            source=rng.binomial(100,np.array([.1,.6]),size=(R,2))
            unrelated=rng.binomial(100,np.array([.35,.35]),size=(R,2))
            B=(source+1)/102;U=(unrelated+1)/102
            pooled=np.repeat(((source.sum(axis=1)+2)/204)[:,None],2,axis=1)
            # Shuffle source event-role assignment, preserving total edits and role counts.
            total=source.sum(axis=1)
            shuffled0=rng.hypergeometric(total,200-total,100)
            shuffled=(np.column_stack([shuffled0,total-shuffled0])+1)/102
            priors={'flat':np.full((R,2),.5),'Byzantine':B,'unrelated':U,'shuffled_roles':shuffled,'role_pooled':pooled}
            losses={}
            for name,prior in priors.items():
                pred=(target+strength*prior)/(n+strength)
                ce=-(truth*np.log2(pred)+(1-truth)*np.log2(1-pred)).mean(axis=1)
                losses[name]=ce
            summary={k:float(v.mean()) for k,v in losses.items()}
            contrast={k:{'mean_bits':float((v-losses['Byzantine']).mean()),'MC_standard_error':float((v-losses['Byzantine']).std(ddof=1)/np.sqrt(R))} for k,v in losses.items() if k!='Byzantine'}
            rows.append({'scenario':scenario,'target_events_per_role':n,'source_events_per_role':100,'prior_strength':strength,'expected_test_CE':summary,'gain_Byzantine_over':contrast})
    assert rows[0]['gain_Byzantine_over']['flat']['mean_bits']>0
    assert next(r for r in rows if r['scenario']=='reversed_role_law')['gain_Byzantine_over']['flat']['mean_bits']<0
    return {'replications':R,'rows':rows,'interpretation':'Known-alignment, observed-role Bernoulli emission submodel. Shows positive and negative transfer under specified truth; no historical or chant inference.'}

def main():
    result={'status':'passed','synthetic_only':True,'one_sided_alpha':.025,'seed_power':20261029,'seed_transfer':991,'power':power(),'transfer':transfer()}
    (ROOT/'power_transfer_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'power_scenarios':len(result['power']['univariate'])+len(result['power']['six_gate_IUT']),'transfer_scenarios':len(result['transfer']['rows'])}))

if __name__=='__main__':main()

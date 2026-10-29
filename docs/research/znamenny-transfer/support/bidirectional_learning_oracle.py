#!/usr/bin/env python3
"""Small exact learning audit. Synthetic profile with observed length and fixed q.
Fits ONE emission row, not a music model. Full enumeration is an independent
oracle for the context DP. Includes vanilla/joint EM and selected likelihood.
"""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('context_oracle', ROOT/'ecsi_kappa_context_oracle.py')
o = importlib.util.module_from_spec(spec); spec.loader.exec_module(o)
c = o.c
checks = []

def check(name, condition):
    assert condition, name
    checks.append(name)

def main():
    rng = np.random.default_rng(420)
    p = c.Profile(2, 2, rng); p.eM[1] = np.array([.5, .5])
    d = c.Diagnostics([1, 2], rng)
    d.w[0] = np.array([-1.0, 2., 2.5, -.3, 0.])
    d.w[1] = np.array([.1, -.5, 1.5, .2, 0.])
    rule = lambda u: int(u[0] and u[1])
    auto = c.SpecAutomaton(rule, d, 2)
    n = 3
    xs = [list(x) for x in itertools.product(range(2), repeat=n)]
    records = []
    for x in xs:
        row = []
        for weight, events in p.paths(x):
            kind, pos = events[1]
            c1 = int(kind == 'M' and x[pos-1] == 1)
            c0 = int(kind == 'M' and x[pos-1] == 0)
            Q, _ = c.path_Q(d, rule, events, x, n, n)
            q = [d.q_anchor(j, *events[j+1], x, n)[1] for j in range(2)]
            row.append((weight / (.5 ** (c0+c1)), c0, c1, Q, q))
        records.append(row)

    def components(theta):
        masses = [np.array([a*(1-theta)**c0*theta**c1 for a,c0,c1,Q,q in row]) for row in records]
        A = np.array([m.sum() for m in masses])
        selected = [m*np.array([r[3] for r in row]) for m,row in zip(masses,records)]
        B = np.array([m.sum() for m in selected])
        return masses, selected, A, B

    truth = .72; initial = .35
    _, true_joint, _, true_B = components(truth)
    # Fractional counts implement the exact population objective (no sample noise).
    counts = 1000*true_B/true_B.sum()

    def objective(theta, mode):
        _,_,A,B = components(theta)
        if mode == 'plain': return float(counts @ np.log(A/A.sum()))
        if mode == 'joint': return float(counts @ np.log(B/A.sum()))
        return float(counts @ np.log(B/B.sum()))

    def em(mode):
        theta = initial; history = [objective(theta, mode)]
        for step in range(2000):
            masses, selected, A, B = components(theta)
            ec = np.zeros(2)
            for count, row, mass in zip(counts, records, selected if mode == 'joint' else masses):
                posterior = mass/mass.sum()
                ec += count*np.array([[r[1],r[2]] for r in row]).T @ posterior
            new = float(np.clip(ec[1]/ec.sum(), 1e-7, 1-1e-7))
            value = objective(new,mode)
            assert value >= history[-1]-1e-9, (mode, step)
            history.append(value)
            if abs(new-theta) < 1e-10:
                theta = new; break
            theta = new
        check(f'{mode}_EM_monotone_all_iterations',np.min(np.diff(history))>=-1e-9)
        direct = minimize_scalar(lambda t:-objective(t,mode),bounds=(1e-7,1-1e-7),method='bounded',options={'xatol':1e-12})
        best=max(-direct.fun,objective(1e-7,mode),objective(1-1e-7,mode))
        check(f'{mode}_EM_matches_direct_objective',abs(history[-1]-best)<1e-7)
        return {'theta':theta,'iterations':len(history)-1,'initial_objective':history[0],'final_objective':history[-1],'history':history}

    fits = {mode:em(mode) for mode in ['plain','joint']}
    selected = minimize_scalar(lambda t:-objective(t,'selected'),bounds=(1e-8,1-1e-8),method='bounded',options={'xatol':1e-12})
    fits['selected_exact'] = {'theta':float(selected.x),'objective':float(-selected.fun)}
    check('selected_population_parameter_recovery',abs(selected.x-truth)<1e-6)
    check('selected_beats_joint_on_selected_objective',objective(selected.x,'selected')>objective(fits['joint']['theta'],'selected')+1e-5)

    # Independent DP verification at every fitted parameter, including global Z.
    dp_errors=[]
    for mode,fit in fits.items():
        theta=fit['theta'];p.eM[1]=np.array([1-theta,theta])
        masses,selected_masses,A,B=components(theta)
        summed,_=o.log_product(p,auto,n)
        err=abs(np.exp(summed[n][1])-B.sum());dp_errors.append(float(err))
        check(mode+'_Z_DP',err<1e-12)
        for i,x in enumerate(xs):
            obs,_=o.log_product(p,auto,n,x=x)
            check(mode+f'_B_DP_{i}',abs(np.exp(obs[n][1])-B[i])<1e-12)
        check(mode+'_normalized_selected',abs((B/B.sum()).sum()-1)<1e-12)
        # Expected KL of latent alignment posteriors against synthetic truth.
        kls=[]
        for t,m in zip(true_joint,selected_masses):
            tp=t/t.sum();mp=m/m.sum();kls.append(float(tp @ np.log(tp/mp)))
        fit['selected_alignment_expected_KL_nats']=float((counts/counts.sum())@np.array(kls))
        fit['selected_objective']=objective(theta,'selected')

    # Same-posterior κ -> S comparators. No extra concept labels for one method.
    masses,_,A,B=components(initial)
    predictions={'AC':[], 'Pool':[], 'Vit':[]}
    for mass,row in zip(masses,records):
        post=mass/mass.sum();q=np.array([r[4] for r in row])
        predictions['AC'].append(float(post @ np.prod(q,axis=1)))
        predictions['Pool'].append(float(np.prod(post@q)))
        predictions['Vit'].append(float(np.prod(q[np.argmax(post)])))
    check('AC_equals_B_over_A',np.max(abs(np.array(predictions['AC'])-B/A))<1e-12)
    check('AC_differs_from_Pool',max(abs(np.array(predictions['AC'])-predictions['Pool']))>1e-4)
    # A local joint block handles correlation even at a fixed alignment.
    block=np.array([.5,0.,0.,.5]);ind=np.array([.25]*4)
    check('local_joint_block_normalizes',abs(block.sum()-1)<1e-12)
    check('local_joint_block_distinguishes_equal_marginals',block[[0,3]].sum()==1 and ind[[0,3]].sum()==.5)

    # Identifiability failure: same X distribution, different latent mixture and m.
    px=np.array([.6,.4]);theta0=.2;theta1=.8
    acceptance=lambda t:(1-t)*.2+t*.8
    b0=px*acceptance(theta0);b1=px*acceptance(theta1)
    check('observed_X_does_not_identify_alignment_mixture',np.allclose((1-theta0)*px+theta0*px,(1-theta1)*px+theta1*px))
    check('same_X_distribution_different_specification_probability',abs(acceptance(theta0)-acceptance(theta1))>.1)
    check('selected_X_also_unidentifiable_in_this_example',np.allclose(b0/b0.sum(),b1/b1.sum()))

    result={'status':'passed','synthetic_only':True,'checks':len(checks),'truth_theta':truth,'initial_theta':initial,
            'population_weighted_observations':1000,'observed_length':n,'fits':fits,'predictions_same_initial_posterior':predictions,
            'max_global_DP_error':max(dp_errors),'local_joint_block_equality_probability':{'joint':1.,'independent':.5},
            'identifiability_counterexample':{'theta0':theta0,'theta1':theta1,'m0':acceptance(theta0),'m1':acceptance(theta1),'same_observed_and_selected_X':True},
            'limitations':['Only one binary emission row is learned; topology and diagnostic heads are fixed.',
                           'Fractional counts come from the assumed selected model, so this is a consistency check.',
                           'No neural A1+gamma, music corpus, or real-world advantage is evaluated.',
                           'Plain EM ignores the semantic labels; conditional direct optimization is the same-information algorithmic control.'],
            'test_names':checks}
    (ROOT/'bidirectional_learning_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','checks','truth_theta','initial_theta','max_global_DP_error']}))
    print(json.dumps({k:{kk:vv for kk,vv in v.items() if kk!='history'} for k,v in fits.items()},indent=2))

if __name__=='__main__':main()

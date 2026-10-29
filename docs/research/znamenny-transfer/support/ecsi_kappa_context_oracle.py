#!/usr/bin/env python3
"""Corrected log-space profile x specification x emitted-context DP.
Independent recurrence; imports the supplied profile fixtures and rule compiler.
Exact for the documented finite-memory diagnostics, not arbitrary neural histories.
"""
import importlib.util
import itertools as it
import json
import math
import platform
import time
import tracemalloc
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('alignment_fixture',ROOT/'original_oracles/alignment_product_oracle.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
TESTS=[]

def lse(xs):
    xs=list(xs)
    if not xs:return -math.inf
    m=max(xs)
    return m if m==-math.inf else m+math.log(sum(math.exp(v-m) for v in xs))

def ck(name,x,y,tol=1e-9):
    err=abs(float(x)-float(y));assert err<tol,(name,x,y,err)
    TESTS.append({'name':name,'absolute_error':err})

def edges(p,k,kind):
    if k==p.K:
        end=p.endM if kind=='M' else p.endI if kind=='I' else 1.
        yield k,'E',end,None
        if end<1:yield k,'I',1-end,p.eI[k]
    elif kind=='M':
        yield k+1,'M',p.tM[k][0],p.eM[k+1]
        yield k,'I',p.tM[k][1],p.eI[k]
        yield k+1,'D',p.tM[k][2],None
    elif kind=='I':
        yield k+1,'M',p.tI[k][0],p.eM[k+1]
        yield k,'I',p.tI[k][1],p.eI[k]
    else:
        yield k+1,'M',p.tD[k][0],p.eM[k+1]
        yield k+1,'D',p.tD[k][1],None

def log_product(p,auto,N,x=None,n_for_factor=None,history_size=1,track_sum=False):
    """Returns log A_n, log B_n, for 0<=n<=N.
    x=None sums over ALL emitted strings using context states.
    q_anchor may use current/previous symbol and i, or supplied n_for_factor.
    q_span mean is supported exactly by track_sum=True in normalization mode.
    Caller must declare all other sufficient history statistics explicitly.
    """
    if auto.diags.end_dependent and n_for_factor is None:
        raise ValueError('End-dependent local diagnostics need one pass per n.')
    if x is None and auto.span_vars and not track_sum:
        raise ValueError('Span-mean diagnostics require sum statistic for Z.')
    if history_size<1 and x is None:
        raise ValueError('These fixture diagnostics require previous emission.')
    nf=N if n_for_factor is None else n_for_factor
    cells=[[{} for _ in range(p.K+1)] for _ in range(N+1)]
    cells[0][0]['M',auto.w0,(),0]=0.
    ends=[[] for _ in range(N+1)];accepted=[[] for _ in range(N+1)]
    max_states=0
    for i in range(N+1):
        for k in range(p.K+1):
            max_states=max(max_states,len(cells[i][k]))
            for (kind,w,h,total),value in list(cells[i][k].items()):
                for kk,q,t,e in edges(p,k,kind):
                    if t<=0:continue
                    if q=='E':
                        v=value+math.log(t);ends[i].append(v)
                        xx=list(x[:i]) if x is not None else ([total/i]*i if i else [])
                        if i==0 and auto.span_vars:continue
                        R=float(auto.R(xx,i)[w])
                        if R>0:accepted[i].append(v+math.log(R))
                        continue
                    emitted=e is not None
                    if emitted and i==N:continue
                    symbols=([x[i]] if x is not None else range(p.V)) if emitted else [None]
                    for sym in symbols:
                        ii=i+int(emitted)
                        hh=(h+(sym,))[-history_size:] if emitted else h
                        ss=total+(sym if emitted and track_sum else 0)
                        v=value+math.log(t)+(math.log(e[sym]) if emitted else 0.)
                        if q in ('M','D'):
                            if x is not None:xx=list(x)
                            else:
                                xx=[0]*max(ii,1)
                                if emitted:
                                    xx[ii-1]=sym
                                    for offset,old in enumerate(reversed(h),start=2):
                                        if ii-offset>=0:xx[ii-offset]=old
                            mat=auto.T(kk,q,ii,xx,nf)
                            targets=[(ww,float(mat[w,ww])) for ww in range(auto.W[kk]) if mat[w,ww]>0]
                        else:targets=[(w,1.)]
                        for ww,weight in targets:
                            key=(q,ww,hh,ss)
                            d=cells[ii][kk];d[key]=lse([d.get(key,-math.inf),v+math.log(weight)])
    return {i:(lse(ends[i]),lse(accepted[i])) for i in range(N+1)},max_states

def brute_global(p,d,rule,N):
    out={}
    for n in range(1,N+1):
        pairs=[c.brute_AB(p,d,rule,list(x),n) for x in it.product(range(p.V),repeat=n)]
        out[n]=(sum(a for a,b in pairs),sum(b for a,b in pairs))
    return out

def regression():
    errors=[]
    for seed in [60,61,62]:
        rng=np.random.default_rng(seed);p=c.Profile(2,3,rng);d=c.Diagnostics([1,2],rng)
        for w in d.w:w[2]=7.
        rule=lambda u:int(u[0] and u[1]);auto=c.SpecAutomaton(rule,d,2)
        exact=brute_global(p,d,rule,4);got,_=log_product(p,auto,4)
        old=c.product_dp(p,auto,[0]*4,4,sum_emissions=True)
        oldZ=sum(float(E@auto.R([0]*4,n)) for n,E in old.items())
        Z=sum(b for a,b in exact.values());newZ=sum(math.exp(got[n][1]) for n in range(1,5))
        for n,(a,b) in exact.items():
            ck(f'A_context_seed{seed}_n{n}',math.exp(got[n][0]),a)
            ck(f'Z_context_seed{seed}_n{n}',math.exp(got[n][1]),b)
        ck(f'conditional_length_window_seed{seed}',newZ/Z,1.)
        errors.append({'seed':seed,'old_relative_error':abs(oldZ-Z)/Z,'corrected_relative_error':abs(newZ-Z)/Z,'enumerated_Z_1_to_4':Z})
    return errors

def contexts_and_gradients():
    rng=np.random.default_rng(42);p=c.Profile(2,2,rng)
    # Full finite terminal statistic: sum of emitted symbols, including insertions.
    d=c.Diagnostics([1,2,'span'],rng);rule=lambda u:int((u[0] or u[1]) and u[2]);auto=c.SpecAutomaton(rule,d,2)
    exact=brute_global(p,d,rule,4);got,_=log_product(p,auto,4,track_sum=True)
    for n,(a,b) in exact.items():
        ck(f'terminal_stat_A_n{n}',math.exp(got[n][0]),a)
        ck(f'terminal_stat_Z_n{n}',math.exp(got[n][1]),b)
    x=[0,1,1,0]
    obs,_=log_product(p,auto,4,x=x)
    for n in range(1,5):
        a,b=c.brute_AB(p,d,rule,x,n)
        ck(f'observed_log_A_n{n}',math.exp(obs[n][0]),a)
        ck(f'observed_log_B_n{n}',math.exp(obs[n][1]),b)
    # End-dependent internal diagnostics require separate passes, also for Z.
    d.end_dependent=True
    for n in range(1,5):
        a,b=brute_global(p,d,rule,n)[n]
        got,_=log_product(p,auto,n,n_for_factor=n,track_sum=True)
        ck(f'end_dependent_Z_n{n}',math.exp(got[n][1]),b)
    d.end_dependent=False
    n=3;x=[0,1,0]
    def score_expectation(x):
        records=[]
        for weight,events in p.paths(x):
            Q,_=c.path_Q(d,rule,events,x,len(x),len(x))
            kind,pos=events[1]
            score=(int(x[pos-1]==1)-p.eM[1][1]) if kind=='M' else 0.
            records.append((weight*Q,score))
        B=sum(w for w,s in records)
        return B,sum(w*s for w,s in records)
    B,dB=score_expectation(x);allrec=[score_expectation(list(z)) for z in it.product(range(2),repeat=n)]
    Z=sum(v[0] for v in allrec);dZ=sum(v[1] for v in allrec)
    analytic=dB/B-dZ/Z
    logits=np.log(p.eM[1]);eps=1e-5;vals=[]
    for sign in [1,-1]:
        z=logits.copy();z[1]+=sign*eps;prob=np.exp(z-max(z));p.eM[1]=prob/prob.sum()
        observed,_=log_product(p,auto,n,x=x)
        global_,_=log_product(p,auto,n,track_sum=True)
        vals.append(observed[n][1]-global_[n][1])
    p.eM[1]=np.exp(logits)
    ck('conditional_kappa_logit_gradient_including_Z',(vals[0]-vals[1])/(2*eps),analytic,1e-8)
    # All 255 specifications: independent log recurrence vs mixture.
    for mask in range(1,256):
        U=list(it.product([0,1],repeat=3))
        rule2=lambda u,m=mask:(m>>U.index(tuple(u)))&1
        aa=c.SpecAutomaton(rule2,d,2)
        logs,_=log_product(p,aa,n,x=x)
        A2,B2=c.brute_AB(p,d,rule2,x,n)
        ck(f'ECSI_identity_{mask}',math.exp(logs[n][1]-logs[n][0]),B2/A2)

def selection_and_learning():
    # Selected Bernoulli observations: acceptance probabilities Q(0)=.2,Q(1)=.7.
    Q=np.array([.2,.7]);counts=np.array([2.,8.])
    def objective(theta,conditional):
        p=np.array([1-theta,theta]);B=p*Q
        return float(counts@np.log(B)- (counts.sum()*math.log(B.sum()) if conditional else 0))
    joint=minimize_scalar(lambda z:-objective(z,False),bounds=(.001,.999),method='bounded')
    cond=minimize_scalar(lambda z:-objective(z,True),bounds=(.001,.999),method='bounded')
    ck('joint_selection_MLE',joint.x,.8,2e-5)
    ck('conditional_selection_MLE',cond.x,8*.2/(2*.7+8*.2),2e-5)
    assert objective(cond.x,True)>objective(joint.x,True)
    TESTS.append({'name':'selection_objectives_differ','absolute_error':0.})
    entropy=lambda p:-sum(v*math.log2(v) for v in p if v)
    assert entropy([.5,.5])>entropy([.9,.05,.05])
    TESTS.append({'name':'constraint_may_increase_alignment_entropy','absolute_error':0.})
    # Same-location concepts can covary through uncertain placement.
    Y=np.array([.1,.9]);ac=float(np.mean(Y*Y));pool=float(np.mean(Y)**2)
    ck('same_landmark_covariance',ac-pool,float(np.var(Y)))
    return {'joint_theta':joint.x,'selected_conditional_theta':cond.x,'selected_loglik_gain':objective(cond.x,True)-objective(joint.x,True),'same_landmark_AC':ac,'same_landmark_Pool':pool}

def benchmark():
    rows=[]
    for K,V,N in [(4,8,32),(8,16,64)]:
        r=np.random.default_rng(K);p=c.Profile(K,V,r)
        d=c.Diagnostics(list(range(1,K+1)),r);rule=lambda u:int(all(u));auto=c.SpecAutomaton(rule,d,K)
        x=list(r.integers(V,size=N))
        tracemalloc.start();start=time.perf_counter()
        logs,states=log_product(p,auto,N,x=x)
        elapsed=time.perf_counter()-start;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        rows.append({'mode':'observed_B','K':K,'V':V,'N':N,'W':max(auto.W),'seconds':elapsed,'python_peak_traced_bytes':peak,'max_cell_states':states,'finite_log_B':math.isfinite(logs[N][1])})
    r=np.random.default_rng(12);p=c.Profile(4,8,r);d=c.Diagnostics([1,2,3,4],r);auto=c.SpecAutomaton(lambda u:int(all(u)),d,4)
    tracemalloc.start();start=time.perf_counter();logs,states=log_product(p,auto,16)
    elapsed=time.perf_counter()-start;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    rows.append({'mode':'summed_Z_previous_symbol','K':4,'V':8,'N':16,'W':max(auto.W),'seconds':elapsed,'python_peak_traced_bytes':peak,'max_cell_states':states,'finite_log_Z':math.isfinite(logs[16][1])})
    return rows

def main():
    errors=regression();contexts_and_gradients();selection=selection_and_learning();bench=benchmark()
    result={'status':'passed','synthetic_only':True,'checks':len(TESTS),'max_absolute_error':max(v['absolute_error'] for v in TESTS),'Z_regression':errors,'selection':selection,'benchmark':bench,'python':platform.python_version(),'numpy':np.__version__,'details':TESTS,'scope':'Finite-memory diagnostics and mean-of-symbols terminal statistic; benchmark dimensions are design stress cases, not measured corpus sizes.'}
    (ROOT/'ecsi_kappa_context_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','checks','max_absolute_error','Z_regression','selection','benchmark']},indent=2))

if __name__=='__main__':main()

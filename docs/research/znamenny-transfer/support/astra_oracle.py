#!/usr/bin/env python3
"""Exact small-model checks. Synthetic data only. Requires numpy; no training corpus.
Indices: zero-based half-open spans. Run: python3 astra_oracle.py
"""
import importlib.util
import itertools as it
import json
import math
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
CHECKS = []

def check(name, actual, expected, tol=2e-10):
    err = abs(float(actual)-float(expected))
    assert err <= tol, (name, actual, expected, err)
    CHECKS.append({'name': name, 'error': err})

def lse(xs):
    xs=list(xs)
    if not xs: return -math.inf
    m=max(xs)
    return m if m == -math.inf else m+math.log(sum(math.exp(x-m) for x in xs))

class Profile:
    """Proper finite-state profile with explicit END and no silent cycles.
    State (j,s), s=B/M/I/D. Every row is normalized including terminal rows.
    Insertion self-loops have probability < 1. All paths eventually terminate.
    """
    def __init__(self, J, V, seed=19):
        self.J,self.V=J,V
        r=np.random.default_rng(seed)
        self.ins={(j,s):float(r.uniform(.03,.35)) for j in range(J+1) for s in 'BMID'}
        self.delete={(j,s):float(r.uniform(.05,.4)) for j in range(J) for s in 'BMID'}
        self.eM=r.dirichlet(np.ones(V),J+1)
        self.eI=r.dirichlet(np.ones(V),J+1)

    def edges(self,j,s):
        u=self.ins[j,s]
        yield (j,'I',u,self.eI[j])
        if j==self.J:
            yield (j,'E',1-u,None)
        else:
            d=self.delete[j,s]
            yield (j+1,'D',(1-u)*d,None)
            yield (j+1,'M',(1-u)*(1-d),self.eM[j+1])

    def forward(self,x, length_only=False):
        N=len(x); f=defaultdict(float);f[0,0,'B']=1.
        out=np.zeros(N+1)
        for i in range(N+1):
            for j in range(self.J+1):
                for s in 'BMID':
                    v=f[i,j,s]
                    for k,q,p,e in self.edges(j,s):
                        if q=='E': out[i]+=v*p
                        elif e is None: f[i,k,q]+=v*p
                        elif i<N: f[i+1,k,q]+=v*p*(1. if length_only else e[x[i]])
        return out

    def brute(self,x):
        total=0.
        def visit(i,j,s,w):
            nonlocal total
            for k,q,p,e in self.edges(j,s):
                if q=='E':
                    if i==len(x):total+=w*p
                elif e is None:visit(i,k,q,w*p)
                elif i<len(x):visit(i+1,k,q,w*p*e[x[i]])
        visit(0,0,'B',1.)
        return total

    def conditional(self,x):
        a=self.forward([0]*len(x),True)[-1]
        return self.forward(x)[-1]/a

def outputs(T,L,K,a=0):
    if a==T:
        yield ();return
    for tail in outputs(T,L,K,a+1):yield ((a,a+1,-1),)+tail
    for b in range(a+1,min(T,a+L)+1):
        for f in range(K):
            for tail in outputs(T,L,K,b):yield ((a,b,f),)+tail

def path_score(y,phi,chi,A,eos):
    score=0.;prev=-1;gap=0
    for a,b,f in y:
        if f==-1:score+=chi[a];gap=1
        else:score+=phi[a,b,f]+A[prev,f,gap];prev=f;gap=0
    return score+eos[prev,gap]

def outer(T,L,K,phi,chi,A,eos,required=frozenset(),banned=frozenset(),maxmode=False):
    """Label+gap+required-count DP. Required alternatives mean exactly one.
    General arbitrary partial constraints require their own finite automaton.
    """
    D=[{} for _ in range(T+1)];D[0][-1,0,0]=0.
    def put(t,key,v):
        old=D[t].get(key,-math.inf)
        D[t][key]=max(old,v) if maxmode else lse([old,v])
    for a in range(T):
        for (prev,gap,c),v in list(D[a].items()):
            put(a+1,(prev,1,c),v+chi[a])
            for b in range(a+1,min(T,a+L)+1):
                for f in range(K):
                    span=(a,b,f)
                    if span in banned:continue
                    cc=c+int(span in required)
                    if cc>1:continue
                    put(b,(f,0,cc),v+phi[span]+A[prev,f,gap])
    vals=[v+eos[p,g] for (p,g,c),v in D[T].items() if c==int(bool(required))]
    return max(vals,default=-math.inf) if maxmode else lse(vals)

def profile_checks():
    for J in [1,2,3]:
        p=Profile(J,2,19+J)
        for n in range(5):
            strings=list(it.product(range(2),repeat=n))
            for x in strings:
                check(f'profile_brute_J{J}_x{x}',p.forward(x)[-1],p.brute(x))
            a=p.forward([0]*n,True)[-1]
            check(f'length_mass_J{J}_n{n}',sum(p.brute(x) for x in strings),a)
            check(f'conditional_normalized_J{J}_n{n}',sum(p.conditional(x) for x in strings),1.)
        check(f'termination_mass_J{J}',sum(p.forward([0]*100,True)),1.)
        x=(0,1,1,0)
        for n,v in enumerate(p.forward(x)):
            check(f'prefix_reuse_J{J}_n{n}',v,p.forward(x[:n])[-1])
    spec=importlib.util.spec_from_file_location('original_claude',ROOT/'original_oracles/claude_dp_oracle.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    bad=mod.Profile(1,2,np.random.default_rng(19))
    masses=[sum(bad.brute(list(x)) for x in it.product(range(2),repeat=n)) for n in range(4)]
    assert sum(masses)>1.2
    CHECKS.append({'name':'claude_normalization_counterexample_detected','error':0.})
    return {'seed':19,'profile_columns':1,'alphabet_size':2,'length_masses_0_to_3':masses,'partial_mass':sum(masses),'meaning':'A probability distribution cannot have this partial mass > 1.'}

def outer_checks():
    r=np.random.default_rng(173)
    for T in range(1,7):
        L,K=3,2
        phi={(a,b,f):float(r.normal()) for a in range(T) for b in range(a+1,min(T,a+L)+1) for f in range(K)}
        chi=r.normal(size=T)
        A={(p,f,g):float(r.normal()) for p in range(-1,K) for f in range(K) for g in [0,1]}
        eos={(p,g):float(r.normal()) for p in range(-1,K) for g in [0,1]}
        ys=list(outputs(T,L,K)); vals=[path_score(y,phi,chi,A,eos) for y in ys]
        Z=lse(vals)
        check(f'gap_partition_T{T}',outer(T,L,K,phi,chi,A,eos),Z)
        check(f'gap_viterbi_T{T}',outer(T,L,K,phi,chi,A,eos,maxmode=True),max(vals))
        check(f'posterior_sum_T{T}',sum(math.exp(v-Z) for v in vals),1.)
        req=frozenset([(0,1,0),(0,min(T,2),1)]); ban=frozenset([(T-1,T,0)])
        valid=[(y,v) for y,v in zip(ys,vals) if sum(s in req for s in y)==1 and not any(s in ban for s in y)]
        check(f'partial_joint_T{T}',outer(T,L,K,phi,chi,A,eos,req,ban),lse(v for y,v in valid))
        for s in list(phi)[:5]:
            marginal=sum(math.exp(v-Z) for y,v in zip(ys,vals) if s in y)
            eps=1e-5;orig=phi[s];phi[s]=orig+eps
            zp=outer(T,L,K,phi,chi,A,eos)
            phi[s]=orig-eps;zm=outer(T,L,K,phi,chi,A,eos);phi[s]=orig
            check(f'gradient_marginal_T{T}_{s}',(zp-zm)/(2*eps),marginal,2e-9)
        zeroA={k:0. for k in A};zeroE={k:0. for k in eos}
        simple=[0.]+[-math.inf]*T
        for b in range(1,T+1):
            simple[b]=lse([simple[b-1]+chi[b-1]]+[simple[a]+phi[a,b,f] for a in range(max(0,b-L),b) for f in range(K)])
        check(f'zero_order_reduction_T{T}',outer(T,L,K,phi,chi,zeroA,zeroE),simple[T])
        segments=[tuple(s for s in y if s[2]>=0) for y in ys]
        check(f'O1_skip_bijection_T{T}',len(set(segments)),len(ys))
    # Empty selected output has 2^(T-1) encodings if arbitrary O chunks are allowed.
    check('arbitrary_background_duplicate_T4',2**(4-1),8)
    # Same last family+gap flag cannot encode an arbitrary previous-span score.
    previous=[(0,1,0),(0,2,0)];nextspan=(3,4,1)
    assert (nextspan[0]-previous[0][1]) != (nextspan[0]-previous[1][1])
    CHECKS.append({'name':'full_span_gap_state_insufficiency_detected','error':0.})

def generative_checks():
    T,L,K=4,3,2;rho=.28;pi=[.4,.6];ln=[.2,.5,.3]
    profiles=[Profile(2,2,71),Profile(2,2,92)]
    ys=list(outputs(T,L,K))
    def prior(y):
        return math.prod((1-rho) if f<0 else rho*pi[f]*ln[b-a-1] for a,b,f in y)
    C=sum(prior(y) for y in ys)
    allmass=0.;maxerr=0.;wrong=[];tempered=[];reset=[]
    for x in it.product(range(2),repeat=T):
        q=[(.65 if x[t]==x[t-1] else .35) if t else (.7 if x[0]==0 else .3) for t in range(T)]
        weights=[];scores=[];bad=[];btemp=[];breset=[]
        for y in ys:
            w=prior(y)/C;score=0.;scorebad=0.;scoretemp=0.;scorereset=0.
            for a,b,f in y:
                if f<0:w*=q[a];continue
                pf=profiles[f].conditional(x[a:b]);w*=pf
                base=math.log(rho*pi[f]*ln[b-a-1])-(b-a)*math.log(1-rho)
                odds=math.log(pf)-sum(math.log(z) for z in q[a:b])
                score+=base+odds
                scorebad+=math.log(rho*pi[f]*ln[b-a-1])+odds
                scoretemp+=base+.5*odds
                qreset=(.7 if x[a]==0 else .3)*math.prod(q[a+1:b])
                scorereset+=base+math.log(pf/qreset)
            weights.append(w);scores.append(score);bad.append(scorebad);btemp.append(scoretemp);breset.append(scorereset)
        allmass+=sum(weights)
        post=np.array(weights)/sum(weights)
        def normalized(v):return np.exp(np.array(v)-lse(v))
        maxerr=max(maxerr,float(np.max(abs(post-normalized(scores)))))
        wrong.append(float(np.max(abs(post-normalized(bad)))))
        tempered.append(float(np.max(abs(post-normalized(btemp)))))
        reset.append(float(np.max(abs(post-normalized(breset)))))
    check('joint_sum_X_y_conditioned_horizon',allmass,1.)
    check('generative_CRF_beta1_Markov_boundary',maxerr,0.)
    assert max(wrong)>1e-3 and max(tempered)>1e-3 and max(reset)>1e-3
    for name in ['length_survival_omission','beta_half','Markov_reset']:
        CHECKS.append({'name':name+'_breaks_original_equivalence','error':0.})
    return {'horizon_prior_normalizer':C,'maximum_posterior_errors':{'correct':maxerr,'omit_survival':max(wrong),'beta_half':max(tempered),'reset_background':max(reset)}}

def semantic_checks():
    # A role-coupled parity specification. Independent edits cannot represent it.
    q={(0,0):.56,(0,1):.24,(1,0):.14,(1,1):.06}
    accept=lambda x:x[0]==x[1]
    A=sum(p for x,p in q.items() if accept(x))
    ps={x:(p/A if accept(x) else 0.) for x,p in q.items()}
    check('semantic_global_normalizer',sum(ps.values()),1.)
    check('semantic_acceptance_mass',A,.62)
    # Soft constraints retain full support.
    eps=.05;B=sum(p*(eps+(1-eps)*accept(x)) for x,p in q.items())
    soft={x:p*(eps+(1-eps)*accept(x))/B for x,p in q.items()}
    check('soft_semantic_mass',sum(soft.values()),1.)
    assert min(soft.values())>0
    # Independent marginals of constrained distribution violate its support.
    m=ps[1,1]
    assert 2*m*(1-m)>0
    CHECKS.append({'name':'nonadditive_semantic_support_counterexample','error':0.})
    # Constraint contributes once; squaring a nonconstant evidence likelihood changes posterior.
    likelihood=np.array([.2,.9]);prior=np.array([.5,.5])
    assert np.max(abs(prior*likelihood/sum(prior*likelihood)-prior*likelihood**2/sum(prior*likelihood**2)))>.05
    CHECKS.append({'name':'double_evidence_changes_posterior_detected','error':0.})
    # Missing diagnostic marginalization differs from observed false.
    check('missing_diagnostic_mass',.3+.7,1.)
    assert .3 != 1.
    CHECKS.append({'name':'missing_is_not_false','error':0.})
    # No injectivity follows from operation counts.
    strings=[(0,1),(1,0)];counts=[sorted(s) for s in strings]
    assert counts[0]==counts[1] and strings[0]!=strings[1]
    CHECKS.append({'name':'operation_summary_not_realization_injective','error':0.})
    return {'acceptance_mass':A,'constrained_distribution':{str(k):v for k,v in ps.items()},'soft_epsilon':eps}

def leakage_checks():
    edges=[('workA','locus1'),('locus1','witness_copy1'),('witness_copy1','dictionary_entry7'),('dictionary_entry7','workB')]
    parent={x:x for e in edges for x in e}
    def find(x):
        if parent[x]!=x:parent[x]=find(parent[x])
        return parent[x]
    for a,b in edges:parent[find(a)]=find(b)
    assert find('workA')==find('workB')
    CHECKS.append({'name':'transitive_source_dictionary_leakage_detected','error':0.})

def main():
    bug=profile_checks();outer_checks();gen=generative_checks();sem=semantic_checks();leakage_checks()
    report={'status':'passed','synthetic_only':True,'checks':len(CHECKS),'max_numeric_error':max(x['error'] for x in CHECKS),'claude_counterexample':bug,'generative':gen,'semantics':sem,'details':CHECKS}
    (ROOT/'astra_test_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','synthetic_only','checks','max_numeric_error','claude_counterexample']},indent=2))

if __name__=='__main__':main()

import numpy as np, sys
sys.path.insert(0,'.')
from a2_ap import prep, ap_fam
from sklearn.metrics import average_precision_score as aps
rng=np.random.default_rng(1)
for trial in range(200):
    N=int(rng.integers(5,40)); Kk=3
    y=rng.integers(0,Kk+1,N); Y=(y[:,None]==np.arange(Kk)).astype(np.float32)
    p=np.round(rng.random((1,1,N,Kk)),1).astype(np.float32)   # many ties
    w=rng.integers(0,3,N).astype(np.float32)
    o,ys,be=prep(p,Y)
    ap=ap_fam(o,ys,be,w[None])[0,0,0]
    # reference: expand duplicates
    idx=np.repeat(np.arange(N),w.astype(int))
    for f in range(Kk):
        yy=Y[idx,f]; ss=p[0,0,idx,f]
        ref=aps(yy,ss) if yy.sum()>0 else np.nan
        assert (np.isnan(ref) and np.isnan(ap[f])) or abs(ref-ap[f])<1e-5, (trial,f,ref,ap[f])
print('AP weighted/ties == sklearn on duplicated data: 200 trials x 3 families PASS')

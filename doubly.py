from scipy import stats
from collections import namedtuple
import numpy as np
Na = 18
Nb = 19

GehanResult = namedtuple('GehanResult', ['u', 'pvalue'])
def gehan2sided(va, vb, ra, rb, la, lb):
    n1 = len(va)
    n2 = len(vb)
    v = np.concatenate( [va, vb] )
    r = np.concatenate( [ra, rb] )
    l = np.concatenate( [la, lb] )

    oand = np.logical_and.outer
    e = ~r & ~l
    s = np.sign( np.subtract.outer(v, v) )
    s *= (oand(e,e)
            | (oand(e, r)&(s <= 0))  | (oand(r, e)&(s >= 0))
            | (oand(e, l) & (s > 0)) | (oand(l, e)&(s < 0))
            | (oand(r, l) & (s > 0)) | (oand(l, r)&(s < 0)))
    w = s.sum(1)
    labels = np.ones(n1+n2, bool)
    labels[n1:] = False
    stat = w[labels].sum()
    p = stats.norm.cdf(stat/np.sqrt(n1*n2/(n1+n2+1)*w.var()))
    p = min(p, 1-p)
    p *= 2
    return GehanResult(stat, p)

rs = []
for _ in range(10000):
    va = np.random.random(size=Na)
    vb = np.random.random(size=Nb)
    la = np.random.random(size=Na) < .2
    ra = np.random.random(size=Na) < .2
    rb = np.random.random(size=Nb) < .2
    lb = np.random.random(size=Nb) < .2
    rs.append(gehan2sided(va, vb, ra, rb, la, lb))


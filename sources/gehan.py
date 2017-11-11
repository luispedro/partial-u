from scipy import stats
from collections import namedtuple
import numpy as np

GehanResult = namedtuple('GehanResult', ['u', 'pvalue'])
def gehan2sided(va, vb, la, lb, ra, rb):
    '''
    va : values for A
    vb : values for B
    la/lb : whether the corresponding value is left censored
    ra/rb : whether the corresponding value is right censored
    '''
    n1 = len(va)
    n2 = len(vb)
    v = np.concatenate( [va, vb] )
    l = np.concatenate( [la, lb] )
    r = np.concatenate( [ra, rb] )
    ok = ~r | ~l

    oand = np.logical_and.outer
    e = ~r & ~l
    s = np.sign( np.subtract.outer(v, v) )
    s *= oand(ok,ok) & (
            (oand(e,e)
            | (oand(e, r) & (s < 0)) | (oand(r, e) & (s > 0))
            | (oand(e, l) & (s > 0)) | (oand(l, e) & (s < 0))
            | (oand(r, l) & (s > 0)) | (oand(l, r) & (s < 0))))
    w = s.sum(1)
    stat = w[:n1].sum()
    p = stats.norm.cdf(stat/np.sqrt(n1*n2/(n1+n2+1)*w.var()))
    p = min(p, 1-p)
    p *= 2
    return GehanResult(stat, p)

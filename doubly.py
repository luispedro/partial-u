import numpy as np
Na = 18
Nb = 19

def old_school(va, vb, ra, rb, la, lb):
    diffs = np.subtract.outer(va, vb)
    sign = np.sign(diffs)

    ea = ~ra & ~la
    eb = ~rb & ~lb

    oand = np.logical_and.outer

    valid =  (oand(ea, eb)
            |oand(ea, lb)&(sign>0) | oand(ea,rb)&(sign<0)
            |oand(la, eb)&(sign<0) | oand(la,rb)&(sign<0)
            |oand(ra, eb)&(sign>0) | oand(ra,lb)&(sign>0))

    U = np.sum( sign * valid )
    return U


def new_school(va, vb, ra, rb, la, lb):
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
    labels = np.ones(Na+Nb, bool)
    labels[Na:] = False
    return w[labels].sum()


for _ in range(10000):
    va = np.random.random(size=Na)
    vb = np.random.random(size=Nb)
    la = np.random.random(size=Na) < .2
    ra = np.random.random(size=Na) < .2
    rb = np.random.random(size=Nb) < .2
    lb = np.random.random(size=Nb) < .2
    print(old_school(va, vb, ra, rb, la, lb) - new_school(va, vb, ra, rb, la, lb))


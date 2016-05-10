from scipy import stats
import numpy as np
from partialU import partial_U_test, Diff
from gehan import gehan2sided

def clip(v):
    return np.clip(v, -7, 0)

def clip_diff(v0, v1):
    return clip(v0) - clip(v1)

def gehan_diff(start0, end0, start1, end1):
    return gehan2sided(clip_diff(end0, start0), clip_diff(end1, start1), start0 < -7, start1 < -7, end0 < -7, end1 < -7)

def compare_clipping(N, delta0=-2, delta1=-4):
    start0 = -10*np.random.rand(N) - 2
    start1 = -10*np.random.rand(N) - 2


    end0 = start0 + np.random.normal(delta0, 1, size=N)
    end1 = start1 + np.random.normal(delta1, 1, size=N)
    end0[end0 > 0] = 0
    end1[end1 > 0] = 0

    if np.all(end0 < -7) and np.all(end1 < -7):
        return compare_clipping(N, delta0, delta1)


    values0 = [Diff(e,s) for e,s in zip(end0, start0)]
    values1 = [Diff(e,s) for e,s in zip(end1, start1)]
    return (
        stats.mannwhitneyu(end0, end1).pvalue,
        stats.mannwhitneyu(end0 - start0, end1 - start1).pvalue,
        stats.mannwhitneyu(clip(end0), clip(end1)).pvalue,
        stats.mannwhitneyu(clip_diff(end0, start0), clip_diff(end1, start1)).pvalue,
        partial_U_test(values0, values1)[1],
        gehan_diff(start0, end0, start1, end1)[1])



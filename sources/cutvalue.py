from scipy import stats
import numpy as np
from partialU import partial_U_test
from jug import TaskGenerator

class CutValue(object):
    def __init__(self, v):
        if v > -7:
            self.type = 'exact'
            self.value = v
        else:
            self.type = 'lt'
            self.value = -7
    def __str__(self):
        return '{}({})'.format(self.type, self.value)
    __repr__ = __str__




@TaskGenerator
def compare_tests(n, effect_mu, effect_sigma, size=100):
    pvalues = []
    for _ in range(size):
        e0 = np.random.uniform(-14, -5, size=n)
        e1 = np.random.uniform(-14, -5, size=n)
        if effect_mu != 0:
            e1 += np.random.normal(effect_mu, effect_sigma, size=n)
        e1 = np.clip(e1, -20, 0)

        c0 = list(map(CutValue,e0))
        c1 = list(map(CutValue,e1))
        pvalues.append([
            stats.mannwhitneyu(e0, e1).pvalue*2,
            stats.mannwhitneyu(np.clip(e0, -7, 0), np.clip(e1, -7, 0)).pvalue*2,
            partial_U_test(c0,c1)])

    return np.array(pvalues)

pvals = {}
for mu,sig in [( 0, 0),
               (-3, 2),
               (-3, 1),
               (-2, 2),
               (-2, 1),
               (-1, 1),
               (-1, 2),
               ( 1, 2),
               ( 1, 1)]:
    pvals[mu,sig] = compare_tests(30, mu, sig)

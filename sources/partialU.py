import random
class Diff(object):
    def __init__(self, e, s):
        if e > -7 and s > -7:
            self.type = 'exact'
            self.value = e - s
        elif e <= -7 and s <= -7:
            self.type = 'NA'
        elif e > -7:
            self.type = 'gt'
            self.value = e - (-7)
        else:
            self.type = 'gt'
            self.value = (-7) - s
    def __str__(self):
        if self.type == 'NA': return self.type
        return '{}({})'.format(self.type, self.value)
    __repr__ = __str__

def lt(d1, d2):
    if d1.type == 'NA' or d2.type == 'NA':
        return 'NA'
    if d1.type == 'exact' and d2.type == 'exact':
        return d1.value < d2.value
    if d1.type == 'gt' and d2.type == 'gt':
        return 'NA'
    if d1.type == 'exact' and d1.value < d2.value:
        return True
    if d2.type == 'exact' and d2.value < d1.value:
        return False
    return 'NA'
def partial_U(diff0, diff1, cmp=None):
    if cmp is None:
        cmp = lt
    smaller = 0.
    valid = 0
    for d0 in diff0:
        for d1 in diff1:
            c = cmp(d0, d1)
            if c != 'NA':
                valid += 1
                smaller += c
    frac = smaller/valid
    return min(frac, 1.-frac)

def partial_U_test(start0, end0, start1, end1, n_permutations=10000):
    diff0 = [Diff(s0,e0) for s0,e0 in zip(start0, end0)]
    diff1 = [Diff(s1,e1) for s1,e1 in zip(start1, end1)]
    base = partial_U(diff0, diff1)
    N0 = len(diff0)
    diffs = diff0 + diff1
    diff_ids = list(range(len(diffs)))
    cache = {}
    def cached_lt(i, j):
        if (i,j) not in cache:
            cache[i,j] = lt(diffs[i], diffs[j])
        return cache[i,j]


    better = 0
    for _ in range(n_permutations):
        random.shuffle(diff_ids)
        better += (
                partial_U(diff_ids[:N0], diff_ids[N0:], cmp=cached_lt) < base)
    return float(better + 1)/n_permutations

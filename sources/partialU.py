import numpy as np
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

#=======+=======+========+=======+=========================
#       | exact | exact  | lt y  | lt y   |  gt y |   gt y
#       | x < y | x >= y | x < y | x >= y | x < y | x >= y
#=======+=======+========+=======+=========================
# exact | True  | False  |  NA   |  False | True  | NA
#-------+-------+--------+-------+--------+-------+--------
#  lt x | True  | NA     |  NA   |  NA    | True  | NA
#-------+-------+--------+-------+--------+-------+--------
#  gt x | NA    | False  |  NA   |  False | NA    | NA
#-------+-------+--------+-------+--------+-------+--------

table = {
        ('exact', 'exact'): (True, False),
        ('exact', 'lt'): ('NA', False),
        ('exact', 'gt'): (True, 'NA'),

        ('lt', 'exact') : (True, 'NA'),
        ('lt', 'lt') : ('NA', 'NA'),
        ('lt', 'gt') : (True, 'NA'),

        ('gt', 'exact') : ('NA', False),
        ('gt', 'lt') : ('NA', False),
        ('gt', 'gt') : ('NA', 'NA'),
        }



def lt(d1, d2):
    if d1.type == 'NA' or d2.type == 'NA':
        return 'NA'
    return table[d1.type, d2.type][d1.value >= d2.value]
def partial_U(values0, values1, cmp=None):
    if cmp is None:
        cmp = lt
    smaller = 0.
    valid = 0
    for d0 in values0:
        for d1 in values1:
            c = cmp(d0, d1)
            if c != 'NA':
                valid += 1
                smaller += c
    if valid == 0:
        return 1.
    frac = smaller/valid
    return min(frac, 1.-frac)

def partial_U_test(values0, values1, n_permutations=10000):
    base = partial_U(values0, values1)
    N0 = len(values0)
    diffs = values0 + values1
    diff_ids = list(range(len(diffs)))

    table_valid = np.zeros((len(diffs), len(diffs)))
    table_smaller = np.zeros((len(diffs), len(diffs)))
    for i,d0 in enumerate(diffs):
        for j, d1 in enumerate(diffs):
            v = lt(d0,d1)
            if v != 'NA':
                table_valid[i,j] = 1
                table_smaller[i,j] = v

    better = 0
    for _ in range(n_permutations):
        random.shuffle(diff_ids)
        cur = table_smaller[diff_ids[:N0]].T[diff_ids[N0:]].sum()/table_valid[diff_ids[:N0]].T[diff_ids[N0:]].sum()
        cur = min(cur, 1.-cur)
        better += (cur < base)
    return float(better + 1)/n_permutations

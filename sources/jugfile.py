from jug import TaskGenerator
from simulation import compare_clipping
import numpy as np
import random
N = 32

@TaskGenerator
def perform_comparisons(N, delta0, delta1, seed):
    random.seed(seed)
    return np.array([compare_clipping(N, delta0=delta0, delta1=delta1) for _ in range(250)])


@TaskGenerator
def print_table(comps):
    with open('table.txt', 'w') as output:
        output.write("Δ₀/Δ₁ : e\te-s\tce\tce-cs\tpartial-U\n")
        for k,v in comps.items():
            output.write("{0[0]: 2}/{0[1]: 2} : {1[0]:.2}\t{1[1]:.2}\t{1[2]:.2}\t{1[3]:.2}\t{1[4]:.2}\n".format(k,np.mean(v < 0.05, axis=0)))

comps = {}
for d0,d1 in [
            ( 0, -1),
            (-1, -2),
            (-2, -3),
            (-3, -4),
            (-4, -5),
            ( 0, -2),
            (-1, -3),
            (-2, -4),
            (-3, -5),
            ( 0,  1),
            ( 1,  2),
            ( 2,  3),
            ( 3,  4)]:
    cur = []
    for i in range(4):
        cur.append(
            perform_comparisons(N, d0, d1, 123 +i*217 + d0*2321 +d1*34666))
    comps[d0, d1] = TaskGenerator(np.concatenate)(cur)
print_table(comps)

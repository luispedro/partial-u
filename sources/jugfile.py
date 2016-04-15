from jug import TaskGenerator
from simulation import compare_clipping
import numpy as np
import random
N = 32

@TaskGenerator
def perform_comparisons(N, seed):
    random.seed(seed)
    return np.array([compare_clipping(N) for _ in range(250)])

comps = []
for i in range(32):
    comps.append(
        perform_comparisons(N, 123+i*217))

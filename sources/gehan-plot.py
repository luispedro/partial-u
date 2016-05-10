from matplotlib import pyplot as plt
from gehan import gehan2sided
import numpy as np
Na = 18
Nb = 19

rs = []
for _ in range(10000):
    va = np.random.random(size=Na)
    vb = np.random.random(size=Nb)
    la = np.random.random(size=Na) < .2
    ra = np.random.random(size=Na) < .2
    rb = np.random.random(size=Nb) < .2
    lb = np.random.random(size=Nb) < .2
    rs.append(gehan2sided(va, vb, ra, rb, la, lb))


xs = np.linspace(0,1,100)
rs = np.array([r for _,r in rs])
fig, ax = plt.subplots()
ax.plot(xs, [np.mean(rs < x) for x in xs])
fig.savefig('gehan-empty.pdf')

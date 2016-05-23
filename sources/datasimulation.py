import gehan
import numpy as np
from scipy import stats
import random
import pandas as pd
import random
from jug import TaskGenerator
from jug.compound import CompoundTaskGenerator

FEATURES = 'species'
MIN_PREVALENCE = 10
N_REPLICATES = 1000

if FEATURES == 'KEGG_ko':
    data = pd.read_table('/g/bork5/kultima/DOGS/PROFILES/functional.profiles/dogs.129/dogs.129.functional.profile.screened.screened.adapter.on.cm3.on.dogs.129.padded.solexaqa.allbest.l45.p95.insert.raw.KEGG_ko', comment='#', index_col=0)
    data = data.drop(['mapped', 'unassigned'])
    data = data.T
    total = data.sum(1)
    normed = (data.T / total)
    detect_limit = normed[normed > 0].min().min()
else:

    data = pd.read_table('/g/bork5/kultima/DOGS/PROFILES/taxonomic.profiles/dogs.65/NCBI/dogs.65.ncbi.profile.extracted.screened.screened.adapter.on.cm3.on.263MetaRef10MGv9.cal.v2.nr.padded.on.Ref10MGv9.padded.solexaqa.allbest.l45.p97.insert.mm.dist.among.unique.scaled.species.fraction', comment='#', index_col=0)
    data = data[(data != 0).sum(1) > MIN_PREVALENCE]
    data = data.T
    total = data.sum(1)
    normed = data.T
    detect_limit = normed[normed > 0].min().min()



@TaskGenerator
def perform_test(c, R, sample_by=None, uneven=False):
    random.seed(R)
    rs = []
    col = data[c]
    if sample_by is not None:
        samples = list(col.index)
        random.shuffle(samples)
        col = col[samples[:len(col)//sample_by]]

    if uneven:
        N = len(col)//4
    else:
        N = len(col)//2
    ra = np.zeros(N, bool)
    rb = np.zeros(len(col) - N, bool)
    for j,effect in enumerate(np.logspace(0, -5, 100)):
        cur = []
        for _ in range(N_REPLICATES):
            samples = list(col.index)
            random.shuffle(samples)
            s = col[samples]

            a = s[N:].values
            b = s[:N].copy()
            b *= effect

            lb = b/total.reindex(b.index) < detect_limit

            b = b.values
            b *= ~lb
            lb = lb.values

            if not (np.any(a) or np.any(b)):
                cur.append((1.,1.))
            else:
                gehan_p = gehan.gehan2sided(a, b, a == 0, lb, ra, rb)[1]
                mann_U_p = stats.mannwhitneyu(a, b)[1]
                cur.append((gehan_p, mann_U_p))
        print(j)
        rs.append(cur)
    return np.array(rs)

@TaskGenerator
def build_plots(results, ofile):
    from matplotlib import style
    from matplotlib import pyplot as plt
    style.use('seaborn-colorblind')

    plt.rcParams['lines.linewidth'] = 1.
    plt.rcParams['axes.titlesize'] = 'small'
    plt.rcParams['xtick.labelsize'] = 'x-small'
    plt.rcParams['ytick.labelsize'] = 'x-small'
    x = np.linspace(0, -5, 100)


    fig,axes = plt.subplots(12, 10, sharey=True, sharex=True, figsize=[12,10])
    ni = 0
    plim = 0.01
    for c in sorted(results.keys()):
        k = results[c]
        power = (k < plim).mean(1)
        ax = axes.flat[ni]
        ax.plot(x, power.T[0], label='Gehan')
        ax.plot(x, power.T[1], label='MWU')
        ni += 1
        m = normed.ix[c].mean()
        m = np.log10(m)
        ax.plot([m,m +1e-6], [0,1], '-k', lw=2)
        # ax.set_title('{:.1}'.format(normed.ix[c].mean()))
        if ni == len(axes.flat):
            break

    for ax in axes.flat:
        ax.set_xticks([0, -5])
        ax.set_yticks([0, 1.])
        ax.set_xlim(0, -7)
        ax.set_ylim(-.1, 1.1)

    fig.tight_layout()
    fig.savefig(ofile)


results = {}
for i,c in enumerate(data.columns):
    results[c] = perform_test(str(c), i*7, 2)
build_plots(results, 'power_dog_species_N=32.pdf')

results = {}
for i,c in enumerate(data.columns):
    results[c] = perform_test(str(c), i*7, uneven=True)
build_plots(results, 'power_dog_species_Uneven.pdf')

results = {}
for i,c in enumerate(data.columns):
    results[c] = perform_test(str(c), i*7)

build_plots(results, 'power_dog_species_N=65.pdf')

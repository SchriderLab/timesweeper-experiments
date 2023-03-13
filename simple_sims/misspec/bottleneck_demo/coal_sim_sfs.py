import msprime 
import tskit
import daiquiri 
import numpy as np
import matplotlib.pyplot as plt

daiquiri.setup(level="INFO")

demo = msprime.Demography()
demo.add_population(initial_size=20000)
demo.add_population_parameters_change(time=3000, initial_size=2000)
demo.add_population_parameters_change(time=3500, initial_size=10000)
demo.sort_events()
print(demo)

ts = msprime.sim_ancestry(
    samples=200,
    recombination_rate=1e-7,
    sequence_length=5000000,
    demography=demo,
    num_replicates=10
)

mut_ts  = [msprime.sim_mutations(i, rate=1e-7) for i in ts]

combo_afs = np.zeros((10, 401))
for idx, _ts in enumerate(mut_ts):
    afs = _ts.allele_frequency_spectrum(span_normalise=False)
    combo_afs[idx] += afs

np.savetxt("coal_sfs.csv", combo_afs, delimiter=",")

fig, ax = plt.subplots()
index = np.arange(0,20)
bar_width = 0.1
opacity = 0.9

simsfs = ax.bar(index+ 2*bar_width, np.mean(combo_afs, axis=0)[:20], bar_width, alpha=opacity, label='exp')

plt.savefig("coal_sfs.png")
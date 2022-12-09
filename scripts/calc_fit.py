import warnings
import pickle
import pandas as pd
from scipy.stats import ttest_1samp
import numpy as np
import sys

warnings.filterwarnings("ignore", category=RuntimeWarning)
# https://www.genetics.org/content/196/2/509

df = pd.DataFrame


def getRescaledIncs(freqs, gens):
    """
    Calculates allele increments for the FIT.

    Args:
        freqs (List[int]): Frequency of a given allele at each site.
        gens (List[int]): Generations that each allele is sampled.

    Returns:
        List[float]: Rescaled frequency increments that can be used in t-test.
    """
    incs = []
    i = 0
    # advance to first non-zero freq
    while i < len(freqs) and (freqs[i] == 0 or freqs[i] == 1):
        i += 1
    if i < len(freqs):
        prevFreq = freqs[i]
        prevGen = gens[i]
        i += 1
        while i < len(freqs):
            if freqs[i] != 0 and freqs[i] != 1:
                num = freqs[i] - prevFreq
                denom = ((2 * prevFreq) * (1 - prevFreq) * (gens[i] - prevGen)) ** 0.5
                incs.append(num / denom)
                prevFreq = freqs[i]
                prevGen = gens[i]
            i += 1

    return incs


def fit(freqs, gens):
    """
    Calculate FIT by performing 1-Sided Student t-test on frequency increments.

    Args:
        freqs (List[int]): Frequencies at all given generations for targeted alleles.
        gens (List[int]): Generations sampled.

    Returns:
        List[int]: t-test results.
    """
    rescIncs = getRescaledIncs(freqs, gens)
    return ttest_1samp(rescIncs, 0)


"""
Calculates fit values given AFT input from a training picklefile

cli arg 1: input training pickle file
cli arg 2: output filepath
"""

ifile = sys.argv[1]
data_dict = pickle.load(open(ifile, "rb"))

total_gens = 200
n_timepoints = 20
gens = list(range(0, total_gens, int(total_gens/n_timepoints)))

trues = []
pvals = []
for swp in ["neut", "ssv", "sdn"]:
    for rep in data_dict[swp].keys():
        if swp == "neut":
            trues.append(0)
        else:
            trues.append(1)
        
        p = fit(data_dict[swp][rep]["aft"][:, 25], gens)[1]
        if p != np.nan:
            pvals.append(p)

with open(sys.argv[2], "w+") as outfile:
    outfile.write("trues,pvals\n")
    for i, j in zip(trues, pvals):
        if j :
            outfile.write(f"{i},{j}\n")

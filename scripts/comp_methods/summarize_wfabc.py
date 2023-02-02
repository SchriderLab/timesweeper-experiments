import pandas as pd
import numpy as np
import sys
from pathlib import Path
from tqdm import tqdm

"""Iterates through a given directory to find and collect output from ApproxWF MCMC runs.

    CLI Input:
        1. Input directory, all subdirs will be globbed through.
        2. Output file, will be a csv of results.
"""


def get_sweep(filename):
    if "neut" in filename:
        return "neut"
    elif "sdn" in filename:
        return "sdn"
    elif "ssv" in filename:
        return "ssv"
    else:
        return None


in_dir = sys.argv[1]
outfile = sys.argv[2]

path = Path(in_dir)
filelist = [str(i) for i in path.glob("**/*WFABC_in_posterior_s.txt")]

reps = []
swps = []
svals = []
est_means = []
stddevs = []

for f in tqdm(filelist):
    with open(f, 'r') as ifile:
        sel_ests = [float(i) for i in ifile.readline().strip().split()]

    reps.append(f.split("/")[-2])
    swps.append(get_sweep(f))
    svals.append(float(f.split("_")[-5].split("s")[-1]))
    est_means.append(np.mean(sel_ests))
    stddevs.append(np.std(sel_ests))

res_df = pd.DataFrame(
    {"rep": reps, "sweep": swps, "s_val": svals, "estimated_s_mean": est_means, "est_std": stddevs}
)
res_df.to_csv(outfile, index=False, header=True)

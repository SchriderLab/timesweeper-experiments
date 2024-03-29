import pandas as pd
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
filelist = [str(i) for i in path.glob("**/*MCMC_output.txt")]

reps = []
swps = []
svals = []
est_means = []
stddevs = []

for f in tqdm(filelist):
    df = pd.read_csv(f, sep="\t", header=0)
    df = df[df["index"] > 10000]
    label = list(df)[-1]

    reps.append(f.split("/")[-2])
    swps.append(get_sweep(label))
    svals.append(float(label.split("_")[-1]))
    est_means.append(df[label].mean())
    stddevs.append(df[label].std())

res_df = pd.DataFrame(
    {"rep": reps, "sweep": swps, "s_val": svals, "estimated_s_mean": est_means, "est_std": stddevs}
)
res_df.to_csv(outfile, index=False, header=True)

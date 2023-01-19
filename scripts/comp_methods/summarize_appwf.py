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

swps = []
svals = []
post_means = []

for f in tqdm(filelist):
    df = pd.read_csv(f, sep="\t", header=0)
    df = df[df["index"] > 10000]
    label = list(df)[-1]

    swps.append(get_sweep(label))
    svals.append(float(label.split("_")[-1]))
    post_means = df[label].mean()

res_df = pd.DataFrame({"sweep": swps, "s_val": svals, "posterior_mean": post_means})
res_df.to_csv(outfile, index=False, header=True)

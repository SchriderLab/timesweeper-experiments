import pandas as pd
import sys
from pathlib import Path
from tqdm import tqdm
import numpy as np

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


in_dir = "/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs"
outfile = "/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/comp_methods/sf_res/sf_res.csv"

path = Path(in_dir)
filelist = [str(i) for i in path.glob("**/*.sf.res")]

reps = []
big_reps = []
big_sweeps = []
big_clrs = []
swps = []
pos = []
clrs = []
preds = []

for f in tqdm(filelist):
    df = pd.read_csv(f, sep="\t", header=0, on_bad_lines="skip")

    reps.append(f.split(".")[-3].split("/")[-1])
    swps.append(get_sweep(f))
    pos.append(float(df["location"].values[int(len(df) / 2)]))
    clrs.append([float(i) for i in list(df["LR"].values)])
    big_reps.extend([f.split(".")[-3] for _ in clrs])
    big_sweeps.extend([get_sweep(f) for _ in clrs])
    big_clrs.extend([float(i) for i in list(df["LR"].values)])

neut_clrs = [clrs[i] for i in range(len(clrs)) if swps[i] == "neut"]
threshold = np.percentile(np.stack(neut_clrs).flatten(), 95)
center_clrs = [i[int(len(i) / 2)] for i in clrs]

print(f"Neutral 95% CLR: {threshold}")

pred = []
for c in center_clrs:
    if c >= threshold:
        pred.append("sweep")
    else:
        pred.append("neut")

res_df = pd.DataFrame(
    {
        "rep": reps,
        "sweep": swps,
        "pos": pos,
        "clr": center_clrs,
        "pred": pred,
    }
)
res_df.to_csv(outfile, index=False, header=True)

all_df = pd.DataFrame({"rep": big_reps, "sweep": big_sweeps, "clr": big_clrs})

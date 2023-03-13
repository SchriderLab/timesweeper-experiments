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
filelist = [str(i) for i in path.glob("**/*shicres.csv")]

reps = []
swps = []
window = []
pred = []
neut_prob = []
hard_prob = []
hardlinked_prob = []
softlinked_prob = []
soft_prob = []

for f in tqdm(filelist):
    df = pd.read_csv(f, sep="\t", header=0)

    reps.append(f.split("/")[-1].split(".")[0])
    swps.append(get_sweep(f))
    window.append(f.split("/")[-1].split(".")[-3].split("_")[-1])
    pred.append(df["predClass"][0])
    neut_prob.append(df["prob(neutral)"][0])
    softlinked_prob.append(df["prob(likedSoft)"][0])
    soft_prob.append(df["prob(soft)"][0])
    hard_prob.append(df["prob(hard)"][0])
    hardlinked_prob.append(df["prob(linkedHard)"][0])

res_df = pd.DataFrame(
    {
        "rep": reps,
        "sweep": swps,
        "window": window,
        "pred": pred,
        "neut_prob": neut_prob,
        "softlinked_prob": softlinked_prob,
        "soft_prob": soft_prob,
        "hard_prob": hard_prob,
        "hardlinked_prob": hardlinked_prob,
    }
)
res_df.to_csv(outfile, index=False, header=True)

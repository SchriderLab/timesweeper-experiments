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
raw_filelist = [str(i) for i in path.glob("**/*spectralres.tsv")]
filelist = [i for i in raw_filelist if "all" not in i]
print(filelist[:10])

reps = []
swps = []
svals = []
est_svals = []
likelihood = []

for f in tqdm(filelist):
    #try:
    df = pd.read_csv(f, sep="\t", header=0)

    reps.append(f.split("_")[-2])
    swps.append(get_sweep(f))
    svals.append(df["true_selCoeff"].values[0])
    est_svals.append(df["est_selCoeff"].values[0])
    likelihood.append(df["max_likelihood"].values[0])
    #except:
    #    print(f)

res_df = pd.DataFrame(
    {
        "rep": reps,
        "sweep": swps,
        "s_val": svals,
        "estimated_sval": est_svals,
        "max_likelihood": likelihood,
    }
)
res_df.to_csv(outfile, index=False, header=True)

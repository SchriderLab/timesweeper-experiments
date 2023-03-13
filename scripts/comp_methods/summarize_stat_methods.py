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
filelist = [str(i) for i in path.glob("**/*stat_methods.csv")]

reps = []
swps = []
fit_pval = []
fet_pval = []
selcoeff = []

for f in tqdm(filelist):
    df = pd.read_csv(f, header=0)
    if "neut" in f:
        sdf = df.dropna().reset_index()
        sdf = sdf.loc[int(len(sdf)/2), :]
        reps.append(f.split("/")[-1].split(".")[0].split("_")[0])
        swps.append(get_sweep(f))
        selcoeff.append(sdf["s_val"])
        fit_pval.append(sdf["FIT_pval"])
        fet_pval.append(sdf["FET_pval"])
    else:
        try:
            sdf = df.loc[df["mut_type"] == 2, :]
            if len(sdf) == 0:
                continue
            reps.append(f.split("/")[-1].split(".")[0])
            swps.append(get_sweep(f))
            selcoeff.append(sdf["s_val"])
            fit_pval.append(sdf["FIT_pval"].values[0])
            fet_pval.append(sdf["FET_pval"].values[0])
        except:
            continue
        
print(len(reps), len(swps), len(selcoeff), len(fit_pval), len(fet_pval))
res_df = pd.DataFrame(
    {
        "rep": reps,
        "sweep": swps,
        "selcoeff": selcoeff,
        "fit_pval": fit_pval,
        "fet_pval": fet_pval
    }
)
res_df.to_csv(outfile, index=False, header=True)

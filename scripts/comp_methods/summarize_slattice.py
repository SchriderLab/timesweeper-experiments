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
filelist = [str(i) for i in path.glob("**/*slattice.csv.out")]

params = pd.read_csv("/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/Testing_Benchmark_params.tsv", sep="\t")
print(params.head())
reps = []
swps = []
svals = []
est_svals = []

for f in tqdm(filelist):
    #try:
    with open(f, "r") as ifile:
        est_s = ifile.readline().strip().split()[0]

    rep = f.split("/")[-2]
    swp = get_sweep(f)
    
    if swp == "neut":
        sval = 0.0
    else:
        sval = params[(params["rep"] == int(rep)) & (params["sweep"] == swp)]["selCoeff"].values[0]

    #except:
    #    continue
    
    reps.append(rep)
    swps.append(swp)
    svals.append(sval)
    est_svals.append(est_s)


res_df = pd.DataFrame(
    {
        "rep": reps,
        "sweep": swps,
        "s_val": svals,
        "estimated_sval": est_svals,
    }
)
res_df.to_csv(outfile, index=False, header=True)

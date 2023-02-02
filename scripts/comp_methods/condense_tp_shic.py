import pickle
import numpy as np
import pathlib
import pandas as pd
from tqdm import tqdm

target_path = "/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_data/vcfs"
paramfile = "/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_data/Testing_params.tsv"
params = pd.read_csv(paramfile, header=0, usecols=[0, 1, 2], sep="\t")

reps = list(range(3001))
swps = ["neut", "sdn", "ssv"]

data_reps = []
data_swps = []
arrs = []
selcoeffs = []

for rep in tqdm(list(range(3001))):
    for swp in swps:
        try:
            arrs.append(
                np.loadtxt(
                    f"{target_path}/{swp}/{rep}/merged.{swp}.win_5.fvec",
                    delimiter="\t",
                    skiprows=1,
                )
            )
            data_reps.append(rep)
            data_swps.append(swp)
            selcoeffs.append(
                params[(params["rep"] == rep) & (params["sweep"] == swp)]["selCoeff"]
            )
        except:
            continue

with open(f"{target_path}/shic_tp_test_data.pickle", "wb") as ofile:
    pickle.dump(
        {"rep": data_reps, "sweep": data_swps, "data": arrs, "selcoeff": selcoeffs},
        ofile,
    )

import pandas as pd
from glob import glob
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import random

"""
header = "Chromosome    position    -log10(p-value)_FET_rep1    -log10(p-value)_FET_rep2    -log10(p-value)_FET_rep3    -log10(p-value)_FET_rep4    -log10(p-value)_FET_rep5    -log10(p-value)_FET_rep6    -log10(p-value)_FET_rep7    -log10(p-value)_FET_rep8  -log10(p-value)_FET_rep9    -log10(p-value)_FET_rep10"

dict_list = []
with open("/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/pvals.tsv", 'r') as ifile:
    for line in tqdm(ifile.readlines()):
        line = line.strip().split()
        for rep in range(1, 11):
            line_dict = {}
            line_dict["Chrom"] = line[0]
            line_dict["BP"] = line[1]
            line_dict["rep"] = rep
            line_dict["fet"] = line[1 + rep]
            dict_list.append(line_dict)
#exp_pvals = pd.DataFrame.from_records(dict_list)
exp_pvals.to_csv("fet_all.tsv", sep="\t")
#exp_pvals = pd.read_csv("fet_all.tsv", sep="\t")

nn_list = []

for rep in tqdm(range(1, 11)):
    aft_ifiles = glob(
        f"/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/timesweeper_output/unif_velocity_0_thresh/aft_*_{rep}_preds.csv"
    )
    for aft_file in aft_ifiles:
        df = pd.read_csv(aft_file, header=0, sep="\t")
        df["rep"] = [int(rep)] * len(df)
        nn_list.append(df)

aft_df = pd.concat(nn_list)

aft_df = aft_df.astype(str)
exp_pvals = exp_pvals.astype(str)

all_merged = aft_df.merge(
    exp_pvals, left_on=["Chrom", "BP", "rep"], right_on=["Chrom", "BP", "rep"]
)

all_merged.to_csv("all_merged.tsv", sep="\t", header=True, index=False)
"""

all_merged = pd.read_csv(
    "/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/results/all_merged.tsv",
    sep="\t",
)

all_merged = all_merged.replace("na", np.NaN)
all_merged = all_merged.dropna()

all_merged["fet"] = all_merged["fet"].astype(float)
all_merged["Soft_Score"] = all_merged["Soft_Score"].astype(float)

print("Calculating correlation")
corr = all_merged[["fet", "Soft_Score"]].corr("spearman")
print(f"Spearman's Correlation: \n {corr}")

# top = all_merged.nlargest(100000, "Soft_Score")

plot = False
if plot:
    for _ in range(10):
        r = random.sample(range(len(all_merged)), 10000)
        _df = all_merged[["fet", "Soft_Score"]].iloc[r, :]
        plt.scatter(x=_df["Soft_Score"].astype(float), y=_df["fet"].astype(float))
        plt.xlabel("TS")
        plt.ylabel("FET")
        plt.title("FET vs Timesweeper")
        plt.savefig(f"fet_v_timesweeper_{_}.png")
        plt.clf()


print("Bin-wise summary")
bins = list(np.around(np.arange(0, 1.05, 0.05), 2))
bins.insert(-1, 0.99)

ts_res_bins = []
for i in tqdm(range(len(bins) - 1), desc="Summing over bins"):
    _df = all_merged[
        (all_merged["Soft_Score"] > bins[i]) & (all_merged["Soft_Score"] <= bins[i + 1])
    ]
    sp = _df["fet"].corr(_df["Soft_Score"], "spearman")

    ts_res_bins.append(
        {
            "bin": (bins[i], bins[i + 1]),
            "num_calls": len(_df),
            "spearman": sp,
            "max_fet": _df["fet"].max(),
            "min_fet": _df["fet"].min(),
            "mean_fet": _df["fet"].mean(),
            "med_fet": _df["fet"].median(),
            "variance": _df["fet"].var(),
            "std": _df["fet"].std(),
        }
    )

ts_res_df = pd.DataFrame(ts_res_bins)
ts_res_df.to_csv("fet_by_ts.tsv", sep="\t", index=False, float_format="%.3f")

bins = list(np.arange(0, 121, 5))
print(bins)
fet_res_bins = []
for i in range(len(bins) - 1):
    _df = all_merged[(all_merged["fet"] > bins[i]) & (all_merged["fet"] <= bins[i + 1])]
    sp = _df["fet"].corr(_df["Soft_Score"], "spearman")
    fet_res_bins.append(
        {
            "bin": (bins[i], bins[i + 1]),
            "num_calls": len(_df),
            "spearman": sp,
            "max_Soft_Score": _df["Soft_Score"].max(),
            "min_Soft_Score": _df["Soft_Score"].min(),
            "mean_Soft_Score": _df["Soft_Score"].mean(),
            "med_Soft_Score": _df["Soft_Score"].median(),
            "variance": _df["Soft_Score"].var(),
            "std": _df["Soft_Score"].std(),
        }
    )

fet_res_df = pd.DataFrame(fet_res_bins)
fet_res_df.to_csv("ts_by_fet.tsv", sep="\t", index=False, float_format="%.3f")

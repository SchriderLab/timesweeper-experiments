from argparse import ArgumentParser
from glob import glob
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (auc, confusion_matrix, precision_recall_curve,
                             r2_score, roc_curve)
from tqdm import tqdm
from plot_exp_metrics import plot_confusion_matrix
np.seterr(divide="ignore", invalid="ignore")

agp = ArgumentParser()
agp.add_argument("-i", "--indir", default="simple_sims/better_benchmark/test_benchmark/vcfs/")
agp.add_argument("-o", "--outpre", default="stats")
agp.add_argument("-b", "--num-bins", default=500)
agp.add_argument("-s", "--size", default=5e6)
agp.add_argument("-r", "--reps", default=5000, type=int)

ua = agp.parse_args()

fig, axes = plt.subplots(3)

trues, preds = [], []
sf_clr_thresh = 2.5516360499999995

for swp_idx, swp in enumerate(["neut", "ssv", "sdn"]):
    print("[INFO] Globbing files")
    stat_filelist = [
        f"{ua.indir}/{swp}/{rep}/{rep}_{swp}_stat_methods.csv" for rep in range(ua.reps)
    ]
    sf_filelist = [
        f"{ua.indir}/{swp}/{rep}/{rep}.sf.res" for rep in range(ua.reps)
    ]
    ts_filelist = [
        f"{ua.indir}/{swp}/{rep}/k51_res_aft.csv" for rep in range(ua.reps)
    ]
    ts_dfs = []
    for i in ts_filelist:
        if Path(i).is_file():
            ts_dfs.append(pd.read_csv(i, sep="\t"))

    stat_dfs = []
    for i in stat_filelist:
        if Path(i).is_file():
            stat_dfs.append(pd.read_csv(i))

    sf_dfs = []
    for i in sf_filelist:
        if Path(i).is_file():
            sf_dfs.append(pd.read_csv(i, sep="\t"))

    all_bins = np.arange(0, ua.size + 1, ua.size / ua.num_bins)
    if swp != "neut":
        half_size = int(len(all_bins)/2)
        swp_bin = int(ua.size / 2) + 1
        bins = np.concatenate((all_bins[:half_size+1], [swp_bin], all_bins[half_size+1:]))
    else:
        bins = all_bins
        
    stat_data_shape = (len(stat_dfs), len(bins) - 1)
    sf_data_shape = (len(sf_dfs), len(all_bins) - 1)
    ts_data_shape = (len(ts_dfs), len(bins) - 1)
    
    stat_bin_sizes = np.zeros(stat_data_shape)
    sf_bin_sizes = np.zeros(sf_data_shape)
    ts_bin_sizes = np.zeros(ts_data_shape)
    
    bin_fit = np.zeros(stat_data_shape)
    bin_fet = np.zeros(stat_data_shape)
    bin_sf = np.zeros(sf_data_shape)
    bin_ts = np.zeros(ts_data_shape)

    for idx, df in enumerate(stat_dfs) :
        df["True_Class"] = np.where(df["mut_type"] == 1, "Neut", "Sweep")
        df["FIT_Pred_Class"] = np.where(df["FIT_pval"] < 0.05, "Sweep", "Neut")
        df["FET_Pred_Class"] = np.where(df["FET_pval"] < 0.05, "Sweep", "Neut")
        
        df["Bin"] = pd.cut(df["bp"], bins, labels=bins[1:])

        if swp != "neut":
            df.loc[df["mut_type"] == 2, "Bin"] = swp_bin
        
        stat_bin_sizes[idx] = df.groupby("Bin").count()["True_Class"].values
        bin_fit[idx] += (
            df[df["FIT_Pred_Class"] == "Sweep"]
            .groupby("Bin")
            .count()["FIT_Pred_Class"]
            .values
        )
        bin_fet[idx] += (
            df[df["FET_Pred_Class"] == "Sweep"]
            .groupby("Bin")
            .count()["FET_Pred_Class"]
            .values
        )

    for idx, df in enumerate(sf_dfs) :
        df["SF_Pred_Class"] = np.where(df["LR"] > sf_clr_thresh, "Sweep", "Neut")
        df["Bin"] = pd.cut(df["location"], all_bins, labels=all_bins[1:])
        
        sf_bin_sizes[idx] = df.groupby("Bin").count()["LR"].values

        bin_sf[idx] += (
            df[df["SF_Pred_Class"] == "Sweep"]
            .groupby("Bin")
            .count()["SF_Pred_Class"]
            .values
        )

    for idx, df in enumerate(ts_dfs):
        df["Sweep_Pred"] = np.where(df["Pred_Class"] == "Neut", "Neut", "Sweep")
        df["Bin"] = pd.cut(df["BP"], bins, labels=bins[1:])
        
        if swp != "neut":
            df.loc[df["Mut_Type"] == 2, "Bin"] = swp_bin
            
        ts_bin_sizes[idx] = df.groupby("Bin").count()["Sweep_Pred"].values

        bin_ts[idx] += (
            df[df["Sweep_Pred"] == "Sweep"]
            .groupby("Bin")
            .count()["Pred_Class"]
            .values
        )

    fit_prop = np.nan_to_num(bin_fit / stat_bin_sizes)
    fet_prop = np.nan_to_num(bin_fet / stat_bin_sizes)
    sf_prop = np.nan_to_num(bin_sf / sf_bin_sizes)
    ts_prop = np.nan_to_num(bin_ts / ts_bin_sizes)

    # Plot

    axes[swp_idx].plot(fit_prop.mean(axis=0), label="FIT")
    axes[swp_idx].plot(fet_prop.mean(axis=0), label="FET")
    axes[swp_idx].plot(sf_prop.mean(axis=0), label="Sweepfinder")
    axes[swp_idx].plot(ts_prop.mean(axis=0), label="Timesweeper")


    axes[swp_idx].set_xticks([0, int(ua.num_bins / 2), ua.num_bins])
    axes[swp_idx].set_yscale("log")
    axes[swp_idx].set_ylim((1e-2, 1.1))
    #axes[swp_idx].set_ylim((0, 1))

axes[0].legend(loc="center left", bbox_to_anchor=(1, 0.5))
for i, name in enumerate(["Neutral", "SSV", "SDN"]):
    axes[i].set_ylabel(name)

axes[2].set_xlabel("Bins")

fig.set_size_inches(20, 10)
fig.tight_layout()
plt.savefig(f"{ua.outpre}.pdf")

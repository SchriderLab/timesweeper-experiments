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
agp.add_argument("-o", "--outpre", default="unzoomed")
agp.add_argument("-b", "--num-bins", default=500)
agp.add_argument("-s", "--size", default=5e6)
agp.add_argument("-r", "--reps", default=5000, type=int)

ua = agp.parse_args()

sizes = [1, 3, 11, 51, 101, 201]  # For shoulder testing
fig, axes = plt.subplots(len(sizes), 6)

for size_idx, win_size in tqdm(enumerate(sizes), total=len(sizes)):
    for swp_idx, swp in enumerate(["neut", "ssv", "sdn"]):
        print("[INFO] Globbing files")
        aft_filelist = [
            f"{ua.indir}/{swp}/{rep}/Win_size_{win_size}_aft.csv" for rep in range(ua.reps)
        ]
        hft_filelist = [
            f"{ua.indir}/{swp}/{rep}/Win_size_{win_size}_hft.csv" for rep in range(ua.reps)
        ]

        aft_dfs = []
        for i in aft_filelist:
            if Path(i).is_file():
                aft_dfs.append(pd.read_csv(i, sep="\t"))

        hft_dfs = []
        for i in hft_filelist:
            if Path(i).is_file():
                hft_dfs.append(pd.read_csv(i, sep="\t"))

        all_bins = np.arange(0, ua.size + 1, ua.size / ua.num_bins)
        
        if swp != "neut":
            half_size = int(len(all_bins)/2)
            swp_bin = int(ua.size / 2) + 1
            bins = np.concatenate((all_bins[:half_size+1], [swp_bin], all_bins[half_size+1:]))
        else:
            bins = all_bins
            
        aft_data_shape = (len(aft_dfs), len(bins) - 1)
        aft_bin_sizes = np.zeros(aft_data_shape)
        aft_bin = np.zeros(aft_data_shape)
        aft_prop = np.zeros(aft_data_shape)

        hft_data_shape = (len(hft_dfs), len(bins) - 1)
        hft_bin_sizes = np.zeros(hft_data_shape)
        hft_bin = np.zeros(hft_data_shape)
        hft_prop = np.zeros(hft_data_shape)


        for idx, df in enumerate(aft_dfs) :
            df["Sweep_Pred"] = np.where(df["Pred_Class"] == "neut", "Neut", "Sweep")
            df["Bin"] = pd.cut(df["BP"], bins, labels=bins[1:])

            if swp != "neut":
                df.loc[df["Mut_Type"] == 2, "Bin"] = swp_bin
            
            aft_bin_sizes[idx] = df.groupby("Bin").count()["Sweep_Pred"].values
            aft_bin[idx] += (
                df[df["Sweep_Pred"] == "Sweep"]
                .groupby("Bin")
                .count()["Pred_Class"]
                .values
            )


        aft_prop = np.nan_to_num(aft_bin / aft_bin_sizes)

        for idx, df in enumerate(hft_dfs):
            df["Sweep_Pred"] = np.where(df["Pred_Class"] == "neut", "Neut", "Sweep")
            df["Bin"] = pd.cut(df["BP"], bins, labels=bins[1:])

            if swp != "neut":
                df.loc[df["Mut_Type"] == 2, "Bin"] = swp_bin
            
            hft_bin_sizes[idx] = df.groupby("Bin").count()["Sweep_Pred"].values
            hft_bin[idx] += (
                df[df["Sweep_Pred"] == "Sweep"]
                .groupby("Bin")
                .count()["Pred_Class"]
                .values
            )

        hft_prop = np.nan_to_num(hft_bin / hft_bin_sizes)

        # Plot
        axes[size_idx, swp_idx].plot(aft_prop.mean(axis=0)[10:-10], label="Neut")

        axes[size_idx, swp_idx + 3].plot(hft_prop.mean(axis=0)[10:-10], label="Neut")

        axes[size_idx, swp_idx].set_xticks([0, int(ua.num_bins / 2), ua.num_bins])
        axes[size_idx, swp_idx + 3].set_xticks([0, int(ua.num_bins / 2), ua.num_bins])

        axes[size_idx, swp_idx].set_yscale("log")
        axes[size_idx, swp_idx+3].set_yscale("log")
        
        axes[size_idx, swp_idx].set_ylim((1e-2, 1.1))
        axes[size_idx, swp_idx+3].set_ylim((1e-2, 1.1))

axes[0, -1].legend(loc="center left", bbox_to_anchor=(1, 0.5))

cols = [f"{i} {j}" for i in ["AFT", "HFT"] for j in ["Neut", "SSV", "SDN"]]
rows = [f"l={i}" for i in sizes]

for ax, col in zip(axes[0], cols):
    ax.set_title(col)

for ax, row in zip(axes[:, 0], rows):
    ax.set_ylabel(row, loc="center")

fig.set_size_inches(20, 10)
fig.tight_layout()
plt.savefig(f"{ua.outpre}.pdf")

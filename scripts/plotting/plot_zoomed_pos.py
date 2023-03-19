import warnings
from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

warnings.simplefilter(action="ignore")

np.seterr(divide="ignore", invalid="ignore")

agp = ArgumentParser()
agp.add_argument("-i", "--indir", default="simple_sims/better_benchmark/test_benchmark/vcfs/")
agp.add_argument("-o", "--outpre", default="zoomed")
agp.add_argument("-n", "--num-flank-snps", default=250, type=int)
agp.add_argument("-r", "--reps", default=5000, type=int)

ua = agp.parse_args()

sizes = [1, 3, 11, 51, 101]  # For shoulder testing
fig, axes = plt.subplots(len(sizes), 6)

for size_idx, win_size in tqdm(enumerate(sizes), total=len(sizes)):
    for swp_idx, swp in enumerate(["Neut", "SSV", "SDN"]):
        print("[INFO] Globbing files")
        aft_filelist = [
            f"{ua.indir}/{swp.lower()}/{rep}/k{win_size}_res_aft.csv" for rep in range(ua.reps)
        ]
        hft_filelist = [
            f"{ua.indir}/{swp.lower()}/{rep}/k{win_size}_res_hft.csv" for rep in range(ua.reps)
        ]

        aft_dfs = []
        for i in tqdm(aft_filelist, desc="Loading AFT files"):
            if Path(i).is_file():
                df = pd.read_csv(i, sep="\t")
                if swp != "Neut":
                    if len(df["Mut_Type"].unique()) > 1:
                        if (len(df) > 0) and ("Pred_Class" in df.columns):
                            aft_dfs.append(df)
                else:
                   if (len(df) > 0) and ("Pred_Class" in df.columns):
                        aft_dfs.append(df) 

        hft_dfs = []
        for i in tqdm(hft_filelist, desc="Loading HFT files"):
            if Path(i).is_file():
                df = pd.read_csv(i, sep="\t")
                if swp != "Neut":
                    if len(df["Mut_Type"].unique()) > 1:
                        if (len(df) > 0) and ("Pred_Class" in df.columns):
                            hft_dfs.append(df)
                else:
                   if (len(df) > 0) and ("Pred_Class" in df.columns):
                        hft_dfs.append(df) 
                        
        aft_data_shape = (len(aft_dfs), ua.num_flank_snps*2+1)
        aft_bin_neut = np.zeros(aft_data_shape)
        aft_bin_ssv = np.zeros(aft_data_shape)
        aft_bin_sdn = np.zeros(aft_data_shape)
        aft_neut_prop = np.zeros(aft_data_shape)
        aft_ssv_prop = np.zeros(aft_data_shape)
        aft_sdn_prop = np.zeros(aft_data_shape)

        hft_data_shape = (len(hft_dfs), ua.num_flank_snps*2+1)
        hft_bin_neut = np.zeros(hft_data_shape)
        hft_bin_ssv = np.zeros(hft_data_shape)
        hft_bin_sdn = np.zeros(hft_data_shape)
        hft_neut_prop = np.zeros(hft_data_shape)
        hft_ssv_prop = np.zeros(hft_data_shape)
        hft_sdn_prop = np.zeros(hft_data_shape)

        for idx, df in enumerate(aft_dfs):
            if swp != "Neut":
                swp_loc = df[df["Mut_Type"] == 2].index[0]
            else:
                swp_loc = int(len(df)/2)
                
            df = df.loc[(swp_loc - ua.num_flank_snps) : (swp_loc + ua.num_flank_snps), :]

            aft_bin_neut[idx] += np.where(df["Pred_Class"] == "Neut", 1, 0)
            aft_bin_ssv[idx] += np.where(df["Pred_Class"] == "SSV", 1, 0)
            aft_bin_sdn[idx] += np.where(df["Pred_Class"] == "SDN", 1, 0)

        aft_neut_prop = np.sum(aft_bin_neut, axis=0) / aft_bin_neut.shape[0]
        aft_ssv_prop = np.sum(aft_bin_ssv, axis=0) / aft_bin_ssv.shape[0]
        aft_sdn_prop = np.sum(aft_bin_sdn, axis=0) / aft_bin_sdn.shape[0]

        for idx, df in enumerate(hft_dfs):
            if swp != "Neut":
                swp_loc = df[df["Mut_Type"] == 2].index[0]
            else:
                swp_loc = int(len(df)/2)
                
            df = df.loc[(swp_loc - ua.num_flank_snps) : (swp_loc + ua.num_flank_snps), :]

            hft_bin_neut[idx] += np.where(df["Pred_Class"] == "Neut", 1, 0)
            hft_bin_ssv[idx] += np.where(df["Pred_Class"] == "SSV", 1, 0)
            hft_bin_sdn[idx] += np.where(df["Pred_Class"] == "SDN", 1, 0)


        hft_neut_prop = np.sum(hft_bin_neut, axis=0) / hft_bin_neut.shape[0]
        hft_ssv_prop = np.sum(hft_bin_ssv, axis=0) / hft_bin_ssv.shape[0]
        hft_sdn_prop = np.sum(hft_bin_sdn, axis=0) / hft_bin_sdn.shape[0]

        # Plot
        axes[size_idx, swp_idx].plot(1 - aft_neut_prop, label="Sweep")

        axes[size_idx, swp_idx + 3].plot(1 - hft_neut_prop, label="Sweep")

        #axes[size_idx, swp_idx].set_xticks([0, int(ua.num_flank_snps / 2), ua.num_flank_snps])
        #axes[size_idx, swp_idx + 3].set_xticks([0, int(ua.num_flank_snps / 2), ua.num_flank_snps])
        
        axes[size_idx, swp_idx].set_yscale("log")
        axes[size_idx, swp_idx+3].set_yscale("log")
        
        axes[size_idx, swp_idx].set_ylim((1e-2, 1))
        axes[size_idx, swp_idx+3].set_ylim((1e-2, 1))

axes[0, -1].legend(loc="center left", bbox_to_anchor=(1, 0.5))

cols = [f"{i} {j}" for i in ["AFT", "HFT"] for j in ["Neut", "SSV", "SDN"]]
rows = [f"k{i}" for i in sizes]

for ax, col in zip(axes[0], cols):
    ax.set_title(col)

for ax, row in zip(axes[:, 0], rows):
    ax.set_ylabel(row, loc="center")

fig.set_size_inches(30, 10)
fig.tight_layout()
plt.savefig(f"{ua.outpre}.pdf")

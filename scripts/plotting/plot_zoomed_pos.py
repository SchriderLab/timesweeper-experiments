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

sizes = [1, 3, 11, 51, 101, 201]  # For shoulder testing
fig, axes = plt.subplots(len(sizes), 6)

for size_idx, win_size in enumerate(sizes):
    for swp_idx, swp in enumerate(["Neut", "SSV", "SDN"]):
        aft_filelist = [
            f"{ua.indir}/{swp.lower()}/{rep}/Win_size_{win_size}_aft.csv" for rep in range(ua.reps)
        ]
        hft_filelist = [
            f"{ua.indir}/{swp.lower()}/{rep}/Win_size_{win_size}_hft.csv" for rep in range(ua.reps)
        ]

        aft_dfs = []
        for i in aft_filelist:
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
        for i in hft_filelist:
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
        aft_bin = np.zeros(aft_data_shape)
        aft_prop = np.zeros(aft_data_shape)

        hft_data_shape = (len(hft_dfs), ua.num_flank_snps*2+1)
        hft_bin = np.zeros(hft_data_shape)
        hft_prop = np.zeros(hft_data_shape)

        for idx, df in enumerate(aft_dfs):

            if swp != "Neut":
                swp_loc = df[df["Mut_Type"] == 2].index[0]
            else:
                swp_loc = int(len(df)/2)
                
            df = df.loc[(swp_loc - ua.num_flank_snps) : (swp_loc + ua.num_flank_snps), :]

            aft_bin[idx] += np.where(df["Pred_Class"] == "neut", 0, 1)

        aft_prop = np.sum(aft_bin, axis=0) / aft_bin.shape[0]

        for idx, df in enumerate(hft_dfs):
            if swp != "Neut":
                swp_loc = df[df["Mut_Type"] == 2].index[0]
            else:
                swp_loc = int(len(df)/2)
                
            df = df.loc[(swp_loc - ua.num_flank_snps) : (swp_loc + ua.num_flank_snps), :]

            hft_bin[idx] += np.where(df["Pred_Class"] == "neut", 0, 1)

        hft_prop = np.sum(hft_bin, axis=0) / hft_bin.shape[0]

        print(win_size, swp, np.mean(np.sum(aft_bin, axis=1)))

        # Plot
        axes[size_idx, swp_idx].plot(aft_prop, label="Sweep")

        axes[size_idx, swp_idx + 3].plot(hft_prop, label="Sweep")
        
        axes[size_idx, swp_idx].set_xticks([0, ua.num_flank_snps, 2*ua.num_flank_snps])
        axes[size_idx, swp_idx+3].set_xticks([0, ua.num_flank_snps, 2*ua.num_flank_snps])

        axes[size_idx, swp_idx].set_yscale("log")
        axes[size_idx, swp_idx+3].set_yscale("log")
        
        axes[size_idx, swp_idx].set_ylim((1e-2, 1))
        axes[size_idx, swp_idx+3].set_ylim((1e-2, 1))

axes[0, -1].legend(loc="center left", bbox_to_anchor=(1, 0.5))

cols = [f"{i} {j}" for i in ["AFT", "HFT"] for j in ["Neut", "SSV", "SDN"]]
rows = [f"l={i}" for i in sizes]

for ax, col in zip(axes[0], cols):
    ax.set_title(col)

for ax, row in zip(axes[:, 0], rows):
    ax.set_ylabel(row, loc="center")

fig.set_size_inches(30, 10)
fig.tight_layout()
plt.savefig(f"{ua.outpre}.pdf")

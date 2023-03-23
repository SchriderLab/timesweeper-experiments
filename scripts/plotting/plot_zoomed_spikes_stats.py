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
import warnings
warnings.filterwarnings('ignore')
np.seterr(divide="ignore", invalid="ignore")

agp = ArgumentParser()
agp.add_argument("-i", "--indir", default="simple_sims/better_benchmark/test_benchmark/vcfs/")
agp.add_argument("-o", "--outpre", default="zoomed_stats")
agp.add_argument("-n", "--num-flank-snps", default=250, type=int)
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
        
    stat_data_shape = (len(stat_dfs), ua.num_flank_snps*2+1)
    sf_data_shape = (len(sf_dfs), ua.num_flank_snps*2+1)
    ts_data_shape = (len(ts_dfs), ua.num_flank_snps*2+1)
    
    stat_bin_sizes = np.zeros(stat_data_shape)
    sf_bin_sizes = np.zeros(sf_data_shape)
    ts_bin_sizes = np.zeros(ts_data_shape)
    
    bin_fit = np.zeros(stat_data_shape)
    bin_fet = np.zeros(stat_data_shape)
    bin_sf = np.zeros(sf_data_shape)
    bin_ts = np.zeros(ts_data_shape)
        
    for idx, df in enumerate(stat_dfs):
        try:
            if swp != "neut":
                swp_loc = df[df["mut_type"] == 2].index[0]
            else:
                swp_loc = int(len(df)/2)
        except:
            continue
        
        df = df.loc[(swp_loc - ua.num_flank_snps) : (swp_loc + ua.num_flank_snps), :]

        df["True_Class"] = np.where(df["mut_type"] == 1, "Neut", "Sweep")
        df["FIT_Pred_Class"] = np.where(df["FIT_pval"] < 0.05, "Sweep", "Neut")
        df["FET_Pred_Class"] = np.where(df["FET_pval"] < 0.05, "Sweep", "Neut")
        
        bin_fit[idx] += np.where(df["FIT_Pred_Class"] == "Neut", 0, 1)
        bin_fet[idx] += np.where(df["FET_Pred_Class"] == "Neut", 0, 1)

    fit_prop = np.sum(bin_fit, axis=0) / bin_fit.shape[0]
    fet_prop = np.sum(bin_fet, axis=0) / bin_fet.shape[0]

    for idx, df in enumerate(sf_dfs) :
        swp_loc = int(len(df)/2)
        
        df = df.loc[(swp_loc - ua.num_flank_snps) : (swp_loc + ua.num_flank_snps), :]
        
        df["SF_Pred_Class"] = np.where(df["LR"] > sf_clr_thresh, "Sweep", "Neut")
        
        bin_sf[idx] += np.where(df["SF_Pred_Class"] == "Neut", 0, 1)

    sf_prop = np.sum(bin_sf, axis=0) / bin_sf.shape[0]

    for idx, df in enumerate(ts_dfs):
        try:
            if swp != "neut":
                swp_loc = df[df["Mut_Type"] == 2].index[0]
            else:
                swp_loc = int(len(df)/2)
        except:
            continue
        
        df = df.loc[(swp_loc - ua.num_flank_snps) : (swp_loc + ua.num_flank_snps), :]

        df["Sweep_Pred"] = np.where(df["Pred_Class"] == "Neut", "Neut", "Sweep")
        
        bin_ts[idx] += np.where(df["Sweep_Pred"] == "Neut", 0, 1)

    ts_prop = np.sum(bin_ts, axis=0) / bin_ts.shape[0]
    
    print(swp.upper())
    if swp == "neut":
        print("TS positives:", (np.sum(np.sum(bin_ts, axis=1))) / bin_ts.shape[0])
        print("FIT positives:", (np.sum(np.sum(bin_fit, axis=1))) / bin_ts.shape[0])
        print("FET positives:", (np.sum(np.sum(bin_fet, axis=1))) / bin_ts.shape[0])
    else:
        print("TS positives:", (np.sum(np.sum(bin_ts, axis=1)) - bin_ts.shape[0]) / bin_ts.shape[0])
        print("FIT positives:", (np.sum(np.sum(bin_fit, axis=1)) - bin_fit.shape[0]) / bin_ts.shape[0])
        print("FET positives:", (np.sum(np.sum(bin_fet, axis=1)) - bin_fet.shape[0]) / bin_ts.shape[0])

    # Plot

    axes[swp_idx].plot(fit_prop, label="FIT")
    axes[swp_idx].plot(fet_prop, label="FET")
    axes[swp_idx].plot(sf_prop, label="Sweepfinder")
    axes[swp_idx].plot(ts_prop, label="Timesweeper")


    axes[swp_idx].set_xticks([0, int(ua.num_flank_snps / 2), ua.num_flank_snps])
    axes[swp_idx].set_yscale("log")
    axes[swp_idx].set_ylim((1e-2, 1.1))
    #axes[swp_idx].set_ylim((0, 1))

axes[0].legend(loc="center left", bbox_to_anchor=(1, 0.5))
for i, name in enumerate(["Neutral", "SSV", "SDN"]):
    axes[i].set_ylabel(name)

axes[2].set_xlabel("Polymorphisms")

fig.set_size_inches(20, 10)
fig.tight_layout()
plt.savefig(f"{ua.outpre}.pdf")

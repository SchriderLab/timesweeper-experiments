import itertools
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (auc, confusion_matrix, precision_recall_curve,
                             r2_score, roc_curve)

plt.rcParams["font.size"] = "16"
plt.rcParams["figure.figsize"] = (8, 8)


def plot_confusion_matrix(
    working_dir, cm, target_names, title="Confusion matrix", cmap=None, normalize=False
):
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap("Blues")

    outfile = title
    title = title.split("_Timesweeper")[0] + " Confusion Matrix"

    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(
                j,
                i,
                f"{cm[i, j]:0.4f}",
                horizontalalignment="center",
                color="black",
                # color="white" if cm[i, j] > thresh else "black",
            )
        else:
            plt.text(
                j,
                i,
                f"{cm[i, j]:,}",
                horizontalalignment="center",
                color="black",
                # color="white" if cm[i, j] > thresh else "black",
            )

    plt.ylabel("sweep label")
    plt.xlabel(f"Predicted label\naccuracy={accuracy:0.4f}; misclass={misclass:0.4f}")
    plt.savefig(os.path.join(working_dir, outfile + ".png"))
    plt.clf()

def plot_roc(data):
    """Plot ROC curve by binarizing neutral/sweep."""

    # Plot sdn/ssv distinction
    sweep_idxs = np.transpose(np.array((data["int_swp"] > 0)).nonzero())
    sweep_labs = np.array(data["int_swp"])[sweep_idxs]

    sdn_probs = data[data["int_swp"] > 0]["sdn_prob"]

    swp_fpr, swp_tpr, thresh = roc_curve(sweep_labs, sdn_probs, pos_label=2)
    swp_auc_val = auc(swp_fpr, swp_tpr)

    # Coerce all ssvs into sweep binary pred
    labs = np.array(data["int_swp"])
    labs[labs > 1] = 1
    pred_probs = np.sum(np.array([data["sdn_prob"], data["ssv_prob"]]).T, axis=1)

    # Plot ROC Curve
    fpr, tpr, thresh = roc_curve(labs, pred_probs)
    auc_val = auc(fpr, tpr)
    
    return swp_fpr, swp_tpr, swp_auc_val, fpr, tpr, auc_val

def plot_prec_recall(data):
    """Plot PR curve by binarizing neutral/sweep."""
    # Plot sdn/ssv distinction

    filt_data = data[(data["sdn_prob"] > 0.0) & (data["ssv_prob"] > 0.0)]

    sweep_idxs = np.transpose(np.array((filt_data["int_swp"] > 0)).nonzero())
    sweep_labs = np.array(filt_data["int_swp"])[sweep_idxs]

    # TODO FIX THIS: divide score of sweep by summed sweep prob
    # TODO FIlter out where probs of both prob are 0
    if len(np.unique(filt_data["int_swp"])) > 2:
        sdn_probs = filt_data[filt_data["int_swp"] > 0]["sdn_prob"] / (
            filt_data[filt_data["int_swp"] > 0]["sdn_prob"]
            + filt_data[filt_data["int_swp"] > 0]["ssv_prob"]
        )

        swp_prec, swp_rec, swp_thresh = precision_recall_curve(
            sweep_labs.flatten(), sdn_probs, pos_label=2
        )
        swp_auc_val = auc(swp_rec, swp_prec)


    # Coerce all ssvs into sweep binary pred
    labs = np.array(data["int_swp"])
    labs[labs > 1] = 1
    pred_probs = np.sum(np.array([data["sdn_prob"], data["ssv_prob"]]).T, axis=1)
    

    # Plot PR Curve for binarized labs
    prec, rec, thresh = precision_recall_curve(labs, pred_probs)
    auc_val = auc(rec, prec)
    
    return swp_prec, swp_rec, swp_auc_val, prec, rec, auc_val


def main():
    lab_dict = {"neut": 0, "ssv": 1, "sdn": 2}
    dict_lab = {v:k for k,v in lab_dict.items()}
    scenarios = ["Constant", "Bottleneck", "OoA"]
    for d_type in ["aft", "hft"]:
        res_dict = {}
        r_fig, r_axes = plt.subplots(len(scenarios), len(scenarios))
        p_fig, p_axes = plt.subplots(len(scenarios), len(scenarios))
        sdn_fig, sdn_axes = plt.subplots(len(scenarios), len(scenarios))
        ssv_fig, ssv_axes = plt.subplots(len(scenarios), len(scenarios))

        for r_idx, s1 in enumerate(scenarios):
            for c_idx, s2 in enumerate(scenarios):
                df = pd.read_csv(f"results/data/{s1.lower()}_on_{s2.lower()}_{d_type}.csv")
                df["pred"] = [dict_lab[i] for i in df["pred_sweep"].values]
                df["int_swp"] = [lab_dict[i] for i in df["sweep"].values]
                name = f"{s1}_on_{s2}"
                res_dict[name] = {}
                
                conf_mat = confusion_matrix(df["sweep"], df["pred"])
                plot_confusion_matrix(
                    "results/figs/confmats",
                    conf_mat,
                    [i.upper() for i in lab_dict.keys()],
                    title=name,
                    normalize=True,
                )
                
                swp_fpr, swp_tpr, roc_swp_auc, fpr, tpr, roc_auc = plot_roc(df)
                swp_prec, swp_rec, pr_swp_auc, prec, rec, pr_auc = plot_prec_recall(df)
                
                res_dict[name]["sweep_roc_auc"] = roc_swp_auc
                res_dict[name]["roc_auc"] = roc_auc
                res_dict[name]["sweep_pr_auc"] = pr_swp_auc
                res_dict[name]["pr_auc"] = pr_auc               
                
                r_axes[r_idx, c_idx].plot(fpr, tpr, label=f"Neutral vs Sweep")
                r_axes[r_idx, c_idx].plot(swp_fpr, swp_tpr, label=f"SDN vs SSV")

                p_axes[r_idx, c_idx].plot(prec, rec, label=f"Neutral vs Sweep")
                p_axes[r_idx, c_idx].plot(swp_prec, swp_rec, label=f"SDN vs SSV")
                
                ssv_df = df[df["sweep"] == "ssv"]
                ssv_axes[r_idx, c_idx].scatter(
                    ssv_df["s_val"], ssv_df["ssv_sval"]
                )
                ssv_r2 = np.round(r2_score(ssv_df["s_val"], ssv_df["ssv_sval"]), 2)
                ssv_axes[r_idx, c_idx].annotate(
                    f"""r^2: {ssv_r2}""",
                    (0.05, 0.0),
                )
                
                sdn_df = df[df["sweep"] == "sdn"]
                sdn_axes[r_idx, c_idx].scatter(
                    sdn_df["s_val"], sdn_df["sdn_sval"]
                )
                sdn_r2 = np.round(r2_score(sdn_df["s_val"], sdn_df["sdn_sval"]), 2)
                sdn_axes[r_idx, c_idx].annotate(
                    f"""r^2: {sdn_r2}""",
                    (0.05, 0.27),
                )     
                
                res_dict[name]["ssv_r2"] = ssv_r2
                res_dict[name]["sdn_r2"] = sdn_r2
                           
        r_axes[2, 1].legend(loc="lower center", bbox_to_anchor=(.5, -1))

        p_axes[-1, 1].legend(loc="lower center", bbox_to_anchor=(1, 0.5))

        for a in [r_axes, p_axes, sdn_axes, ssv_axes]:
            for ax, col in zip(a[0], scenarios):
                ax.set_title(col)

            for ax, row in zip(a[:, 0], scenarios):
                ax.set_ylabel(row, loc="center")
                
        r_fig.supxlabel("Trained On")
        r_fig.supylabel("Tested On")
        r_fig.suptitle("ROC Curves")
        r_fig.tight_layout()

        
        p_fig.savefig(f"results/figs/prec_recall_{d_type}.png", bbox_inches="tight")
        r_fig.savefig(f"results/figs/roc_{d_type}.png", bbox_inches="tight")
        sdn_fig.savefig(f"results/figs/sdn_selcoeffs_{d_type}.png")
        ssv_fig.savefig(f"results/figs/ssv_selcoeffs_{d_type}.png")
        
        pd.DataFrame(res_dict).to_csv(f"results/misspec_{d_type}_res.tsv", sep="\t")
        
if __name__ == "__main__":
    main()
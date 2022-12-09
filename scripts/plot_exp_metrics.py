import argparse
import os
from glob import glob
from pathlib import Path
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, precision_recall_curve, auc

# Adapt the single-plots from plotting.plotting_utils to iteratively plot curves
def plot_roc(datums, schema, outdir):
    """Plot ROC curve by binarizing neutral/sweep."""

    for name, data in datums.items():
        # Plot sdn/ssv distinction
        sweep_idxs = np.transpose(np.array((data["true"] > 0)).nonzero())
        sweep_labs = np.array(data["true"])[sweep_idxs]

        # sweep_labs[sweep_labs == 1] = 0
        # sweep_labs[sweep_labs == 2] = 1

        """
        if len(np.unique(data["true"])) > 2:
            ssv_probs = data["ssv_scores"]

            swp_fpr, swp_tpr, thresh = roc_curve(sweep_labs, ssv_probs)
            swp_auc_val = auc(swp_fpr, swp_tpr)
            plt.plot(
                swp_fpr,
                swp_tpr,
                label=f"{name.capitalize()} SDN vs SSV: {swp_auc_val:.4}",
            )
        """

        # Coerce all ssvs into sweep binary pred
        labs = np.array(data["true"])
        labs[labs > 1] = 1
        pred_probs = np.sum(
            np.array([data["sdn_scores"], data["ssv_scores"]]).T, axis=1
        )

        # Plot ROC Curve
        fpr, tpr, thresh = roc_curve(labs, pred_probs)
        auc_val = auc(fpr, tpr)
        plt.plot(
            fpr, tpr, label=f"{name.capitalize()} Neutral vs Sweep AUC: {auc_val:.2}"
        )

    plt.title(f"ROC Curve {schema}")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.legend()
    plt.savefig(f"{outdir}/{schema.replace(' ', '_')}_roc_curve.pdf")
    plt.clf()


def plot_prec_recall(datums, schema, outdir):
    """Plot PR curve by binarizing neutral/sweep."""
    for name, data in datums.items():

        # Plot sdn/ssv distinction
        sweep_idxs = np.transpose(np.array((data["true"] > 0)).nonzero())
        sweep_labs = np.array(data["true"])[sweep_idxs]

        sweep_labs[sweep_labs == 1] = 0
        sweep_labs[sweep_labs == 2] = 1

        """
        if len(np.unique(data["true"])) > 2:
            ssv_probs = data[data["true"] > 0]["ssv_scores"]

            swp_prec, swp_rec, swp_thresh = precision_recall_curve(
                sweep_labs.flatten(), ssv_probs
            )
            swp_auc_val = auc(swp_rec, swp_prec)
            plt.plot(swp_rec, swp_prec, label=f"{name.capitalize()} SDN vs SSV AUC: {swp_auc_val:.2}")
        """

        # Coerce all ssvs into sweep binary pred
        labs = np.array(data["true"])
        labs[labs > 1] = 1
        pred_probs = np.sum(
            np.array([data["sdn_scores"], data["ssv_scores"]]).T, axis=1
        )

        # Plot PR Curve for binarized labs
        prec, rec, thresh = precision_recall_curve(labs, pred_probs)
        auc_val = auc(rec, prec)
        plt.plot(
            rec, prec, label=f"{name.capitalize()} Neutral vs Sweep AUC: {auc_val:.2}"
        )

    plt.title(f"PR Curve {schema}")
    plt.legend()
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.savefig(f"{outdir}/{schema.replace(' ', '_')}_pr_curve.pdf")
    plt.clf()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-id",
        "--in-dir",
        dest="in_dir",
        required=True,
        type=Path,
        help="Directory of experiments to glob through.",
    )
    ap.add_argument(
        "-n",
        "--name",
        dest="exp_name",
        required=True,
        type=str,
        help="Name of experiment set. Used in figure labeling.",
    )
    ap.add_argument(
        "-o",
        "--output-dir",
        dest="outdir",
        required=True,
        type=Path,
        help="Path to write .pdf files to write as plot.",
    )
    args = ap.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    # Glob in testing predictions
    datums = {}
    for t_file in glob(
        os.path.join(
            args.in_dir,
            "*",
            "*",
            "test_predictions",
            "*Timesweeper_aft_test_predictions.csv",
        ),
        recursive=True,
    ):
        run_name = re.split(r"_[tT]imesweeper", os.path.split(t_file)[1])[0]
        print(run_name)
        data = pd.read_csv(t_file, header=0)
        datums[run_name] = data

    plot_roc(datums, args.exp_name, args.outdir)
    plot_prec_recall(datums, args.exp_name, args.outdir)


if __name__ == "__main__":
    main()

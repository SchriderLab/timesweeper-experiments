import argparse
import itertools
import os
import re
from glob import glob
from pathlib import Path
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    auc,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
    r2_score,
)

plt.rcParams["font.size"] = "16"
plt.rcParams["figure.figsize"] = (8, 8)


def plot_sel_coeff_preds(data, dtype, name, outdir, scenarios):
    """Plot s predictions against true value, color by scenario."""
    if "ssv" in name:
        true_class = "ssv"
    elif "sdn" in name:
        true_class = "sdn"

    plt.scatter(
        data["true_sel_coeff"], data["pred_sel_coeff"], label=true_class.upper()
    )
    plt.annotate(
        f"""r^2 of {true_class.upper()}: {np.round(r2_score(data["true_sel_coeff"], data["pred_sel_coeff"]), 2)}""",
        (0.05, 0.27),
    )

    plt.legend()
    plt.xlim((0, 0.3))
    plt.ylim((0, 0.3))
    plt.title(f"{name} \n Predicted vs True Selection Coefficients")
    plt.ylabel("Predicted S")
    plt.xlabel("True S")

    plt.savefig(
        f"{outdir}/{name.replace(' ', '_')}_Timesweeper_Reg_{dtype}_selcoeffs.pdf"
    )
    plt.savefig(
        f"{outdir}/{name.replace(' ', '_')}_Timesweeper_Reg_{dtype}_selcoeffs.png"
    )
    plt.clf()


def plot_confusion_matrix(
    working_dir, cm, target_names, title="Confusion matrix", cmap=None, normalize=False
):
    """
    Given a sklearn confusion matrix (cm), make a nice plot.

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """

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

    plt.ylabel("True label")
    plt.xlabel(f"Predicted label\naccuracy={accuracy:0.4f}; misclass={misclass:0.4f}")
    plt.savefig(os.path.join(working_dir, outfile + ".pdf"))
    plt.savefig(os.path.join(working_dir, outfile + ".png"))
    plt.clf()


# Adapt the single-plots from plotting.plotting_utils to iteratively plot curves
def plot_roc(name, data, dtype, outdir):
    """Plot ROC curve by binarizing neutral/sweep."""

    # Plot sdn/ssv distinction
    sweep_idxs = np.transpose(np.array((data["true"] > 0)).nonzero())
    sweep_labs = np.array(data["true"])[sweep_idxs]

    sdn_probs = data[data["true"] > 0]["sdn_prob"]

    swp_fpr, swp_tpr, thresh = roc_curve(sweep_labs, sdn_probs, pos_label=2)
    swp_auc_val = auc(swp_fpr, swp_tpr)
    plt.plot(
        swp_fpr,
        swp_tpr,
        label=f"{name.split('_')[0].capitalize()} SDN vs SSV: {swp_auc_val:.4}",
    )

    # Coerce all ssvs into sweep binary pred
    labs = np.array(data["true"])
    labs[labs > 1] = 1
    pred_probs = np.sum(np.array([data["sdn_prob"], data["ssv_prob"]]).T, axis=1)

    # Plot ROC Curve
    fpr, tpr, thresh = roc_curve(labs, pred_probs)
    auc_val = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{name.split('_')[0].capitalize()} Neutral vs Sweep AUC: {auc_val:.2}")
    
    plt.ylim((0,1.1))
    plt.xlim((0,1.1))
    plt.title(f"ROC Curve {name.split('_')[0]}")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.legend()
    plt.savefig(f"{outdir}/{name.replace(' ', '_')}_Timesweeper_Class_{dtype}_roc.pdf")
    plt.savefig(f"{outdir}/{name.replace(' ', '_')}_Timesweeper_Class_{dtype}_roc.png")
    plt.clf()


def plot_prec_recall(name, data, dtype, outdir):
    """Plot PR curve by binarizing neutral/sweep."""
    # Plot sdn/ssv distinction

    filt_data = data[(data["sdn_prob"] > 0.0) & (data["ssv_prob"] > 0.0)]

    sweep_idxs = np.transpose(np.array((filt_data["true"] > 0)).nonzero())
    sweep_labs = np.array(filt_data["true"])[sweep_idxs]

    # TODO FIX THIS: divide score of sweep by summed sweep prob
    # TODO FIlter out where probs of both prob are 0
    if len(np.unique(filt_data["true"])) > 2:
        sdn_probs = filt_data[filt_data["true"] > 0]["sdn_prob"] / (
            filt_data[filt_data["true"] > 0]["sdn_prob"]
            + filt_data[filt_data["true"] > 0]["ssv_prob"]
        )

        swp_prec, swp_rec, swp_thresh = precision_recall_curve(
            sweep_labs.flatten(), sdn_probs, pos_label=2
        )
        swp_auc_val = auc(swp_rec, swp_prec)
        plt.plot(
            swp_rec,
            swp_prec,
            label=f"{name.split('_')[0].capitalize()} SDN vs SSV AUC: {swp_auc_val:.2}",
        )

    # Coerce all ssvs into sweep binary pred
    labs = np.array(data["true"])
    labs[labs > 1] = 1
    pred_probs = np.sum(np.array([data["sdn_prob"], data["ssv_prob"]]).T, axis=1)

    # Plot PR Curve for binarized labs
    prec, rec, thresh = precision_recall_curve(labs, pred_probs)
    auc_val = auc(rec, prec)
    plt.plot(rec, prec, label=f"{name.split('_')[0].capitalize()} Neutral vs Sweep AUC: {auc_val:.2}")

    plt.title(f"PR Curve {name}")
    plt.legend()
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.ylim((0,1.1))
    plt.xlim((0,1.1))
    plt.savefig(f"{outdir}/{name.replace(' ', '_')}_Timesweeper_Class_{dtype}_pr.pdf")
    plt.savefig(f"{outdir}/{name.replace(' ', '_')}_Timesweeper_Class_{dtype}_pr.png")
    plt.clf()


def get_ua():
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
        "-o",
        "--output-dir",
        dest="outdir",
        required=True,
        type=Path,
        help="Path to write image files to write as plot.",
    )
    args = ap.parse_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    return args


def main():
    ua = get_ua()

    lab_conv = {"neut": 0, "ssv": 1, "sdn": 2}

    for dtype in ["aft", "hft"]:
        datums = {}
        for t_file in glob(
            os.path.join(
                ua.in_dir,
                "*",
                "test_predictions",
                f"*{dtype}*class_test_predictions.csv",
            ),
            recursive=True,
        ):
            run_name = re.split(r"_[tT]imesweeper", os.path.split(t_file)[1])[0].split("_Training")[0]
            if "2D" in run_name:
                run_name = run_name.split("_2DTimesweeper")[0]
            elif "Big_" in run_name:
                run_name.replace("Big_", "")

            data = pd.read_csv(t_file, header=0)
            data.true = [lab_conv[i] for i in data.true]
            data.pred = [lab_conv[i] for i in data.pred]
            datums[run_name] = data

        for (name, data) in datums.items():
            plot_roc(name, data, dtype, ua.outdir)
            plot_prec_recall(name, data, dtype, ua.outdir)

            conf_mat = confusion_matrix(data["true"], data["pred"])
            plot_confusion_matrix(
                ua.outdir,
                conf_mat,
                ["Neutral", "SSV", "SDN"],
                title=f"{name}_Timesweeper_Class_{dtype}_confmat_normed",
                normalize=True,
            )
            plot_confusion_matrix(
                ua.outdir,
                conf_mat,
                ["Neutral", "SSV", "SDN"],
                title=f"{name}_Timesweeper_Class_{dtype}_confmat_unnormed",
                normalize=False,
            )

        datums = {}
        for t_file in glob(
            os.path.join(
                ua.in_dir,
                #"*",
                "test_predictions",
                f"*_{dtype}_selcoeff_test_predictions.csv",
            ),
            recursive=True,
        ):
            run_name = re.split(r"_[tT]imesweeper", os.path.split(t_file)[1])[0]
            if "2D" in run_name:
                run_name = run_name.split("_2DTimesweeper")[0]
            elif "Big_" in run_name:
                run_name = run_name.replace("Big_", "")

            data = pd.read_csv(t_file, header=0)
            datums[run_name] = data

        for (name, data) in datums.items():
            plot_sel_coeff_preds(data, dtype, name, ua.outdir, list(lab_conv.keys()))


if __name__ == "__main__":
    main()

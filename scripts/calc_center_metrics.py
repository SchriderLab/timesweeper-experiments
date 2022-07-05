import os
from glob import glob
import itertools
import matplotlib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    auc,
    classification_report,
    precision_recall_curve,
    roc_curve,
    confusion_matrix,
)

matplotlib.use("Agg")

import matplotlib.pyplot as plt


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

    plt.figure(figsize=(9, 8))
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

    plt.savefig(os.path.join(working_dir, title + "_OoA_on_Simple.pdf"))
    plt.clf()


labs = []
scores = []

preds = {}
prob_threshes = np.arange(0.5, 1.05, 0.05)
for i in prob_threshes:
    preds[i] = []

for swp in ["neut", "soft", "hard"]:
    for i in glob(
        f"/pine/scr/l/s/lswhiteh/timesweeper-experiments/misspec/OoA_on_Simple/results/{swp}/*/aft_preds.csv",
        recursive=True,
    ):
        try:
            _df = pd.read_csv(i, sep="\t")

            if swp == "neut":
                center_score = float(_df["Sweep_Score"][50])
                labs.append(0)
                scores.append(center_score)

                for i in prob_threshes:
                    if center_score > i:
                        preds[i].append(1)
                    else:
                        preds[i].append(0)

            else:
                center_score = float(_df[_df["Mut_Type"] == 2]["Sweep_Score"])
                labs.append(1)
                scores.append(center_score)

                for i in prob_threshes:
                    if center_score > i:
                        preds[i].append(1)
                    else:
                        preds[i].append(0)
        except:
            pass

"""
# Plot ROC Curve
fpr, tpr, thresh = roc_curve(labs, scores)
auc_val = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"AFT Neutral vs Sweep AUC: {auc_val:.4}")

plt.title(f"ROC Curve Centers Only")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.savefig("centers_roc_OoA_on_Simple.pdf")
plt.clf()

# Plot PR Curve
prec, rec, thr = precision_recall_curve(labs, scores)
auc_val = auc(rec, prec)
plt.plot(rec, prec, label=f"AFT Neutral vs Sweep AUC: {auc_val:.4}")
plt.title(f"PR Curves")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.savefig("centers_pr_OoA_on_Simple.pdf")
plt.clf()
"""

for i in prob_threshes:
    conf_mat = confusion_matrix(labs, preds[i])
    plot_confusion_matrix(
        "./foo",
        conf_mat,
        ["Neutral", "Sweep"],
        title=f"centers_confmat_normed_OoA_on_Simple_thresh_{i}",
        normalize=True,
    )

import matplotlib
from sklearn.metrics import confusion_matrix
import sys

matplotlib.use("Agg")
import itertools
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob


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

    plt.savefig(os.path.join(working_dir, title + ".tiff"))
    plt.savefig(os.path.join(working_dir, title + ".png"))
    plt.clf()


lablist = ["Neutral", "SDN", "SSV"]
data_dir = sys.argv[1]

for ifile in glob(f"{sys.argv[1]}/*.csv"):
    data = pd.read_csv(ifile)
    out_dir = os.path.dirname(ifile) + "/../images"
    filename = os.path.basename(ifile).split("_test")[0]

    conf_mat = confusion_matrix(data["true"], data["pred"])
    plot_confusion_matrix(
        out_dir,
        conf_mat,
        lablist,
        title=f"{filename}_confmat_normed",
        normalize=True,
    )
    plot_confusion_matrix(
        out_dir,
        conf_mat,
        lablist,
        title=f"{filename}_confmat_unnormed",
        normalize=False,
    )

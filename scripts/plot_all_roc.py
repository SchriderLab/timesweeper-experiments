import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    classification_report,
    roc_curve,
    auc,
    precision_recall_curve,
)

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


### ROC Curves
# AFT
aft_data = pd.read_csv(aftfile)
# Coerce all ssvs into sweep binary pred
labs = aft_data["true"]
labs[labs > 1] = 1
pred_probs = np.sum(aft_data[["ssv_scores", "sdn_scores"]], axis=1)

# Plot ROC Curve
fpr, tpr, thresh = roc_curve(labs, pred_probs)
auc_val = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"AFT Neutral vs Sweep AUC: {auc_val:.4}")

# HFT
hft_data = pd.read_csv(hftfile)
# Coerce all ssvs into sweep binary pred
labs = hft_data["true"]
labs[labs > 1] = 1
pred_probs = np.sum(hft_data[["ssv_scores", "sdn_scores"]], axis=1)

# Plot ROC Curve
fpr, tpr, thresh = roc_curve(labs, pred_probs)
auc_val = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"HFT Neutral vs Sweep AUC: {auc_val:.4}")

"""
# FIT
fit_data = pd.read_csv(fitfile).dropna()

# Plot ROC Curve
fpr, tpr, thresh = roc_curve(fit_data["trues"], 1 - fit_data["pvals"])
auc_val = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"FIT Neutral vs Sweep AUC: {auc_val:.4}")

plt.title(f"ROC Curves")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.savefig("ss10_all_roc.pdf")
plt.clf()
"""

### PR Curves
# AFT
aft_data = pd.read_csv(aftfile)
# Coerce all ssvs into sweep binary pred
labs = aft_data["true"]
labs[labs > 1] = 1
pred_probs = np.sum(aft_data[["ssv_scores", "sdn_scores"]], axis=1)

# Plot PR Curve
prec, rec, thr = precision_recall_curve(labs, pred_probs)
auc_val = auc(rec, prec)
plt.plot(rec, prec, label=f"AFT Neutral vs Sweep AUC: {auc_val:.4}")

# HFT
hft_data = pd.read_csv(hftfile)
# Coerce all ssvs into sweep binary pred
labs = hft_data["true"]
labs[labs > 1] = 1
pred_probs = np.sum(hft_data[["ssv_scores", "sdn_scores"]], axis=1)

# Plot PR Curve
prec, rec, thr = precision_recall_curve(labs, pred_probs)
auc_val = auc(rec, prec)
plt.plot(rec, prec, label=f"HFT Neutral vs Sweep AUC: {auc_val:.4}")

# FIT
fit_data = pd.read_csv(fitfile).dropna()

# Plot ROC Curve
prec, rec, thr = precision_recall_curve(fit_data["trues"], 1 - fit_data["pvals"])
auc_val = auc(rec, prec)
plt.plot(rec, prec, label=f"FIT Neutral vs Sweep AUC: {auc_val:.4}")

plt.title(f"PR Curves")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.savefig("ss10_all_pr.tiff")
plt.savefig("ss10_all_pr.png")
plt.clf()

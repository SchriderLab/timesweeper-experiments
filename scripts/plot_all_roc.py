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


fitfile = "../sample_size_10_benchmark/test_predictions/fitvals.csv"
aftfile = "../sample_size_10_benchmark/test_predictions/Sample_Size_10_benchmark_Timesweeper_aft_test_predictions.csv"
hftfile = "../sample_size_10_benchmark/test_predictions/Sample_Size_10_benchmark_Timesweeper_hft_test_predictions.csv"


### ROC Curves
#AFT
aft_data = pd.read_csv(aftfile)
# Coerce all softs into sweep binary pred
labs = aft_data["true"]
labs[labs > 1] = 1
pred_probs = np.sum(aft_data[["soft_scores", "hard_scores"]], axis=1)

# Plot ROC Curve
fpr, tpr, thresh = roc_curve(labs, pred_probs)
auc_val = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"AFT Neutral vs Sweep AUC: {auc_val:.4}")

#HFT
hft_data = pd.read_csv(hftfile)
# Coerce all softs into sweep binary pred
labs = hft_data["true"]
labs[labs > 1] = 1
pred_probs = np.sum(hft_data[["soft_scores", "hard_scores"]], axis=1)

# Plot ROC Curve
fpr, tpr, thresh = roc_curve(labs, pred_probs)
auc_val = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"HFT Neutral vs Sweep AUC: {auc_val:.4}")

#FIT
fit_data = pd.read_csv(fitfile).dropna()

# Plot ROC Curve
fpr, tpr, thresh = roc_curve(fit_data["trues"], 1-fit_data["pvals"])
auc_val = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f"FIT Neutral vs Sweep AUC: {auc_val:.4}")

plt.title(f"ROC Curves")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.savefig("ss10_all_roc.pdf")
plt.clf()


### PR Curves
#AFT
aft_data = pd.read_csv(aftfile)
# Coerce all softs into sweep binary pred
labs = aft_data["true"]
labs[labs > 1] = 1
pred_probs = np.sum(aft_data[["soft_scores", "hard_scores"]], axis=1)

# Plot PR Curve
prec, rec, thr = precision_recall_curve(labs, pred_probs)
auc_val = auc(rec, prec)
plt.plot(rec, prec, label=f"AFT Neutral vs Sweep AUC: {auc_val:.4}")

#HFT
hft_data = pd.read_csv(hftfile)
# Coerce all softs into sweep binary pred
labs = hft_data["true"]
labs[labs > 1] = 1
pred_probs = np.sum(hft_data[["soft_scores", "hard_scores"]], axis=1)

# Plot PR Curve
prec, rec, thr = precision_recall_curve(labs, pred_probs)
auc_val = auc(rec, prec)
plt.plot(rec, prec, label=f"HFT Neutral vs Sweep AUC: {auc_val:.4}")

#FIT
fit_data = pd.read_csv(fitfile).dropna()

# Plot ROC Curve
prec, rec, thr = precision_recall_curve(fit_data["trues"], 1-fit_data["pvals"])
auc_val = auc(rec, prec)
plt.plot(rec, prec, label=f"FIT Neutral vs Sweep AUC: {auc_val:.4}")

plt.title(f"PR Curves")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend()
plt.savefig("ss10_all_pr.pdf")
plt.clf()
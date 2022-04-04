# From https://python-graph-gallery.com/manhattan-plot-with-matplotlib

import pandas as pd
from scipy.stats import uniform
from scipy.stats import randint
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(
    "/pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/mongolian_samples/timesweeper_output/raw/aft_preds_m02.csv",
    sep="\t",
)

# -log_10(1-sweep score)
df["minuslog10pvalue"] = -np.log10(df["Neut Score"])
df["Chrom"] = df["Chrom"].astype("str").astype("category")

# How to plot gene vs. -log10(pvalue) and colour it by Chrom?
df["ind"] = range(len(df))
df_grouped = df.groupby("Chrom")

# manhattan plot
fig = plt.figure(figsize=(20, 8))  # Set the figure size
ax = fig.add_subplot(111)
colors = ["darkred", "darkblue", "darkgreen", "gold"]
x_labels = []
x_labels_pos = []
for num, (name, group) in enumerate(df_grouped):
    group.plot(
        kind="scatter",
        x="ind",
        y="minuslog10pvalue",
        color=colors[num % len(colors)],
        ax=ax,
    )
    x_labels.append(name)
    x_labels_pos.append(
        (group["ind"].iloc[-1] - (group["ind"].iloc[-1] - group["ind"].iloc[0]) / 2)
    )

ax.set_xticks(x_labels_pos)
ax.set_xticklabels(x_labels)
plt.xticks(rotation=45)
ax.set_xmargin(0.5)

# Plot dotted line for threshold
ax.hlines(y=-np.log10(0.05), xmin=0, xmax=len(df), linestyles="dashed")

# set axis limits
ax.set_xlim([0, len(df) + 1])
ax.set_ylim([min(df["minuslog10pvalue"]), 2])

# x axis label
ax.set_xlabel("Chrom")

# show the graph
plt.savefig("manhattan_plot_m02.png")

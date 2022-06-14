import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(
    "/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/replication/summarized_hits.txt",
    header=None,
    sep="\t",
    names=["chrom", "bp", "ts_score", "fet_score", "freqs"],
)

# df = df[df["Soft_Score"] > 0.8]

fig, axes = plt.subplots(1, 1)

axes.set_title("AFT Sweep Score vs FET")
axes.errorbar(
    range(len(groups)), groups["Soft_Score"].mean(), yerr=groups["Soft_Score"].std()
)


fig.set_size_inches(10, 5)
plt.savefig("scores.pdf")

import pandas as pd
from glob import glob

header = "Chromosome	position	-log10(pvalue)_CMH	-log10(p-value)_FET_rep1	-log10(p-value)_FET_rep2	-log10(p-value)_FET_rep3	-log10(p-value)_FET_rep4	-log10(p-value)_FET_rep5	-log10(p-value)_FET_rep6	-log10(p-value)_FET_rep7	-log10(p-value)_FET_rep8-log10(p-value)_FET_rep9	-log10(p-value)_FET_rep10"
exp_pvals = pd.read_csv(
    "/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/pvals.tsv",
    sep="\t",
    names=header.split("\t"),
)

nn_list = []
fit_list = []

for rep in range(1, 11):
    aft_ifiles = glob(
        f"/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/timesweeper_output/aft_*_{rep}_preds.csv"
    )
    for aft_file in aft_ifiles:
        df = pd.read_csv(aft_file, header=0, sep="\t")
        df["Rep"] = [rep] * len(df)
        nn_list.append(df)

    fit_ifiles = glob(
        f"/pine/scr/l/s/lswhiteh/timesweeper-experiments/d_simulans/ts_simulans/timesweeper_output/fit_*_{rep}_preds.csv"
    )
    for fit_file in fit_ifiles:
        df = pd.read_csv(fit_file, header=0, sep="\t")
        df["Rep"] = [rep] * len(df)
        fit_list.append(df)

aft_df = pd.concat(nn_list)
fit_df = pd.concat(fit_list)

print(aft_df)
print(fit_df)
preds_merged = aft_df.merge(fit_df, on=["Chrom", "BP"])
all_merged = preds_merged.merge(
    exp_pvals, left_on=["Chrom", "BP"], right_on=["Chromosome", "position"]
)

all_merged.to_csv("all_merged.tsv", header=True, index=False)

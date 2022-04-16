import pandas as pd
import sys

"""This filters TS predictions to those which are present in a matching BED file that has been filtered/annotated with bedtools."""

bedfile = pd.read_csv(sys.argv[1], sep="\t", header=None)
preds = pd.read_csv(sys.argv[2], sep="\t", header=0)

preds["Chrom"] = preds["Chrom"].astype("str")
bedfile[0] = bedfile[0].astype("str")

final_preds = pd.merge(preds, bedfile, left_on=["Chrom", "BP"], right_on=[0, 3])
final_preds.drop_duplicates(["BP", "Chrom"], inplace=True, keep="first")

final_preds.sort_values(by="Neut Score", inplace=True)

# final_preds.drop_duplicates([7], inplace=True)
# final_preds = final_preds[
#    ["Chrom", "BP", "Class", "Neut Score", "Hard Score", "Soft Score", 0, 1, 2, 7]
# ]


final_preds.to_csv(
    "sorted_allhits_preds.csv", sep="\t", index=False, float_format="%.3f"
)


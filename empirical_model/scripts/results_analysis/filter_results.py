import pandas as pd
import sys
import subprocess

# Filters Timesweeper results based on confidence threshold and non-recombining sites.
gaps_file = "/proj/dschridelab/human/annotations/hg19/ucscGaps_03312022_hg19.bed"
non_recomb_file = "/pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/Kong2010_SexAveraged.wig"

# Filter out lower-confidence scores
res_file = sys.argv[1]
call_thresh = 0.1  # Max confidence that a given pred is neutral

res = pd.read_csv(res_file, sep="\t")
res = res[res["Neut Score"] < call_thresh]
res.to_csv(
    "conf_filtered_results.bed", sep="\t",
)

# Filter out low-recombining regions
recomb_data = pd.read_csv(
    non_recomb_file,
    sep="\t",
    comment="#",
    names=["Chrom", "Start", "End", "Recomb_Rate"],
)
recomb_data["Chrom"] = recomb_data["Chrom"].str.replace("chr", "")

low_recomb_data = recomb_data[recomb_data["Recomb_Rate"] < 0.25]
low_recomb_data.to_csv(
    "kong2010_recomb_below.25.bed", index=False, header=False, sep="\t"
)

# Filter out gapped regions
gaps_data = pd.read_csv(
    gaps_file, header=None, names=["Chrom", "Start", "End"], sep="\t"
)
gaps_data["Chrom"] = gaps_data["Chrom"].str.replace("chr", "")

gaps_data.to_csv("chr_fixed_gaps.hg19.ucsc.bed", index=False, header=False, sep="\t")

# Intersect to get regions remaining
subprocess.run(
    "bedtools intersect -v \
    -a filtered_results.bed \
    -b kong2010_recomb_below.25.bed chr_fixed_gaps.hg19.ucsc.bed \
    > filtered_Timesweeper_candidates.bed".split(),
    shell=True,
)

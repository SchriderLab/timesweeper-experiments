import pandas as pd

vcf = pd.read_csv(
    "/pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/vcfs/merged/ts_merged.filtered.calls.vcf.gz",
    header=None,
    sep="\t",
    comment="#",
)
vcf = vcf[[0, 1]]

dists = {}
for chrom in vcf[0].unique():
    dists[chrom] = []
    locs = list(vcf[vcf[0] == chrom][1]).sort()
    for i in range(25, len(locs) - 25):
        dists[chrom].append(locs[i + 25] - locs[i - 25])

dists_df = pd.DataFrame(dists).to_csv("distances.csv", index=False)

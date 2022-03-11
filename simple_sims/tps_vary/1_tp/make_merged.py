import os
from glob import glob

infiles = glob("1tp_exp/vcfs/*/*.multivcf")

for ifile in infiles:
    numname = os.path.basename(ifile).split(".")[0]
    ipath = os.path.dirname(ifile)
    if not os.path.exists(os.path.join(ipath, numname)):
        os.makedirs(os.path.join(ipath, numname))

    os.rename(ifile, os.path.join(ipath, numname, "merged.vcf"))
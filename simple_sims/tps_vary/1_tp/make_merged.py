import os
from glob import glob
import shutil
from tqdm import tqdm
from allel import read_vcf
import warnings

warnings.filterwarnings("error")

infiles = glob("1tp_exp/vcfs/*/*.multivcf")

for ifile in tqdm(infiles):
    numname = os.path.basename(ifile).split(".")[0]
    ipath = os.path.dirname(ifile)

    try:
        foo = read_vcf(ifile)
    except UserWarning as uw:
        print(ifile)
        continue

    os.makedirs(os.path.join(ipath, numname), exist_ok=True)
    shutil.copy(ifile, os.path.join(ipath, numname, "merged.vcf"))

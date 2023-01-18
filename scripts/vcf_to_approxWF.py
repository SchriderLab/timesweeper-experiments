import argparse
import math
from pathlib import Path
import multiprocessing as mp
import allel
import numpy as np
from tqdm import tqdm
import subprocess
from itertools import cycle
import os

# type: ignore

"""
Script to convert VCF files to SHIC feature vectors
Some calculations are done assuming you want 20% of the chromosome length sampled, namely `half_window`
"""


def converter(args):
    vcffile, L, samp_sizes = args
    try:
        vcf = allel.read_vcf(
            vcffile, fields=["variants/CHROM", "variants/POS", "calldata/GT"]
        )
        snps = list(zip(vcf["variants/CHROM"], vcf["variants/POS"]))
        haps = allel.GenotypeArray(vcf["calldata/GT"]).to_haplotypes()
        # Shape is now (snps, haps)

        # Iterate through timepoints to get each row
        tp_labels = list(range(10, 210, 10))
        tp_counts = []
        cur_samp = 0
        for tp_idx in range(len(samp_sizes)):
            tp_haps = haps[cur_samp : cur_samp + (2 * samp_sizes[tp_idx]) :]
            cur_samp += 2 * samp_sizes[tp_idx]
            counts = np.sum(tp_haps, axis=1).flatten()
            tp_counts.append([f"{c}/{2*samp_sizes[tp_idx]}" for c in counts])

        vcf_fullpath = os.path.abspath(vcffile)
        if "neut" in vcf_fullpath:
            tp_msOutfile = (
                vcffile.split(".")[0] + f".neut.win_{windows[window_idx]}.msOut"
            )
        elif "sdn" in vcf_fullpath:
            tp_msOutfile = (
                vcffile.split(".")[0] + f".sdn.win_{windows[window_idx]}.msOut"
            )
        elif "ssv" in vcf_fullpath:
            tp_msOutfile = (
                vcffile.split(".")[0] + f".ssv.win_{windows[window_idx]}.msOut"
            )
        else:
            print("Path doesn't have necessary sweep component")
            continue

        if tp_idx == 0:
            with open(tp_msOutfile, "w") as ofile:
                ofile.write(
                    f"ms {tp_haps.shape[0]} {len(samp_sizes)} -t {ua.theta}" + "\n"
                )
                ofile.write("\n")
                ofile.write("//" + "\n")
                ofile.write(f"segsites: {tp_haps.shape[1]}" + "\n")
                ofile.write(
                    f"positions: {' '.join([str(i) for i in positions])}" + "\n"
                )
                for hap in tp_haps:
                    ofile.write("".join([str(int(i)) for i in hap]))
                    ofile.write("\n")

        fvec_name = tp_msOutfile.replace("msOut", "fvec")
        subprocess.run(
            f"diploSHIC fvecSim diploid {tp_msOutfile} {fvec_name}",
            shell=True,
            stderr=open(f"{tp_msOutfile}.shiclog.txt", "a"),
            stdout=open(f"{tp_msOutfile}.shiclog.txt", "a"),
        )

    except Exception as e:
        print(f"{vcffile} couldn't be converted due to: {e}")


def get_ua():
    agp = argparse.ArgumentParser(
        description="Utility to convert VCFs to ms-style outputs. Output will be placed in the same location with identical filename as VCF with the `.msOut` suffix.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    agp.add_argument(
        "-s",
        "--samp-sizes",
        dest="samp_sizes",
        nargs="+",
        default=[10] * 20,
        required=False,
        help="Number of diploid individuals at each sampling timepoint to extract from the haplotypes.",
    )
    agp.add_argument(
        "-id",
        "--in-dir",
        dest="in_dir",
        type=str,
        required=False,
        help="Top-level vcf directory to search for VCFs in. E.g. samp_size_10/vcfs. Output will be in the same structure as VCFs if --outdir is unused with this option.",
    )
    agp.add_argument(
        "-i",
        "--in-vcf",
        dest="in_vcf",
        type=str,
        required=False,
        help="Single VCF to convert.",
    )
    agp.add_argument(
        "--simulated",
        dest="simmed",
        type=bool,
        default=True,
        help="Whether VCF(s) are from SLiM or not and therefore whether to check for mutation type.",
    )

    agp.add_argument(
        "--sim-chrom-size",
        dest="chrom_size",
        type=int,
        required=False,
        default=5000000,
        help="Total size of simulated chromosomes used to output VCFs.",
    )
    agp.add_argument(
        "--theta",
        dest="theta",
        type=float,
        required=False,
        default=4 * 500 * (1e-7),
        help="Theta used for simulations.",
    )
    return agp.parse_args()


ua = get_ua()

if ua.in_vcf:
    vcflist = [ua.in_vcf]
elif ua.in_dir:
    path = Path(ua.in_dir)
    vcflist = [str(i) for i in path.glob("**/*.vcf")]
else:
    raise ValueError("[Err] Must provide either in-vcf or in-dir.")

mp_args = zip(vcflist, cycle([ua.chrom_size]), cycle([ua.samp_sizes]))

with mp.Pool(mp.cpu_count()) as p:
    _ = list(
        tqdm(
            p.imap_unordered(converter, mp_args, chunksize=4),
            desc="Converting",
            total=len(vcflist),
        )
    )

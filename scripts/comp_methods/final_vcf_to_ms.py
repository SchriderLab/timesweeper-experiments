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
import random

# type: ignore

"""
Script to convert VCF files to SHIC feature vectors
Some calculations are done assuming you want 20% of the chromosome length sampled, namely `half_window`
"""


def converter(args):
    vcffile, L, samp_size = args
    try:
        vcf = allel.read_vcf(
            vcffile, fields=["variants/CHROM", "variants/POS", "calldata/GT"]
        )
        raw_snps = list(zip(vcf["variants/CHROM"], vcf["variants/POS"]))
        raw_haps = allel.GenotypeArray(vcf["calldata/GT"]).to_haplotypes().T
        # Shape is now (haps, snps)
        # Subsample to individuals requested
        raw_haps = raw_haps[random.sample(range(raw_haps.shape[0]), samp_size * 2), :]
        print(raw_haps.shape)

        window_size = L / 11

        ### Iterate through window positions
        windows = list(range(11))
        for window in windows:
            win_start, win_end = (
                window * window_size,
                (window + 1) * window_size,
            )

            snp_idxs = [
                i
                for i in range(len(raw_snps))
                if raw_snps[i][1] > win_start and raw_snps[i][1] < win_end
            ]
            snps = [raw_snps[i] for i in snp_idxs]
            haps = raw_haps[:, snp_idxs]

            vcf_fullpath = os.path.abspath(vcffile)
            if "neut" in vcf_fullpath:
                msOutfile = vcffile.split(".")[0] + f".final.neut.win_{window}.msOut"
            elif "sdn" in vcf_fullpath:
                msOutfile = vcffile.split(".")[0] + f".final.sdn.win_{window}.msOut"
            elif "ssv" in vcf_fullpath:
                msOutfile = vcffile.split(".")[0] + f".final.ssv.win_{window}.msOut"
            else:
                print("Path doesn't have necessary sweep component")
                continue

            # Recalculate positions with filtered SNPs
            # Scale position in window to 0-1
            positions = [
                ((snps[i][1] - win_start) / window_size) for i in range(len(snps))
            ]

            with open(msOutfile, "w") as ofile:
                ofile.write(f"ms {haps.shape[0]} 1 -t {ua.theta}" + "\n")
                ofile.write("\n")
                ofile.write("//" + "\n")
                ofile.write(f"segsites: {haps.shape[1]}" + "\n")
                ofile.write(
                    f"positions: {' '.join([str(i) for i in positions])}" + "\n"
                )
                for hap in haps:
                    ofile.write("".join([str(int(i)) for i in hap]))
                    ofile.write("\n")

            fvec_name = msOutfile.replace("msOut", "fvec")
            subprocess.run(
                f"diploSHIC fvecSim diploid {msOutfile} {fvec_name}",
                shell=True,
                # stderr=open(f"{msOutfile}.shiclog.txt", "a"),
                # stdout=open(f"{msOutfile}.shiclog.txt", "a"),
            )

    except Exception as e:
        print(f"{vcffile} couldn't be converted due to: {e}")


def get_ua():
    agp = argparse.ArgumentParser(
        description="Utility to convert VCFs to ms-style outputs. Output will be placed in the same location with identical filename as VCF with the `.msOut` suffix.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
        "-s",
        "--samp-size",
        dest="samp_size",
        default=200,
        required=False,
        help="Number of diploid individuals to use.",
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
    vcflist = [str(i) for i in path.glob("**/*.vcf") if "final" in i]
else:
    raise ValueError("[Err] Must provide either in-vcf or in-dir.")

mp_args = zip(vcflist, cycle([ua.chrom_size]), cycle([ua.samp_size]))

with mp.Pool(mp.cpu_count()) as p:
    _ = list(
        tqdm(
            p.imap_unordered(converter, mp_args, chunksize=4),
            desc="Converting",
            total=len(vcflist),
        )
    )

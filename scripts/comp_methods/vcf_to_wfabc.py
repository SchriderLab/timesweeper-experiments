import argparse
import allel
import numpy as np
import subprocess
import os

# type: ignore

"""
Script to convert VCF files to SHIC feature vectors
Some calculations are done assuming you want 20% of the chromosome length sampled, namely `half_window`
"""


def get_sweep(filename):
    if "neut" in filename:
        return "neut"
    elif "sdn" in filename:
        return "sdn"
    elif "ssv" in filename:
        return "ssv"
    else:
        return None


def converter(vcffile, samp_sizes):
    vcf = allel.read_vcf(
        vcffile,
        fields=[
            "variants/CHROM",
            "variants/POS",
            "calldata/GT",
            "variants/S",
            "variants/MT",
        ],
    )
    snps = list(
        zip(
            vcf["variants/CHROM"],
            vcf["variants/POS"],
            vcf["variants/MT"],
            vcf["variants/S"],
        )
    )
    haps = allel.GenotypeArray(vcf["calldata/GT"]).to_haplotypes()
    # Shape is now (snps, haps)

    center_idx = int(haps.shape[1] / 2)

    for i in range(len(snps)):
        if str(snps[i][2]) == "2":
            center_idx = i
            break
        else:
            pass

    sel_coeff = snps[center_idx][3]
    target_hap = haps[center_idx, :]

    # Iterate through timepoints to get each row
    tp_labels = list(range(10, 210, 10))
    tp_counts = []
    cur_samp = 0
    for tp_idx in range(len(samp_sizes)):
        tp_haps = target_hap[cur_samp : cur_samp + (2 * samp_sizes[tp_idx])]
        cur_samp += 2 * samp_sizes[tp_idx]
        tp_counts.append(np.sum(tp_haps))

    sweep = get_sweep(os.path.abspath(vcffile))
    locifile = vcffile + f"_{sweep}_s{sel_coeff}_WFABC_in.txt"
    with open(locifile, "w") as ofile:
        ofile.write("1" + "\t" + f"{str(len(tp_labels))}" + "\n")
        ofile.write("\t".join([str(i) for i in tp_labels]) + "\n")
        ofile.write("\t".join([str(i) for i in [20]*20]) + "\n")
        ofile.write("\t".join([str(i) for i in tp_counts]))

    cmd1 = f"""/work/users/l/s/lswhiteh/timesweeper-experiments/comp_tools/WFABC_v1.1/binaries/Linux/wfabc_1 \
        -nboots 0 \
        {locifile} \
        """

    subprocess.run(
        cmd1,
        shell=True,
        stdout=open(f"{locifile}.wfabc.1.log", "w"),
        stderr=open(f"{locifile}.wfabc.1.log", "w"),
    )

    cmd2 = f"""/work/users/l/s/lswhiteh/timesweeper-experiments/comp_tools/WFABC_v1.1/binaries/Linux/wfabc_2 \
        -fixed_N 500 \
        -ploidy 2 \
        -min_s 0 \
        -max_s 0.25 \
        {locifile} \
        """

    subprocess.run(
        cmd2,
        shell=True,
        stdout=open(f"{locifile}.wfabc.2.log", "w"),
        stderr=open(f"{locifile}.wfabc.2.log", "w"),
    )

def get_ua():
    agp = argparse.ArgumentParser(
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
        "-i",
        "--in-vcf",
        dest="in_vcf",
        type=str,
        required=False,
        help="Single VCF to convert.",
    )
    return agp.parse_args()


ua = get_ua()

converter(ua.in_vcf, ua.samp_sizes)

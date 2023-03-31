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
        counts = np.sum(tp_haps)
        tp_counts.append(f"{counts}/{2*samp_sizes[tp_idx]}")

    sweep = get_sweep(os.path.abspath(vcffile))
    locifile = vcffile + ".appWF_in.loci"
    with open(locifile, "w") as ofile:
        ofile.write("time\t" + "\t".join([str(i) for i in tp_labels]) + "\n")
        ofile.write(f"{sweep}_{str(sel_coeff)}" + "\t" + "\t".join(tp_counts))

    cmd = f"""/work/users/l/s/lswhiteh/timesweeper-experiments/comp_tools/approxwf/ApproxWF \
        task=estimate \
        loci={locifile} \
        N=500 \
        mutRate=1e-7 \
        h=0.5 \
        sampling=100 \
        MCMClength=100000 \
        verbose"""

    subprocess.run(
        cmd,
        shell=True,
        stdout=open(f"{locifile}.mcmc.log", "w"),
        stderr=open(f"{locifile}.mcmc.log", "w"),
    )


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

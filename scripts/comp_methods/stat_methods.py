import argparse
import os
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import ttest_1samp
from tqdm import tqdm
from timesweeper.utils import snp_utils as su
from timesweeper.make_training_features import prep_ts_aft

warnings.filterwarnings("ignore", category=RuntimeWarning)

"""
Time series:
-	FIT
-	FET
-	spectralHMM
Single point: final timepoint
-	S/HIC
-	Fay and Wu’s H (windowed, from S/HIC) 
-	SweepFinder
"""


def fit(freqs, gens):
    """
    Calculate FIT by performing 1-Sided Student t-test on frequency increments.

    Args:
        freqs (List[int]): Frequencies at all given generations for targeted alleles.
        gens (List[int]): Generations sampled.

    Returns:
        List[int]: t-test results.
    """
    incs = []
    i = 0
    # advance to first non-zero freq
    while i < len(freqs) and (freqs[i] == 0 or freqs[i] == 1):
        i += 1
    if i < len(freqs):
        prevFreq = freqs[i]
        prevGen = gens[i]
        i += 1
        while i < len(freqs):
            if freqs[i] != 0 and freqs[i] != 1:
                num = freqs[i] - prevFreq
                denom = ((2 * prevFreq) * (1 - prevFreq) * (gens[i] - prevGen)) ** 0.5
                incs.append(num / denom)
                prevFreq = freqs[i]
                prevGen = gens[i]
            i += 1

    return ttest_1samp(incs, 0)[1]


def write_fit(fit_dict, outfile, benchmark):
    """
    Writes FIT predictions to file.

    Args:
        fit_dict (dict): FIT p values and SNP information.
        outfile (str): File to write results to.
    """
    inv_pval = [1 - i[1] for i in fit_dict.values()]
    if benchmark:
        chroms, bps, mut_type = zip(*fit_dict.keys())
        predictions = pd.DataFrame(
            {"Chrom": chroms, "BP": bps, "Mut_Type": mut_type, "Inv_pval": inv_pval}
        )
    else:
        chroms, bps = zip(*fit_dict.keys())
        predictions = pd.DataFrame({"Chrom": chroms, "BP": bps, "Inv_pval": inv_pval})

    predictions.dropna(inplace=True)
    predictions.sort_values(["Chrom", "BP"], inplace=True)
    predictions.to_csv(
        os.path.join(outfile),
        header=True,
        index=False,
        sep="\t",
    )


def get_ua():
    parser = argparse.ArgumentParser(
        description="""\
            Module to run alternative selective sweep detection methods for both time series and single-timepoint data. 
            Methods in this script include: 
                Fisher's Exact Test (FET) + Frequency Increment Test (FIT)
                SweepFinder2
                spectralHMM
        """
    )
    parser.add_argument(
        "-v",
        "--vcf",
        required=True,
        help="Multi-timepoint input VCF file formatted as required for Timesweeper.",
    )
    parser.add_argument(
        "-o", "--out", action="store", required=True, help="Output CSV."
    )
    parser.add_argument(
        "-b",
        "--benchmark",
        action="store_true",
        help="Use this flag to denote the input_vcf is a simulated sample and the SLIM mutation type can be parsed.",
    )
    parser.add_argument(
        "-m",
        "--methods",
        nargs="+",
        choices=["FIT-FET", "SweepFinder2", "diploSHIC", "HMM"],
        required=False,
        help="Which methods to use.",
    )
    parser.add_argument(
        "-dm",
        "--diploshic-model",
        required=False,
        help="If using diploSHIC must provide a trained model.",
    )
    parser.add_argument(
        "-s",
        "--sample-sizes",
        nargs="+",
        required=True,
        help="Number of sampled individuals at each timepoint separated by a space.",
    )
    parser.add_argument(
        "-g",
        "--gens-sampled",
        nargs="+",
        required=True,
        help="Generation of each sampling point. Relative spacing between values is only relevant aspect, so can be generations from present or from 0.",
    )
    return parser.parse_args()


def main():
    """
    Load VCF
    Iterate through SNPs
    Calculate frequencies
    Do tests

    Convert VCF to SF input
    Run SF2
    """

    args = get_ua()
    in_vcf = args.vcf
    outfile = args.out
    benchmark = args.benchmark
    methods = args.methods
    samp_sizes = [int(i) for i in args.sample_sizes]
    gens_sampled = [int(i) for i in args.gens_sampled]

    if "FIT-FET" in methods:
        print("Running Frequency Increment Test (FIT) and Fisher's Exact Test (FET)")
        results_dict = {}
        vcf_iter = su.get_vcf_iter(in_vcf, benchmark)
        for chunk_idx, chunk in enumerate(vcf_iter):
            chunk = chunk[0]  # Why you gotta do me like that, skallel?

            genos, snps = su.vcf_to_genos(chunk, benchmark)
            ts_aft = prep_ts_aft(genos, samp_sizes)

            # FIT
            for idx in tqdm(
                range(len(snps)), desc=f"Calculating FIT for chunk {chunk_idx}"
            ):
                results_dict[snps[idx]] = {}
                results_dict[snps[idx]]["FIT"] = fit(
                    list(ts_aft[:, idx]), gens_sampled
                )  # tval, pval

                first_min_allele = ts_aft[:, idx][0]
                first_maj_allele = 1 - first_min_allele
                last_min_allele = ts_aft[:, idx][-1]
                last_maj_allele = 1 - last_min_allele

                results_dict[snps[idx]]["FET"] = stats.fisher_exact(
                    [
                        [first_maj_allele, last_maj_allele],
                        [first_min_allele, last_min_allele],
                    ]
                )[1]

    res_df = (
        pd.Series(results_dict)
        .rename_axis(["chrom", "bp"])
        .reset_index(name="res_dict")
    )
    res_df = pd.concat(
        [res_df.drop(["res_dict"], axis=1), res_df["res_dict"].apply(pd.Series)], axis=1
    )
    print(res_df)
    res_df.to_csv(outfile)


if __name__ == "__main__":
    main()

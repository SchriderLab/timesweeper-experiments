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


def make_list_from_str(list_str):
    return [int(i) for i in list_str.strip("[").strip("]").split(", ")]


def get_ua():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--sample-sizes",
        nargs="+",
        required=False,
        default=[10] * 20,
        help="Number of sampled individuals at each timepoint separated by a space.",
    )
    parser.add_argument(
        "-g",
        "--gens-sampled",
        nargs="+",
        required=False,
        default=list(range(0, 200, 10)),
        help="Number of sampled individuals at each timepoint separated by a space.",
    )
    parser.add_argument(
        "-r",
        "--replicate",
        dest="rep",
        type=int,
        required=True,
        help="Replicate ID to pull out from the dataset for parallelized runs",
    )
    return parser.parse_args()


def main():
    args = get_ua()

    benchmark = True
    gens_sampled = [int(i) for i in args.gens_sampled]

    for swp in ["neut", "sdn", "ssv"]:
        in_vcf = f"/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/{swp}/{args.rep}/merged.vcf"

        print("Running Frequency Increment Test (FIT) and Fisher's Exact Test (FET)")
        results_dict = {}
        vcf_iter = su.get_vcf_iter(in_vcf, benchmark)
        for chunk_idx, chunk in enumerate(vcf_iter):
            chunk = chunk[0]  # Why you gotta do me like that, skallel?

            genos, snps = su.vcf_to_genos(chunk, benchmark)
            ts_aft = prep_ts_aft(genos, args.sample_sizes)

            # FIT
            for idx in tqdm(
                range(len(snps)), desc=f"Calculating FIT for chunk {chunk_idx}"
            ):
                results_dict[snps[idx]] = {}
                results_dict[snps[idx]]["FIT_pval"] = fit(
                    list(ts_aft[:, idx]), gens_sampled
                )  # tval, pval

                first_min_allele = ts_aft[:, idx][0]
                first_maj_allele = 1 - first_min_allele
                last_min_allele = ts_aft[:, idx][-1]
                last_maj_allele = 1 - last_min_allele

                results_dict[snps[idx]]["FET_pval"] = stats.fisher_exact(
                    [
                        [first_maj_allele*20, first_min_allele*20],
                        [last_maj_allele*20, last_min_allele*20],
                    ],
                alternative="two-sided")[1]

        res_df = (
            pd.Series(results_dict)
            .rename_axis(["chrom", "bp", "mut_type", "s_val"])
            .reset_index(name="res_dict")
        )
        res_df = pd.concat(
            [res_df.drop(["res_dict"], axis=1), res_df["res_dict"].apply(pd.Series)],
            axis=1,
        )

        outfile = in_vcf.replace("merged.vcf", f"{args.rep}_{swp}_stat_methods.csv")
        res_df.to_csv(outfile, index=False)


if __name__ == "__main__":
    main()

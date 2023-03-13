import argparse as ap
import logging
import os

from itertools import cycle
import numpy as np
import pandas as pd
import yaml
from tensorflow.keras.models import load_model
from tqdm import tqdm
import pickle as pkl

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

logging.basicConfig()
logger = logging.getLogger("timesweeper")
logger.setLevel("INFO")

pd.options.display.float_format = "{:.2f}".format


def load_npz(npz_path):
    npz_obj = np.load(npz_path)
    aft = npz_obj["aftIn"]  # (snps, timepoints, window)
    locs = npz_obj["aftInPosition"]  # (snps, window_locs)

    return aft, locs


def parse_npz_name(npz_path):
    splitpath = npz_path.split("_")
    chrom = splitpath[2]
    rep = splitpath[-1].split(".")[0]

    return chrom, rep


def run_aft_windows(ts_aft, locs, chrom, c_model, r_model, selcoeff_scaler):
    """
    Iterates through windows of MAF time-series matrix and predicts using NN.

    Args:
        snps (list[tup(chrom, pos,  mut)]): Tuples of information for each SNP. Contains mut only if benchmarking == True.
        genos (allel.GenotypeArray): Genotypes of all samples. 
        samp_sizes (list[int]): Number of chromosomes sampled at each timepoint.
        win_size (int): Number of SNPs to use for each prediction. Needs to match how NN was trained.
        model (Keras.model): Keras model to use for prediction.

    Returns:
        dict: Prediction values in the form of dict[snps[center]]
        np.arr: the central-most window, either based on mutation type or closest to half size of chrom.
    """
    left_edges = list(locs[:, 0])
    right_edges = list(locs[:, -1])
    centers = list(locs[:, 25])
    class_probs = c_model.predict(ts_aft)
    s_est = selcoeff_scaler.inverse_transform(r_model.predict(ts_aft))

    results_list = zip(cycle([chrom]), centers, left_edges, right_edges, class_probs, s_est)

    return results_list


def write_preds(results_list, outfile, benchmark):
    """
    Writes NN predictions to file.

    Args:
        results_dict (dict): SNP NN prediction scores and window edges.
        outfile (str): File to write results to.
    """
    lab_dict = {0: "Neut", 1: "SSV"}
    chrom, centers, left_edges, right_edges, probs, s_coeffs = zip(*results_list)

    neut_scores = [i[0] for i in probs]
    ssv_scores = [i[1] for i in probs]
    classes = [lab_dict[np.argmax(i)] for i in probs]

    predictions = pd.DataFrame(
        {
            "Chrom": chrom,
            "BP": centers,
            "Class": classes,
            "Neut_Score": neut_scores,
            "SSV_Score": ssv_scores,
            "s_coeff": [i[0] for i in s_coeffs],
            "Win_Start": left_edges,
            "Win_End": right_edges,
        }
    )

    # predictions = predictions[predictions["Neut_Score"] < 0.5]

    predictions.sort_values(["Chrom", "BP"], inplace=True)

    predictions.to_csv(outfile, header=True, index=False, sep="\t", float_format="%.3f")

    bed_df = predictions[["Chrom", "Win_Start", "Win_End", "BP"]]
    bed_df.to_csv(outfile.replace(".csv", ".bed"), header=False, index=False, sep="\t")


def parse_ua():
    uap = ap.ArgumentParser(
        description="Module for iterating across windows in a time-series vcf file and predicting whether a sweep is present at each snp-centralized window."
    )
    uap.add_argument(
        "-i",
        "--input-file",
        dest="input_file",
        help="NPZ file with allele frequencies already processed in proper shape.",
        required=True,
    )
    uap.add_argument(
        "-o",
        "--out-dir",
        dest="outdir",
        help="Directory to write output to.",
        required=True,
    )
    uap.add_argument(
        "--benchmark",
        dest="benchmark",
        action="store_true",
        help="If testing on simulated data and would like to report the mutation \
            type stored by SLiM during outputVCFSample as well as neutral predictions, use this flag. \
            Otherwise the mutation type will not be looked for in the VCF entry nor reported with results.",
        required=False,
    )
    uap.add_argument(
        "--class-model",
        dest="class_model",
        help="Path to Keras2-style saved model to load for classification aft prediction.",
        required=True,
    )
    uap.add_argument(
        "--reg-model",
        dest="reg_model",
        help="Path to Keras2-style saved model to load for regression aft prediction.",
        required=True,
    )
    uap.add_argument(
        "--scaler",
        dest="scaler",
        help="Path to pickled selcoeff scaler.",
        required=True,
    )
    return uap.parse_args()


def main(ua):
    outdir, class_model, reg_model, scaler = (
        ua.outdir,
        load_model(ua.class_model),
        load_model(ua.reg_model),
        pkl.load(open(ua.scaler, 'rb'))
    )

    try:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
    except:
        #running in high-parallel sometimes it errors when trying to check/create simultaneously
        pass

    # Load in everything
    logger.info(f"Loading data from {ua.input_file}")
    chrom, rep = parse_npz_name(ua.input_file)
    ts_aft, locs = load_npz(ua.input_file)

    # aft
    logger.info("Predicting with AFT")
    aft_predictions = run_aft_windows(ts_aft, locs, chrom, class_model, reg_model, scaler)
    write_preds(aft_predictions, f"{outdir}/aft_{chrom}_{rep}_preds.csv", ua.benchmark)
    logger.info(f"Done, results written to {outdir}/aft_{chrom}_{rep}_preds.csv")

if __name__ == "__main__":
    ua = parse_ua()
    main(ua)

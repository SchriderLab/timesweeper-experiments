import argparse
import pickle as pkl
import subprocess
from itertools import cycle

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
import sys


def make_list_from_str(list_str):
    return [int(i) for i in list_str.strip("[").strip("]").split(", ")]


def get_ua():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-r",
        "--replicate",
        dest="rep",
        type=int,
        required=True,
        help="Replicate ID to pull out from the dataset for parallelized runs",
    )

    ap.add_argument(
        "-l",
        "--slim-log",
        dest="slim_logs",
        type=str,
        required=True,
        default="/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/Testing_params.tsv",
    )
    ap.add_argument(
        "-t",
        "--training-data",
        dest="training_data_file",
        type=str,
        required=True,
        default="/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/testing_data.pkl",
    )
    ua = ap.parse_args()
    return ua


def main():
    """
    Pull in test data
    Pull in training data
    Extract all test data central snp
    Create config file for spectralHMM
    Run and collect results
    Parse results and tabulate

    rep	sweep	selCoeff	sampOffset	numRestarts	numSamples	seed	physLen	sampGens	selAlleleFreq	class	true_sel_coeff	pred_sel_coeff	abs_error
    19212	sdn	0.0110916521803371	2	16	20	711469270847202	5000000	[9998, 10009, 10019, 10030, 10040, 10051, 10061, 10072, 10083, 10093, 10104, 10114, 10125, 10136, 10146, 10157, 10167, 10178, 10188, 10199]	[0.001, 0.019, 0.035, 0.042, 0.066, 0.112, 0.171, 0.176, 0.226, 0.215, 0.195, 0.208, 0.189, 0.229, 0.352, 0.36, 0.44, 0.462, 0.565, 0.597]	sdn	0.0110917	0.04299812	0.031906420000000005

    """

    ua = get_ua()
    with open(ua.training_data_file, "rb") as pklfile:
        train_d = pkl.load(pklfile)

    log_info = pd.read_csv(ua.slim_logs, sep="\t")

    yearsPerGen = 25
    mutRate = 1e-7
    popSize = 500
    sampSize = 20

    for swp in ["neut", "sdn", "ssv"]:
        multiplex_lines = []

        s_df = log_info[(log_info["rep"] == ua.rep) & (log_info["sweep"] == swp)]
        sel_coeff = s_df["selCoeff"].values[0]

        sampYears = [
            (i) * yearsPerGen for i in make_list_from_str(s_df["sampGens"].values[0])
        ]

        selFreqs = train_d[swp][str(ua.rep)]["aft"][:, 25]
        numDerived = [int(round(i * sampSize)) for i in selFreqs]
        initFreq = selFreqs[0]

        multiplex_lines.append(
            " ".join(
                [
                    f"({yr}.00, {ss}, {nd});"
                    for yr, ss, nd in zip(sampYears, cycle([sampSize]), numDerived)
                ]
            )
        )
        print(multiplex_lines)

        spectral_config = f"/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/{swp}/{ua.rep}/{swp}_{ua.rep}_spectral.config"
        with open(spectral_config, "w") as tmpfile:
            tmpfile.writelines("\n".join(multiplex_lines))

        cmd = f"""python /work/users/l/s/lswhiteh/timesweeper-experiments/spectralHMM/runSpectralHMM.py \
            -Xmx2g \
            --multiplex \
            --inputFile {spectral_config} \
            --mutToBenef {mutRate} \
            --mutFromBenef {mutRate} \
            --effPopSize {popSize} \
            --yearsPerGen {yearsPerGen} \
            --initFrequency {initFreq} \
            --initTime {sampYears[0] - s_df["sampOffset"]}.00 \
            --selection [0.0:0.0025:0.25] \
            --dominance 0.5 \
            --precision 40 \
            --matrixCutoff 150 \
            --maxM 140 \
            --maxN 130"""

        scoeffs = []
        likelihoods = []
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, text=True)
        while (line := p.stdout.readline()) != "":
            line = line.strip()
            if "#" in line:
                if "selection =" in line:
                    scoeffs.append(float(line.strip().split()[3]))
                pass
            else:
                likelihoods.append(float(line.split("\t")[-1]))

        max_likelihood = max(likelihoods)
        best_scoeff = scoeffs[likelihoods.index(max_likelihood)]

        res_dict = {
            "rep": ua.rep,
            "sweep": swp,
            "true_selCoeff": sel_coeff,
            "est_selCoeff": best_scoeff,
            "max_likelihood": max_likelihood,
        }

        foo = pd.DataFrame(res_dict, index=[0])
        foo.to_csv(
            f"/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/{swp}/{ua.rep}/{swp}_{ua.rep}_spectralres.tsv",
            index=False,
            sep="\t",
        )

        pd.DataFrame(
            {
                "rep": [ua.rep for i in range(len(likelihoods))],
                "sweep": [swp for i in range(len(likelihoods))],
                "true_selCoeff": [sel_coeff for i in range(len(likelihoods))],
                "est_selCoeff": scoeffs,
                "likelihood": likelihoods,
            }
        ).to_csv(
            f"/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/{swp}/{ua.rep}/{swp}_{ua.rep}_all_spectralres.tsv",
            index=False,
            sep="\t",
        )


if __name__ == "__main__":
    main()

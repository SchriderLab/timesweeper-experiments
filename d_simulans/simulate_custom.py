import argparse
import logging
import multiprocessing as mp
import os
import subprocess
import sys
import yaml
import numpy as np

logging.basicConfig()
logger = logging.getLogger("simple_simulate")
logger.setLevel("INFO")


def randomize_selCoeff(lower_bound=0.005, upper_bound=0.5):
    """Draws selection coefficient from log normal dist to vary selection strength."""
    rng = np.random.default_rng(
        np.random.seed(int.from_bytes(os.urandom(4), byteorder="little"))
    )
    log_low = np.math.log10(lower_bound)
    log_upper = np.math.log10(upper_bound)
    rand_log = rng.uniform(log_low, log_upper, 1)

    return 10 ** rand_log[0]


def read_config(yaml_file):
    """Reads in the YAML config file."""
    with open(yaml_file, "r") as infile:
        yamldata = yaml.safe_load(infile)

    return yamldata


def make_d_block(sweep, outFile, dumpfile, verbose=False):
    """
    This is meant to be a very customizeable block of text for adding custom args to SLiM as constants.
    Can add other functions to this module and call them here e.g. pulling selection coeff from a dist.
    This block MUST INCLUDE the 'sweep' and 'outFile' params, and at the very least the outFile must be used as output for outputVCFSample.
    Please note that when feeding strings as a constant you must escape them since this is a shell process.
    """
    rng = np.random.default_rng(
        np.random.seed(int.from_bytes(os.urandom(4), byteorder="little"))
    )

    recomb_rate = rng.uniform(0, 2e-8)

    num_sample_points = 7
    inds_per_tp = 100  # Diploid inds
    physLen = 100000
    burnPopSize = 250000
    selPopSize = 1000
    selCoeff = randomize_selCoeff(0.02, 0.2)
    seed = int(rng.uniform(0, 1e16))

    Q = 100
    d_block_burn = f"""
    -d sweep=\"{sweep}\" \
    -d outFile=\"{outFile}\" \
    -d dumpFile=\"{dumpfile}\" \
    -d samplingInterval={int(60/num_sample_points)} \
    -d burnPopSize={int(burnPopSize/Q)} \
    -d selPopSize={int(selPopSize/Q)} \
    -d mutationRate={Q*5e-9} \
    -d recombRate={recomb_rate * Q} \
    -d selCoeff={selCoeff * Q} \
    -d Q={Q} \
    -d numSamples={num_sample_points} \
    -d sampleSizePerStep={inds_per_tp} \
    -d physLen={physLen} \
    -d seed={seed} \
    """

    Q = 1
    d_block_sel = f"""
    -d sweep=\"{sweep}\" \
    -d outFile=\"{outFile}\" \
    -d dumpFile=\"{dumpfile}\" \
    -d samplingInterval={int(60/num_sample_points)} \
    -d burnPopSize={int(burnPopSize/100)} \
    -d selPopSize={int(selPopSize/Q)} \
    -d mutationRate={Q*5e-9} \
    -d recombRate={recomb_rate * Q} \
    -d selCoeff={selCoeff * Q} \
    -d Q={Q} \
    -d numSamples={num_sample_points} \
    -d sampleSizePerStep={inds_per_tp} \
    -d physLen={physLen} \
    -d seed={seed} \
    """

    if verbose:
        logger.info(f"Using the following constants with SLiM: {d_block_burn}")

    return d_block_burn, d_block_sel


def run_slim(slimfile, d_block_burn, d_block_sel):
    cmd1 = f"slim {d_block_burn} {slimfile}.burn"
    cmd2 = f"slim {d_block_sel} {slimfile}.selection"

    try:
        slimlog1 = subprocess.check_output(cmd1.split())
        logger.info(slimlog1)
        slimlog2 = subprocess.check_output(cmd2.split())
        logger.info(slimlog2)

    except subprocess.CalledProcessError as e:
        logger.error(e.output)

    sys.stdout.flush()
    sys.stderr.flush()


def get_ua():
    uap = argparse.ArgumentParser(
        description="Simulates selection for training Timesweeper using a pre-made SLiM script."
    )
    uap.add_argument(
        "--threads",
        required=False,
        type=int,
        default=mp.cpu_count(),
        dest="threads",
        help="Number of processes to parallelize across. Defaults to all.",
    )
    uap.add_argument(
        "--rep-range",
        required=False,
        dest="rep_range",
        nargs=2,
        help="<start, stop>. If used, only range(start, stop) will be simulated for reps. \
            This is to allow for easy SLURM parallel simulations.",
    )
    subparsers = uap.add_subparsers(dest="config_format")
    subparsers.required = True
    yaml_parser = subparsers.add_parser("yaml")
    yaml_parser.add_argument(
        metavar="YAML_CONFIG",
        dest="yaml_file",
        help="YAML config file with all cli options defined.",
    )

    cli_parser = subparsers.add_parser("cli")
    cli_parser.add_argument(
        "-w",
        "--work-dir",
        dest="work_dir",
        type=str,
        help="Directory used as work dir for simulate modules. Should contain simulated vcfs processed using process_vcf.py.",
        required=False,
        default=os.getcwd(),
    )
    cli_parser.add_argument(
        "-i",
        "--slim-file",
        required=True,
        type=str,
        help="SLiM Script to simulate with. Must output to a single VCF file. ",
        dest="slim_file",
    )
    cli_parser.add_argument(
        "--reps",
        required=False,
        type=int,
        help="Number of replicate simulations to run if not using rep-range.",
        dest="reps",
    )
    return uap.parse_args()


def main(ua):
    """
    For simulating non-stdpopsim SLiMfiles.
    Currently only works with 1 pop models where m2 is the sweep mutation.
    Otherwise everything else is identical to stdpopsim version, just less complex.

    Generalized block of '-d' arguments to give to SLiM at the command line allow for 
    flexible script writing within the context of this wrapper. If you write your SLiM script
    to require args set at runtime, this should be easily modifiable to do what you need and 
    get consistent results to plug into the rest of the workflow.

    The two things you *will* need to specify in your '-d' args to SLiM (and somewhere in the slim script) are:
    - sweep [str] One of "neut", "hard", or "soft". If you're testing only a neut/hard model, 
        make the soft a dummy switch for the neutral scenario.
    - outFile [path] You will need to define this as a population outputVCFSample input, with replace=T and append=T. 
        This does *not* need to be specified by you in the custom -d block, it will be standardized to work with the rest of the pipeline using work_dir.
        example line for slim script: `p1.outputVCFSample(sampleSizePerStep, replace=F, append=T, filePath=outFile);`
        
    Please note that since this is supposed to be modifiable I am leaving it as a cli-argument module only.
    This means that you will have to replicate any args this may share with the YAML you use for the rest of the workflow, if that's how you choose to run it.
    This also means, however, that you 
    """
    if ua.config_format == "yaml":
        yaml_data = read_config(ua.yaml_file)
        work_dir, slim_file, reps, rep_range = (
            yaml_data["work dir"],
            yaml_data["slimfile"],
            yaml_data["reps"],
            ua.rep_range,
        )
    elif ua.config_format == "cli":
        work_dir, slim_file, reps, rep_range = (
            ua.work_dir,
            ua.slim_file,
            ua.reps,
            ua.rep_range,
        )

    work_dir = work_dir
    vcf_dir = f"{work_dir}/vcfs"
    dumpfile_dir = f"{work_dir}/dumpfiles"
    params_dir = f"{work_dir}/params"

    sweeps = ["neut", "soft"]

    for i in [vcf_dir, dumpfile_dir, params_dir]:
        for sweep in sweeps:
            os.makedirs(f"{i}/{sweep}", exist_ok=True)

    mp_args = []
    # Inject info into SLiM script and then simulate, store params for reproducibility
    if rep_range:  # Take priority
        replist = range(int(rep_range[0]), int(rep_range[1]) + 1)
    else:
        replist = range(reps)

    for rep in replist:
        for sweep in sweeps:
            if not os.path.exists(f"{vcf_dir}/{sweep}/{rep}.multivcf"):
                outFile = f"{vcf_dir}/{sweep}/{rep}.multivcf"
                dumpFile = f"{dumpfile_dir}/{sweep}/{rep}.dump"

                # Grab those constants to feed to SLiM
                d_block_burn, d_block_sel = make_d_block(sweep, outFile, dumpFile, True)

                mp_args.append((slim_file, d_block_burn, d_block_sel))

    pool = mp.Pool(processes=ua.threads)
    pool.starmap(run_slim, mp_args, chunksize=5)

    # Log the constant params
    with open(f"{params_dir}/{sweep}/slim_params_{rep}.txt", "w") as paramsfile:
        cleaned_block = "\n".join(
            [i.strip() for i in d_block_sel.split() if "-d" not in i]
        )
        paramsfile.writelines(cleaned_block)

    # Cleanup
    for rep in replist:
        for sweep in sweeps:
            dumpFile = f"{dumpfile_dir}/{sweep}/{rep}.dump"
            os.remove(dumpFile)

    logger.info(
        f"Simulations finished, parameters saved to {work_dir}/slim_params.csv."
    )


if __name__ == "__main__":
    ua = get_ua()
    main(ua)

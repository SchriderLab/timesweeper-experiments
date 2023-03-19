import argparse
import logging
import multiprocessing as mp
import os
import subprocess
import sys
import yaml
import numpy as np
from glob import glob 
logging.basicConfig()
logger = logging.getLogger("simple_simulate")
logger.setLevel("INFO")


def read_config(yaml_file):
    """Reads in the YAML config file."""
    with open(yaml_file, "r") as infile:
        yamldata = yaml.safe_load(infile)

    return yamldata


def randomize_selCoeff_uni(lower_bound=0.00025, upper_bound=0.25):
    """Draws selection coefficient from log uniform dist to vary selection strength."""
    rng = np.random.default_rng(
        np.random.seed(int.from_bytes(os.urandom(4), byteorder="little"))
    )

    return rng.uniform(lower_bound, upper_bound, 1)[0]


def randomize_sampGens(num_timepoints, dev=50, span=200):
    rng = np.random.default_rng(
        np.random.seed(int.from_bytes(os.urandom(4), byteorder="little"))
    )
    start = round(rng.uniform(-dev, dev, 1)[0])
    if num_timepoints == 1:
        sampGens = [start + span]
    else:
        sampGens = [
            round(i) for i in np.linspace(start, start + span + 1, num_timepoints)
        ]

    return sampGens


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
    num_sample_points = 20

    selCoeff = randomize_selCoeff_uni()
    sampGens = [str(i) for i in randomize_sampGens(num_sample_points)]

    inds_per_tp = 10  # Diploid inds
    physLen = 500000
    burnPopSize = 10000 / 5
    seed = int(rng.uniform(0, 1e16))

    Q = 5
    d_block_burn = f"""\
    -d "sweep='{sweep}'" \
    -d "outFile='{outFile}'" \
    -d "dumpFile='{dumpfile}'" \
    -d burnPopSize={int(burnPopSize)} \
    -d mutationRate={Q*1e-7} \
    -d selCoeff={selCoeff * Q} \
    -d sampGens='c({','.join(sampGens)})' \
    -d Q={Q} \
    -d sampleSizePerStep={inds_per_tp} \
    -d physLen={physLen} \
    -d seed={seed} \
    """

    Q = 1
    d_block_sel = f"""\
    -d "sweep='{sweep}'" \
    -d "outFile='{outFile}'" \
    -d "dumpFile='{dumpfile}'" \
    -d burnPopSize={int(burnPopSize)} \
    -d mutationRate={Q*1e-7} \
    -d selCoeff={selCoeff * Q} \
    -d sampGens='c({','.join(sampGens)})' \
    -d Q={Q} \
    -d sampleSizePerStep={inds_per_tp} \
    -d physLen={physLen} \
    -d seed={seed} \
    """

    return d_block_burn, d_block_sel


def run_slim(d_block_burn, d_block_sel, logfile):

    cmd1 = " ".join(
        ["time slim", d_block_burn, "bottleneck_burn.slim", ">>", logfile]
    ).replace("    ", "")
    cmd2 = " ".join(
        ["time slim", d_block_sel, "bottleneck_selection.slim", ">>", logfile]
    ).replace("    ", "")

    with open(logfile, "w") as ofile:
        ofile.write(cmd1 + "\n")
        ofile.write(cmd2 + "\n")

    try:
        slimlog1 = subprocess.run(cmd1, shell=True)
        slimlog2 = subprocess.check_output(cmd2, shell=True)

    except subprocess.CalledProcessError as e:
        logger.error(e.output)

    sys.stdout.flush()
    sys.stderr.flush()


# VCF Processing
def read_multivcf(input_vcf):
    """Reads in file and returns as list of strings."""
    with open(input_vcf, "r") as input_file:
        raw_lines = [i.strip() for i in input_file.readlines()]

    return raw_lines


def split_multivcf(vcf_lines, header):
    """Splits the lines of multi-vcf file into list of vcf entries by <header> using itertools."""
    header_idxs = [i for i in range(len(vcf_lines)) if vcf_lines[i] == header]

    split_vcfs = []
    for idx in range(len(header_idxs[:-1])):
        split_vcfs.append(vcf_lines[header_idxs[idx] : header_idxs[idx + 1]])

    split_vcfs.append(vcf_lines[header_idxs[-1] :])

    return split_vcfs


def write_vcfs(vcf_lines, vcf_dir):
    """Writes list of vcf entries to numerically-sorted vcf files."""
    for idx, lines in enumerate(vcf_lines):
        with open(os.path.join(vcf_dir, f"{idx}.vcf"), "w") as outfile:
            outfile.writelines("\n".join(lines))


def index_vcf(vcf):
    """
    Indexes and sorts vcf file.
    Commands are run separately such that processes complete before the next one starts.
    """
    bgzip_cmd = f"bgzip -c {vcf} > {vcf}.gz"
    tabix_cmd = f"tabix -f -p vcf {vcf}.gz"
    bcftools_cmd = f"bcftools sort -Ov {vcf}.gz | bgzip -f > {vcf}.sorted.gz"
    tabix_2_cmd = f"tabix -f -p vcf {vcf}.sorted.gz"
    subprocess.run(
        bgzip_cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    )
    subprocess.run(
        tabix_cmd.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    )
    subprocess.run(
        bcftools_cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    )
    subprocess.run(
        tabix_2_cmd.split(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    )


def merge_vcfs(vcf_dir):
    num_files = len(glob(f"{vcf_dir}/*.vcf.sorted.gz"))
    if num_files == 1:
        cmd = f"""zcat {f"{vcf_dir}/0.vcf.sorted.gz"} > {vcf_dir}/merged.vcf"""

    else:
        cmd = f"""bcftools merge -Ov -0 \
                --force-samples --info-rules 'MT:join,S:join' \
                {" ".join([f"{vcf_dir}/{i}.vcf.sorted.gz" for i in range(num_files)])} > \
                {vcf_dir}/merged.vcf \
                """

    subprocess.run(cmd, shell=True)


def make_vcf_dir(input_vcf):
    """Creates directory named after vcf basename."""
    dirname = os.path.basename(input_vcf).split(".")[0]
    dirpath = os.path.dirname(input_vcf)
    vcf_dir = os.path.join(dirpath, dirname)
    if os.path.exists(vcf_dir):
        for ifile in glob(f"{vcf_dir}/*"):
            os.remove(ifile)

    os.makedirs(vcf_dir, exist_ok=True)

    final_vcf = f"{input_vcf}.final"
    if os.path.exists(final_vcf):
        os.rename(final_vcf, f"{vcf_dir}/{final_vcf.split('/')[-1]}")

    return vcf_dir


def process_vcfs(input_vcf, num_tps):
    try:
        # Split into multiples after SLiM just concats to same file
        raw_lines = read_multivcf(input_vcf)
        split_lines = split_multivcf(raw_lines, "##fileformat=VCFv4.2")
        if len(split_lines) > 0:
            split_lines = split_lines[len(split_lines) - num_tps :]

            # Creates subdir for each rep
            vcf_dir = make_vcf_dir(input_vcf)
            write_vcfs(split_lines, vcf_dir)

            # Now index and merge
            [index_vcf(vcf) for vcf in glob(f"{vcf_dir}/*.vcf")]
            merge_vcfs(vcf_dir)

            cleanup_intermed(vcf_dir)

    except Exception as e:
        print(f"[ERROR] Couldn't process {e}")
        pass

def cleanup_intermed(vcf_dir):
    for ifile in glob(f"{vcf_dir}/*"):
        if "merged" not in ifile and "final" not in ifile:
            pass
            os.remove(ifile)
            
def simulate_prep(
    vcf_file, d_block_burn, d_block_sel, logfile, dumpFile
):
    run_slim(d_block_burn, d_block_sel, logfile)
    os.remove(dumpFile)

    process_vcfs(vcf_file, 20)
    os.remove(vcf_file)


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

    uap.add_argument(
        "-y",
        metavar="YAML_CONFIG",
        dest="yaml_file",
        help="YAML config file with all cli options defined.",
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
    - sweep [str] One of "neut", "sdn", or "ssv". If you're testing only a neut/sdn model, 
        make the ssv a dummy switch for the neutral scenario.
    - outFile [path] You will need to define this as a population outputVCFSample input, with replace=F and append=T. 
        This does *not* need to be specified by you in the custom -d block, it will be standardized to work with the rest of the pipeline using work_dir.
        example line for slim script: `p1.outputVCFSample(sampleSizePerStep, replace=F, append=T, filePath=outFile);`
        
    Please note that since this is supposed to be modifiable I am leaving it as a cli-argument module only.
    This means that you will have to replicate any args this may share with the YAML you use for the rest of the workflow, if that's how you choose to run it.
    This also means, however, that you 
    """

    yaml_data = read_config(ua.yaml_file)
    work_dir, slim_file, reps, rep_range = (
        yaml_data["work dir"],
        yaml_data["slimfile"],
        yaml_data["reps"],
        ua.rep_range,
    )

    work_dir = work_dir
    vcf_dir = f"{work_dir}/vcfs"
    dumpfile_dir = f"{work_dir}/dumpfiles"
    logfile_dir = f"{work_dir}/logs"

    sweeps = ["neut", "sdn", "ssv"]

    for i in [vcf_dir, dumpfile_dir, logfile_dir]:
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
            outFile = f"{vcf_dir}/{sweep}/{rep}.multivcf"
            dumpFile = f"{dumpfile_dir}/{sweep}/{rep}.dump"
            logFile = f"{logfile_dir}/{sweep}/{rep}.log"

            # Grab those constants to feed to SLiM
            d_block_burn, d_block_sel = make_d_block(sweep, outFile, dumpFile, True)

            mp_args.append(
                (
                    outFile,
                    d_block_burn,
                    d_block_sel,
                    logFile,
                    dumpFile,
                )
            )
            
    pool = mp.Pool(processes=ua.threads)
    pool.starmap(simulate_prep, mp_args, chunksize=5)

    # Cleanup
    for rep in replist:
        for sweep in sweeps:
            dumpFile = f"{dumpfile_dir}/{sweep}/{rep}.dump"
            os.remove(dumpFile)

    logger.info(f"Simulations finished")


if __name__ == "__main__":
    ua = get_ua()
    main(ua)
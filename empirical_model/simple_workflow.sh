#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=8G
#SBATCH -c 5
#SBATCH --time=4:00:00
#SBATCH -J classify
#SBATCH -o logfiles/sims/simulate.%A.%a.out
#SBATCH -e logfiles/sims/simulate.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500:10
conda activate blinx

srcdir=/proj/dschridelab/lswhiteh/timesweeper/src
configfile=OoA_config.yaml

python ${srcdir}/simulate_stdpopsim.py --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+100)) yaml ${configfile}
#python ${srcdir}/process_vcfs.py yaml ${configfile}
#python ${srcdir}/make_training_features.py yaml ${configfile}
#python ${srcdir}/nets.py -n mongolian_samples yaml ${configfile}

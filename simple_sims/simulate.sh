#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=16G
#SBATCH -c 4
#SBATCH --time=24:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/sims/workflow.%A.%a.out
#SBATCH -e logfiles/sims/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500:10
conda init bash
conda activate blinx
source activate blinx

srcdir=/proj/dschridelab/lswhiteh/timesweeper/src
configfile=OoA_config.yaml

#python ${srcdir}/simulate_stdpopsim.py --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+100)) yaml ${configfile}
python ${srcdir}/process_vcfs.py yaml ${configfile}
python ${srcdir}/make_training_features.py yaml ${configfile}
python ${srcdir}/nets.py -n mongolian_samples yaml ${configfile}
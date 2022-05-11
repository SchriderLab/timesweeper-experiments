#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=8G
#SBATCH -c 8
#SBATCH --time=8:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500:5
conda init bash
conda activate blinx
source activate blinx

cd /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=OoA_config.yaml

python ${srcdir}/simulate_stdpopsim.py --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+10)) yaml ${configfile}
#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=8G
#SBATCH -c 16
#SBATCH --time=8:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2490:10
conda init bash
conda activate blinx
source activate blinx

configfile=d_simulans_config.yaml

python Timesweeper/timesweeper/simulate_custom --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+10)) yaml ${configfile}
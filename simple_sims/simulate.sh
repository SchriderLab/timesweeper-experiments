#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=8G
#SBATCH -c 2
#SBATCH --time=12:00:00
#SBATCH -J k51_sim
#SBATCH -o logfiles/sims/k51.%A.%a.out
#SBATCH -e logfiles/sims/k51.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-10000:50

conda activate blinx
source activate blinx
timesweeper sim_custom --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+50)) -y config.yaml

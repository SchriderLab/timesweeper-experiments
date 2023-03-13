#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=1G
#SBATCH -c 3
#SBATCH --time=2-00:00:00
#SBATCH -J k51_sim
#SBATCH -o logfiles/sims/k51.%A.%a.out
#SBATCH -e logfiles/sims/k51.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=1-5001:2

conda activate blinx
source activate blinx
timesweeper sim_custom --rep-range ${SLURM_ARRAY_TASK_ID} ${SLURM_ARRAY_TASK_ID} -y config.yaml --threads 3

#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=8G
#SBATCH -c 2
#SBATCH --time=12:00:00
#SBATCH -J 100tp_sim
#SBATCH -o logfiles/sims/100tp.%A.%a.out
#SBATCH -e logfiles/sims/100tp.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-30000:50
conda activate blinx

timesweeper sim_custom --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+50)) -y config.yaml

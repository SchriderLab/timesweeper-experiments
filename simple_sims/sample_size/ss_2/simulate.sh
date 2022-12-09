#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=8G
#SBATCH -c 6
#SBATCH --time=6:00:00
#SBATCH -J ss2_sim
#SBATCH -o logfiles/sims/ss2.%A.%a.out
#SBATCH -e logfiles/sims/ss2.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-10000:50
conda init bash
conda activate blinx
source activate blinx


timesweeper sim_custom --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+50)) -y config.yaml

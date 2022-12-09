#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=8G
#SBATCH -c 6
#SBATCH --time=6:00:00
#SBATCH -J s0.05_sim
#SBATCH -o logfiles/sims/s0.05.%A.%a.out
#SBATCH -e logfiles/sims/s0.05.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-30000:50
conda init bash
conda activate blinx
source activate blinx


python simulate_custom.py --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+50)) -y config.yaml

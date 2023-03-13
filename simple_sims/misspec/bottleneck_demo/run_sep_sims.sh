#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=4G
#SBATCH -c 4
#SBATCH --time=2:00:00
#SBATCH -J sep_sim
#SBATCH -o logfiles/sims/sep_sim.%A.%a.out
#SBATCH -e logfiles/sims/sep_sim.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-5000:5
conda init bash
conda activate blinx
source activate blinx


time python simulate_custom.py --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+5)) -y misspec.yaml --threads 4

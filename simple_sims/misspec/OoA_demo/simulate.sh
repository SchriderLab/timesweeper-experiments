#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=8G
#SBATCH -c 4
#SBATCH --time=8:00:00
#SBATCH -J OoA_test
#SBATCH -o logfiles/sims/OoA_test.%A.%a.out
#SBATCH -e logfiles/sims/OoA_test.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-5000:5
conda init bash
conda activate blinx
source activate blinx


timesweeper sim_stdpopsim --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+5)) OoA_test.yaml

#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=1G
#SBATCH -c 1
#SBATCH --time=2:00:00
#SBATCH -J stat_methods
#SBATCH -o logfiles/stat_methods.%A.%a.out
#SBATCH -e logfiles/stat_methods.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-4950:50
conda init bash
conda activate blinx
source activate blinx

for r in $(seq ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+50)))
do
    python stat_methods.py -r ${r}
done
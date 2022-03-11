#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=8G
#SBATCH -c 6
#SBATCH --time=6:00:00
#SBATCH -J 5tp_sim
#SBATCH -o logfiles/sims/5tp.%A.%a.out
#SBATCH -e logfiles/sims/5tp.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500:10
conda init bash
conda activate blinx
source activate blinx

configfile=config.yaml
python simulate_custom.py --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+10)) yaml ${configfile}

#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=8G
#SBATCH -c 4
#SBATCH --time=2:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500:5
conda init bash
conda activate blinx
source activate blinx

configfile=d_simulans_config.yaml
cd ..
python simulate_custom.py --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+5)) yaml ${configfile}
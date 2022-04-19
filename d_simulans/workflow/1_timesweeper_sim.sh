#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=4G
#SBATCH -c 2
#SBATCH --time=8:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/sim.%A.%a.out
#SBATCH -e logfiles/sim.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500
conda init bash
conda activate blinx
source activate blinx

configfile=d_simulans_config.yaml
cd ..

python simulate_custom.py --rep-range ${SLURM_ARRAY_TASK_ID} ${SLURM_ARRAY_TASK_ID} yaml ${configfile}
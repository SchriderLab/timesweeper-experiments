#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=2G
#SBATCH -c 1
#SBATCH --time=2:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/sims/sim.%A.%a.out
#SBATCH -e logfiles/sims/sim.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500
conda init bash
conda activate blinx
source activate blinx

configfile=d_simulans_config.yaml
cd ..

#using custom 2-stage burn/selection launcher
python simulate_custom.py --rep-range ${SLURM_ARRAY_TASK_ID} ${SLURM_ARRAY_TASK_ID} yaml ${configfile}
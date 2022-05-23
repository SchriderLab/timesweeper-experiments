#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=16G
#SBATCH -c 4
#SBATCH --time=24:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/sims/workflow.%A.%a.out
#SBATCH -e logfiles/sims/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500:10
conda init bash
conda activate blinx
source activate blinx

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=OoA_config.yaml

#python ${srcdir}/simulate_stdpopsim.py --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+100)) yaml ${configfile}
timesweeper process yaml ${configfile}
timesweeper condense -o training_data.pkl yaml ${configfile}
timesweeper train -i training_data.pkl -n mongolian_samples yaml ${configfile}

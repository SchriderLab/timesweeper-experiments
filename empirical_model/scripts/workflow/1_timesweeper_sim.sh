#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=4G
#SBATCH -c 4
#SBATCH --time=4:00:00
#SBATCH -J workflow
#SBATCH -o /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/scripts/workflow/logfiles/sims/simulate.%A.%a.out
#SBATCH -e /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/scripts/workflow/logfiles/sims/simulate.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2500
conda init bash
conda activate blinx
source activate blinx

cd /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=OoA_config.yaml

timesweeper sim_stdpopsim --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID}+1)) yaml ${configfile}
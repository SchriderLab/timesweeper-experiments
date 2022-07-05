#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=8G
#SBATCH -c 2
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

configfile=/pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/OoA_constant_sampling_config.yaml

timesweeper sim_stdpopsim --rep-range ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID} + 1)) yaml ${configfile}
#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=32G
#SBATCH -c 24
#SBATCH --time=4:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx

cd /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=OoA_config.yaml

#timesweeper process yaml ${configfile}
#timesweeper condense --hft -o training_data.pkl yaml ${configfile}
timesweeper train -i training_data.pkl --hft -n Neo_Mongolians yaml ${configfile}
timesweeper plot_training -i training_data.pkl -n Neo_Mongolians -o input_images
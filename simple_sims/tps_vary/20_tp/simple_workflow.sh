#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8 
#SBATCH --mem=128G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J tp20workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx
source activate blinx

#timesweeper summarize -n 20_Timepoints -y config.yaml
timesweeper condense --hft -o 20tp_training_data.pkl -y config.yaml
timesweeper train -i 20tp_training_data.pkl --hft -y config.yaml -s 10000
timesweeper plot_training -i 20tp_training_data.pkl -n 20_Timepoint -o 20_Timepoint/images
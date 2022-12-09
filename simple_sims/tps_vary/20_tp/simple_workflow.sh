#!/bin/bash
#SBATCH --partition=general
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


timesweeper condense --hft -o 20tp_training_data.pkl -y config.yaml --subsample-tps 20 --og-tps 100
timesweeper train -i 20tp_training_data.pkl -d aft -n 20_Timepoint -y config.yaml
timesweeper train -i 20tp_training_data.pkl -d hft -n 20_Timepoint -y config.yaml
timesweeper plot_training -i 20tp_training_data.pkl -n 20_Timepoint -o 20_Timepoint/images
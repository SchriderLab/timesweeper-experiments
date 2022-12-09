#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=128G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J tp5workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
source activate blinx
conda activate blinx


timesweeper condense --hft -o 5tp_training_data.pkl -y config.yaml --subsample-tps 5 --og-tps 100
timesweeper train -i 5tp_training_data.pkl -d aft -n 5_Timepoint -y config.yaml
timesweeper train -i 5tp_training_data.pkl -d hft -n 5_Timepoint -y config.yaml
timesweeper plot_training -i 5tp_training_data.pkl -n 5_Timepoint -o 5_Timepoint/images
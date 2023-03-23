#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=128G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J tp2workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx
source activate blinx

timesweeper summarize -n 2_Timepoints -y config.yaml
timesweeper condense --hft -o 2tp_training_data.pkl -y config.yaml
timesweeper train -i 2tp_training_data.pkl --hft -y config.yaml
timesweeper plot_training -i 2tp_training_data.pkl -n 2_Timepoint -o 2_Timepoint/images
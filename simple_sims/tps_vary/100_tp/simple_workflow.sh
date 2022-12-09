#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=128G
#SBATCH -c 16
#SBATCH --time=7-00:00:00
#SBATCH -J tp100workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx
source activate blinx


timesweeper condense --hft -o 100tp_training_data.pkl -y config.yaml
timesweeper train -i 100tp_training_data.pkl -d aft -n 100_Timepoint -y config.yaml
timesweeper train -i 100tp_training_data.pkl -d hft -n 100_Timepoint -y config.yaml
timesweeper plot_training -i 100tp_training_data.pkl -n 100_Timepoint -o 100_Timepoint/images
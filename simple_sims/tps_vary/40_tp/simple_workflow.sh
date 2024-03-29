#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=128G
#SBATCH -c 16
#SBATCH --time=2-00:00:00
#SBATCH -J tp40workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx
source activate blinx

#timesweeper summarize -n 40_Timepoints -y config.yaml
timesweeper condense --hft -o 40tp_training_data.pkl -y config.yaml
timesweeper train -i 40tp_training_data.pkl -d aft -n 40_Timepoints -y config.yaml
timesweeper train -i 40tp_training_data.pkl -d hft -n 40_Timepoints -y config.yaml
timesweeper plot_training -i 40tp_training_data.pkl -n 40_Timepoints -o 40_tp_sims/images/inputs
#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=32G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J s0.01workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx

tar -xzf vcfs.tar.gz
timesweeper condense --hft -o 001selcoeff_training_data.pkl -y config.yaml
timesweeper train -i 001selcoeff_training_data.pkl -d aft -n Sel_Coeff_0.01 -y config.yaml
timesweeper train -i 001selcoeff_training_data.pkl -d hft -n Sel_Coeff_0.01 -y config.yaml
timesweeper plot_training -i 001selcoeff_training_data.pkl -n Sel_Coeff_0.01 -o Sel_Coeff_0.01/images
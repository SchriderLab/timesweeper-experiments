#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=64G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J s0.005workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx
source activate blinx


timesweeper condense --hft -o 0005selcoeff_training_data.pkl -y config.yaml
timesweeper train -i 0005selcoeff_training_data.pkl --hft -y config.yaml
timesweeper plot_training -i 0005selcoeff_training_data.pkl -n Sel_Coeff_0.005 -o Sel_Coeff_0.005/images
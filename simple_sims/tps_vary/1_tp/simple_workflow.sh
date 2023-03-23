#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8 
#SBATCH --mem=64G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J tp1workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx
source activate blinx

timesweeper condense --hft -o new_1tp_training_data.pkl -y config.yaml
timesweeper train -i new_1tp_training_data.pkl --hft -y config.yaml
timesweeper plot_training -i new_1tp_training_data.pkl -n 1_Timpeoint -o 1_Timpeoint/images
#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=64G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx

timesweeper condense --hft -o k201_training_data.pkl -y config.yaml
timesweeper train -i k201_training_data.pkl --hft -y config.yaml
timesweeper plot_training -i k201_training_data.pkl  -o Win_size_201/images

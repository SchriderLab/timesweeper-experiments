#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=32G
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




timesweeper condense --hft -o k101_training_data.pkl -y config.yaml
timesweeper train -i k101_training_data.pkl -d aft -n Win_size_101 -y config.yaml
timesweeper train -i k101_training_data.pkl -d hft -n Win_size_101 -y config.yaml
timesweeper plot_training -i k101_training_data.pkl -n Win_size_101 -o Win_size_101/images
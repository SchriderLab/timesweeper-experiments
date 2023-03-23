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
##SBATCH --array=0-10000:50
conda init bash
conda activate blinx
source activate blinx

timesweeper condense --hft -o k11_training_data.pkl -y config.yaml --threads 16
timesweeper train -i k11_training_data.pkl --hft -y config.yaml
timesweeper plot_training -i k11_training_data.pkl  -o Win_size_11/images

#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=32G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J k1_workflow
#SBATCH -o logfiles/k1_workflow.%A.%a.out
#SBATCH -e logfiles/k1_workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx



timesweeper condense --hft -o training_data.pkl -y config.yaml
timesweeper train -i training_data.pkl --hft -y config.yaml -s 10000
timesweeper plot_training -i training_data.pkl -o Win_size_1/images

#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=32G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J ss5workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx


timesweeper condense --hft -o 5tp_training_data.pkl -y config.yaml --subsample-inds 5
timesweeper train -i 5tp_training_data.pkl -d aft -n Sample_Size_5 -y config.yaml
timesweeper train -i 5tp_training_data.pkl -d hft -n Sample_Size_5 -y config.yaml
timesweeper plot_training -i 5tp_training_data.pkl -n Sample_Size_5 -o sample_size_5/images
#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=64G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J k201shoulders
#SBATCH -o logfiles/k201shoulders.%A.%a.out
#SBATCH -e logfiles/k201shoulders.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx


timesweeper condense --hft -o shoulder_k201_training_data.pkl -y config.yaml --allow-shoulders 
timesweeper train -i shoulder_k201_training_data.pkl -d aft -n Shoulder_Win_size_201 -y config.yaml
timesweeper train -i shoulder_k201_training_data.pkl -d hft -n Shoulder_Win_size_201 -y config.yaml
timesweeper plot_training -i shoulder_k201_training_data.pkl -n Shoulder_Win_size_201 -o Shoulder_Win_size_201/images
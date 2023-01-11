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
source activate blinx

conda activate blinx



#timesweeper condense --hft -o ../20tp_training_data.pkl -y config.yaml --subsample-reps 5000
timesweeper train -i ../20tp_training_data.pkl -d aft -n Reps_Size_5k -y config.yaml --subsample-amount 5000
timesweeper train -i ../20tp_training_data.pkl -d hft -n Reps_Size_5k -y config.yaml --subsample-amount 5000
timesweeper plot_training -i ../20tp_training_data.pkl -n Reps_Size_5k -o Reps_Size_5k/images
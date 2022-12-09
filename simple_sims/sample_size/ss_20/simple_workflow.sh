#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=64G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J ss20workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
##SBATCH --array=0-30000:50
conda init bash
conda activate blinx
source activate blinx


timesweeper condense --hft -o 20ss_training_data.pkl -y config.yaml
timesweeper train -i 20ss_training_data.pkl -d aft -n Sample_Size_20 -y config.yaml
timesweeper train -i 20ss_training_data.pkl -d hft -n Sample_Size_20 -y config.yaml
timesweeper plot_training -i 20ss_training_data.pkl -n Sample_Size_20 -o sample_size_20/images
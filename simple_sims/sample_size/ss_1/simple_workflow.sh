#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=32G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J ss1_workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
##SBATCH --array=0-10000:50
conda init bash
conda activate blinx
source activate blinx




timesweeper condense --hft -o 1ss_training_data.pkl -y config.yaml --subsample-inds 1
timesweeper train -i 1ss_training_data.pkl -d aft -n Sample_Size_1 -y config.yaml
timesweeper train -i 1ss_training_data.pkl -d hft -n Sample_Size_1 -y config.yaml
timesweeper plot_training -i 1ss_training_data.pkl -n Sample_Size_1 -o sample_size_1/images

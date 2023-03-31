#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8 
#SBATCH --mem=64G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J ss20workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx

#timesweeper summarize -n Sample_Sizes -y config.yaml
timesweeper condense --hft -o 20ss_training_data.pkl -y config.yaml --threads 16
timesweeper train -i 20ss_training_data.pkl --hft -y config.yaml
timesweeper plot_training -i 20ss_training_data.pkl -n Sample_Size_20 -o input_images
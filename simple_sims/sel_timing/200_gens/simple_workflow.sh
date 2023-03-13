#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=32G
#SBATCH -c 32
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


timesweeper summarize -n 200_Gens_Post -y config.yaml

timesweeper condense --hft -o 50gens_training_data.pkl -y config.yaml --threads 32
timesweeper train -i 50gens_training_data.pkl -d aft -n 200_Gens_Post -y config.yaml
timesweeper train -i 50gens_training_data.pkl -d hft -n 200_Gens_Post -y config.yaml
timesweeper plot_training -i 50gens_training_data.pkl -n 200_Gens_Post -o 200_Gens_Post/images
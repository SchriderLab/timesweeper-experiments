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

timesweeper summarize -n neg200_Gens_Post -y config.yaml

timesweeper condense --hft -o neg200gens_training_data.pkl -y config.yaml --threads 32
timesweeper train -i neg200gens_training_data.pkl -d aft -n neg200_Gens_Post -y config.yaml
timesweeper train -i neg200gens_training_data.pkl -d hft -n neg200_Gens_Post -y config.yaml
timesweeper plot_training -i neg200gens_training_data.pkl -n neg200_Gens_Post -o neg200_Gens_Post/images
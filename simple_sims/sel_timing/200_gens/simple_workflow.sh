#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=32G
#SBATCH -c 64
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


timesweeper condense --hft -o 200_gen_training_data.pkl -y config.yaml --threads 32
timesweeper train -i 200_gen.pkl -y config.yaml --hft
timesweeper plot_training -i 50gens_training_data.pkl  -o 200_Gens_Post/images
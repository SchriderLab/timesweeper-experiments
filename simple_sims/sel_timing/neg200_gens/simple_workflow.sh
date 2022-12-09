#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=16G
#SBATCH -c 32
#SBATCH --time=24:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
##SBATCH --array=0-30000:50
conda init bash
conda activate blinx
source activate blinx



#
##timesweeper condense --hft -o training_data.pkl -y config.yaml
#timesweeper train -i training_data.pkl --hft -n Post_Sel_25 -y config.yaml
timesweeper plot_training -i training_data.pkl -n Post_Sel_25 -o input_images
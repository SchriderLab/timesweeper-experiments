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
##SBATCH --array=0-30000:50
conda init bash
conda activate blinx
source activate blinx



timesweeper process -y config.yaml
timesweeper condense --hft -o uni_sel_training_data.pkl -y config.yaml
timesweeper train -i uni_sel_training_data.pkl --hft -n Sample_Size_10_uni_sel_benchmark -y config.yaml
timesweeper plot_training -i uni_sel_training_data.pkl -n Sample_Size_10_benchmark_uni_sel -o sample_size_10_benchmark_uni_sel/images

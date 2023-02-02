#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=128G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J bmworkflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
source activate blinx
conda activate blinx

timesweeper condense --hft -o testing_data.pkl -y test_config.yaml

timesweeper plot_training -i testing_data.pkl -n Test_Data -o Benchmark/images
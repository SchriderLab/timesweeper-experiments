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

timesweeper condense --hft -o benchmark_training_data.pkl -y config.yaml
timesweeper train -i benchmark_training_data.pkl -d aft -n Benchmark -y config.yaml
timesweeper train -i benchmark_training_data.pkl -d hft -n Benchmark -y config.yaml
timesweeper plot_training -i benchmark_training_data.pkl -n Benchmark -o Benchmark/images
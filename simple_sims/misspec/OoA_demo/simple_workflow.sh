#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8 
#SBATCH --mem=32G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J ss10workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx


#timesweeper condense --hft -o OoA_test_data.pkl -y OoA_test.yaml
timesweeper train -i OoA_constant_data.pkl --hft -y OoA_constant_sampling_config.yaml

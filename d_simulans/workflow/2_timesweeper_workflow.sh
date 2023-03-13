#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=24G
#SBATCH -c 24
#SBATCH --time=1:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx

cd ..

timesweeper condense --hft \
    -o ts_simulans/d_simulans.pkl \
    -y d_simulans_config.yaml \
    --threads 16
    
timesweeper train \
    -i ts_simulans/d_simulans.pkl \
    --hft \
    -y d_simulans_config.yaml 

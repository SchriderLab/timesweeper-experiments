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

configfile=d_simulans_config.-y

##

#0 threshold
timesweeper condense --hft \
    -o ts_simulans/d_simulans_log_uni_0_thresh_vel.pkl \
    -y config.yaml
    
#timesweeper train \
    -i ts_simulans/d_simulans_log_uni_0_thresh_vel.pkl \
    -n d_simulans_log_uni_0_thresh_vel \
    -y config.yaml

#25 threshold
##timesweeper condense --hft \
    -f 0.25 \
    -o ts_simulans/d_simulans_log_uni_25_thresh_vel.pkl \
    -y config.yaml
    
#timesweeper train \
    -i ts_simulans/d_simulans_log_uni_25_thresh_vel.pkl \
    -n d_simulans_log_uni_25_thresh_vel \
    -y config.yaml
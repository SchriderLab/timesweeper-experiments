#!/bin/bash
#SBATCH --partition=dschridelab
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

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=d_simulans_config.yaml

##timesweeper process yaml ${configfile}

#0 threshold
timesweeper condense --hft \
    -o ts_simulans/d_simulans_log_uni_0_thresh_vel.pkl \
    yaml ${configfile}
    
#timesweeper train \
    -i ts_simulans/d_simulans_log_uni_0_thresh_vel.pkl \
    -n d_simulans_log_uni_0_thresh_vel \
    yaml ${configfile}

#25 threshold
##timesweeper condense --hft \
    -f 0.25 \
    -o ts_simulans/d_simulans_log_uni_25_thresh_vel.pkl \
    yaml ${configfile}
    
#timesweeper train \
    -i ts_simulans/d_simulans_log_uni_25_thresh_vel.pkl \
    -n d_simulans_log_uni_25_thresh_vel \
    yaml ${configfile}
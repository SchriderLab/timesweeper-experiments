#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8 
#SBATCH --mem=32G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
##SBATCH --array=0-2500:10
conda init bash
conda activate blinx
source activate blinx

configfile=sampsize10_config.yaml

#timesweeper process yaml ${configfile}
#timesweeper condense --hft -o uni_sel_training_data.pkl yaml ${configfile}
timesweeper train -i uni_sel_training_data.pkl --hft -n Win_size_51 yaml ${configfile}
timesweeper plot_training -i uni_sel_training_data.pkl -n Win_size_51 -o Win_size_51/images
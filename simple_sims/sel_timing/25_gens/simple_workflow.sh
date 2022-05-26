#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=16G
#SBATCH -c 32
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

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=config.yaml

#timesweeper process yaml ${configfile}
timesweeper condense --hft -o training_data.pkl yaml ${configfile}
timesweeper train -i training_data.pkl --hft -n Post_Sel_25 yaml ${configfile}
timesweeper plot_training -i training_data.pkl -n Post_Sel_25 -o input_images

#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=16G
#SBATCH -c 16
#SBATCH --time=4:00:00
#SBATCH -J 5tp-workflow
#SBATCH -o logfiles/5tp_workflow.%A.%a.out
#SBATCH -e logfiles/5tp_workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
##SBATCH --array=0-2500:10
conda init bash
conda activate blinx
source activate blinx

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=config.yaml

timesweeper process yaml ${configfile}
timesweeper condense --hft -o training_data.pkl yaml ${configfile}
timesweeper train -i training_data.pkl --hft -n TPs_5 yaml ${configfile}
timesweeper plot_training -i training_data.pkl -n TPs_5 -o input_images

#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=16G
#SBATCH -c 16
#SBATCH --time=2:00:00
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

timesweeper condense --missingness 0.8 yaml ${configfile}
timesweeper train -i training_data.pkl -n m_0.8 yaml ${configfile}
python ${srcdir}/plotting/plot_input_data.py -i missingness_0.8/training_data.pkl -n Missingness_0.8 -o missingness_0.8/images/
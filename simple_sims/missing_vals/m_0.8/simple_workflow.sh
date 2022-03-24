#!/bin/bash
#SBATCH --partition=general
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

srcdir=/proj/dschridelab/lswhiteh/timesweeper/src
configfile=config.yaml

python ${srcdir}/make_training_features.py --missingness 0.8 yaml ${configfile}
python ${srcdir}/nets.py -n m_0.8 yaml ${configfile}
python ${srcdir}/plotting/plot_input_data.py -i missingness_0.8/training_data.pkl -s Missingness_0.8 -o missingness_0.8/images/
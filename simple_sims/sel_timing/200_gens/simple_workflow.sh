#!/bin/bash
#SBATCH --partition=general
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

srcdir=/proj/dschridelab/lswhiteh/timesweeper/src
configfile=config.yaml

python ${srcdir}/process_vcfs.py yaml ${configfile}
python ${srcdir}/make_training_features.py yaml ${configfile}
python ${srcdir}/nets.py -n 200gpost yaml ${configfile}

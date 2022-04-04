#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=8G
#SBATCH -c 16
#SBATCH --time=8:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx

cd /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model

srcdir=/proj/dschridelab/lswhiteh/timesweeper/src
configfile=OoA_config.yaml

python ${srcdir}/process_vcfs.py yaml ${configfile}
python ${srcdir}/make_training_features.py -m 0.1 yaml ${configfile}
python ${srcdir}/nets.py -n mongolian_samps_01  yaml ${configfile}
python ${srcdir}/plotting/plot_input_data.py -i mongolian_samples/training_data.pkl -n mongolian_samps_0.1 -o mongolian_samples/images/
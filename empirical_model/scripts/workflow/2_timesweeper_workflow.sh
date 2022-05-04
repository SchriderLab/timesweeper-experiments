#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=32G
#SBATCH -c 24
#SBATCH --time=4:00:00
#SBATCH -J workflow
#SBATCH -o ../logfiles/workflow.%A.%a.out
#SBATCH -e ../logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx

cd /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=OoA_config.yaml

#python ${srcdir}/process_vcfs.py yaml ${configfile}
python ${srcdir}/make_training_features.py -m 0.3 yaml ${configfile}
python ${srcdir}/nets.py -i training_data.pkl -n mongolian_samps_3  yaml ${configfile}
python ${srcdir}/plotting/plot_input_data.py -i mongolian_samples/training_data.pkl -n mongolian_samps_0.3 -o mongolian_samples/images/
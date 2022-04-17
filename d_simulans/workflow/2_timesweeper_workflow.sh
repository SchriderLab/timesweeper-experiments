#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=32G
#SBATCH -c 24
#SBATCH --time=4:00:00
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

python ${srcdir}/process_vcfs.py yaml ${configfile}
python ${srcdir}/make_training_features.py yaml ${configfile}
python ${srcdir}/nets.py -n d_simulans  yaml ${configfile}

#python ${srcdir}/plotting/plot_input_data.py -i ts_simulans/training_data.pkl -n mongolian_samps_0.43 -o mongolian_samples/images/
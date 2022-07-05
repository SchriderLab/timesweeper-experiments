#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=32G
#SBATCH -c 24
#SBATCH --time=4:00:00
#SBATCH -J workflow
#SBATCH -o workflow.%A.%a.out
#SBATCH -e workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx

cd /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model

srcdir=/proj/dschridelab/lswhiteh/timesweeper/timesweeper
configfile=OoA_constant_sampling_config.yaml

timesweeper process yaml ${configfile}
timesweeper condense --hft -o training_data_constant_uni_sel.pkl yaml ${configfile}
timesweeper train -i training_data_constant_uni_sel.pkl --hft -n OoA_Constant_uni_sel yaml ${configfile}
timesweeper plot_training -i training_data_constant_uni_sel.pkl -n OoA_Constant_uni_sel -o input_images
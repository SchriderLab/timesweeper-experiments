#!/bin/bash
#SBATCH --partition=general
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

configfile=OoA_constant_sampling_config.-y


timesweeper condense --hft -o training_data_constant_uni_sel.pkl -y config.yaml
timesweeper train -i training_data_constant_uni_sel.pkl --hft -n OoA_Constant_uni_sel -y config.yaml
timesweeper plot_training -i training_data_constant_uni_sel.pkl -n OoA_Constant_uni_sel -o input_images
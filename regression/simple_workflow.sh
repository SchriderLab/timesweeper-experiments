#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8 
#SBATCH --mem=32G
#SBATCH -c 16
#SBATCH --time=24:00:00
#SBATCH -J workflow
#SBATCH -o logfiles/workflow.%A.%a.out
#SBATCH -e logfiles/workflow.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda init bash
conda activate blinx
source activate blinx

configfile=config.yaml

timesweeper process ${configfile}
timesweeper condense --hft -o uni_sel_training_data.pkl ${configfile}
timesweeper train -i uni_sel_training_data.pkl --hft -n logtrans ${configfile}
timesweeper plot_training -i uni_sel_training_data.pkl -n Sample_Size_10_benchmark_uni_sel -o sample_size_10_benchmark_uni_sel/images

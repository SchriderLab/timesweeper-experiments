#!/bin/bash
#SBATCH --job-name=makeCmp
#SBATCH --time=2:00:00
#SBATCH --partition=general
#SBATCH --output=logs/d_simulans_output_rep_10_X.log
#SBATCH --mem=16G
#SBATCH --requeue
#SBATCH --export=ALL

python 5_makeComparisonFile.py ../../d_simulans_output/aft_X_10_preds.csv 10 X /proj/dschridelab/drosophila/simulansEAndR/aftInputsVelocity/dsim_chrom_X_rep_10.npz /pine/scr/d/s/dschride/data/timeSeriesSweeps/compareToFETOut/rep10ScoreCompX_d_simulans_output.txt

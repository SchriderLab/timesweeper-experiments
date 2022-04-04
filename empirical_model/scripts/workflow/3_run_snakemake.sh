#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=64G
#SBATCH -c 32
#SBATCH --time=2-00:00:00
#SBATCH -J merge_proc_vcf
#SBATCH -o /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/scripts/logfiles/snakemake.%A.out
#SBATCH -e /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/scripts/logfiles/snakemake.%A.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

cd /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model

conda activate blinx
source activate blinx

snakemake -c all --rerun-incomplete
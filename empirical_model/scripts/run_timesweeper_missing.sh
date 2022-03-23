#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH -c 8
#SBATCH --time=2-00:00:00
#SBATCH -J run_timesweeper_missing
#SBATCH -o run_timesweeper_missing.%A.out
#SBATCH -e run_timesweeper_missing.%A.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

source activate blinx
conda activate blinx

python /proj/dschridelab/lswhiteh/timesweeper/src/timesweeper.py \
    -i vcfs/merged/ts_merged_missing.filtered.calls.vcf.gz \
    --afs-model mongolian_samples/trained_models/mongolian_samples_TimeSweeper_afs \
    --hfs-model mongolian_samples/trained_models/mongolian_samples_TimeSweeper_hfs \
    yaml OoA_missing_config.yaml 
 
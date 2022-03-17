#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=128G
#SBATCH --ntasks=4
#SBATCH --time=2-00:00:00
#SBATCH -J run_timesweeper
#SBATCH -o run_timesweeper.%A.out
#SBATCH -e run_timesweeper.%A.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

source activate blinx
conda activate blinx

#tabix ts_merged.calls.vcf.gz
python /proj/dschridelab/lswhiteh/timesweeper/src/timesweeper.py \
    -i ts_merged.calls.vcf.gz \
    --afs-model mongolian_samples/trained_models/mongolian_samples_TimeSweeper_afs \
    --hfs-model mongolian_samples/trained_models/mongolian_samples_TimeSweeper_hfs \
    yaml OoA_config.yaml
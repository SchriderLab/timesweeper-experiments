#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=16G
#SBATCH --ntasks=1
#SBATCH -c 4
#SBATCH --time=2-00:00:00
#SBATCH -J run_timesweeper_0s
#SBATCH -o /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/logfiles/run_timesweeper.%A.out
#SBATCH -e /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/logfiles/run_timesweeper.%A.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

source activate blinx
conda activate blinx

cd /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model
python /proj/dschridelab/lswhiteh/timesweeper/src/timesweeper.py \
    -i /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/vcfs/merged/ts_merged.filtered.calls.vcf.gz \
    --aft-model /pine/scr/l/s/lswhiteh/timesweeper-experiments/empirical_model/mongolian_samples/trained_models/mongolian_samples_TimeSweeper_aft \
    yaml OoA_config.yaml 
 
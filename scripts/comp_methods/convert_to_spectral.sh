#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=2G
#SBATCH -c 1
#SBATCH --time=2:00:00
#SBATCH -J spectralrun
#SBATCH -o logfiles/spectralrun.%A.%a.out
#SBATCH -e logfiles/spectralrun.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-5000
conda init bash
conda activate blinx
source activate blinx

python run_spectral.py -l /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/Test_Benchmark_params.tsv -t /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/testing_data.pkl -r ${SLURM_ARRAY_TASK_ID}
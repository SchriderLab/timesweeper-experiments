#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=32G
#SBATCH -c 1
#SBATCH --time=2:00:00
#SBATCH -J ts_predict
#SBATCH -o logfiles/ts_predict.%A.%a.out
#SBATCH -e logfiles/ts_predict.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-3000
conda init bash

for swp in neut sdn ssv
do
    timesweeper detect -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_data/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/merged.vcf \
    --aft-class-model /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/trained_models/Benchmark_Timesweeper_Class_aft \
    --aft-reg-model /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/trained_models/REG_Benchmark_sdn_minmax_Timesweeper_Reg_aft \
    --hft-class-model /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/trained_models/Benchmark_Timesweeper_Class_hft \
    --hft-reg-model /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/trained_models/REG_Benchmark_sdn_minmax_Timesweeper_Reg_hft \
    -o /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_data/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/ \
    -y /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_config.yaml \
    -s /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/Benchmark_selcoeff_scaler.pkl
done
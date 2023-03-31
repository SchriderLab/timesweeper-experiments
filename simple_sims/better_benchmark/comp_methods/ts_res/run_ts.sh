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
#SBATCH --array=0-5000
conda init bash
conda activate blinx
source activate blinx

cd /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark

for swp in neut sdn ssv
do
    timesweeper detect -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/merged.vcf \
    -o /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/ \
    -y config.yaml \
    --hft \
    --benchmark
done
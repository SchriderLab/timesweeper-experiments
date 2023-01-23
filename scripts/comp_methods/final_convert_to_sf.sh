#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=1G
#SBATCH -c 1
#SBATCH --time=4:00:00
#SBATCH -J sf_convert
#SBATCH -o logfiles/sf_conversion.%A.%a.out
#SBATCH -e logfiles/sf_conversion.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-10000
conda init bash
conda activate blinx
source activate blinx

python vcf2sf.py -v /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/neut/${SLURM_ARRAY_TASK_ID}.multivcf.final -o /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/neut/${SLURM_ARRAY_TASK_ID}.sf
python vcf2sf.py -v  /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/sdn/${SLURM_ARRAY_TASK_ID}.multivcf.final -o  /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/sdn/${SLURM_ARRAY_TASK_ID}.sf
python vcf2sf.py -v  /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/ssv/${SLURM_ARRAY_TASK_ID}.multivcf.final -o  /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/ssv/${SLURM_ARRAY_TASK_ID}.sf
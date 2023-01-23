#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=1G
#SBATCH -c 1
#SBATCH --time=2:00:00
#SBATCH -J shic_convert
#SBATCH -o logfiles/shic_conversion.%A.%a.out
#SBATCH -e logfiles/shic_conversion.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-10000
conda init bash
conda activate blinx
source activate blinx

python final_vcf_to_ms.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/neut/${SLURM_ARRAY_TASK_ID}.multivcf.final
python final_vcf_to_ms.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/sdn/${SLURM_ARRAY_TASK_ID}.multivcf.final
python final_vcf_to_ms.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/benchmark_sims/vcfs/ssv/${SLURM_ARRAY_TASK_ID}.multivcf.final
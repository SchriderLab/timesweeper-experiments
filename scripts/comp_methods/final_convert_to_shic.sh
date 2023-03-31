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
#SBATCH --array=0-9990:10
conda init bash
conda activate diploshic
source activate diploshic

for i in $(seq ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID} + 10)))
do
    python final_vcf_to_ms.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/train_benchmark/vcfs/neut/${i}/merged.vcf
    python final_vcf_to_ms.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/train_benchmark/vcfs/sdn/${i}/merged.vcf
    python final_vcf_to_ms.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/train_benchmark/vcfs/ssv/${i}/merged.vcf
done
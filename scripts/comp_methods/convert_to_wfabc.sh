#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=1G
#SBATCH -c 1
#SBATCH --time=2:00:00
#SBATCH -J wf_convert
#SBATCH -o logfiles/wfabc_conversion.%A.%a.out
#SBATCH -e logfiles/wfabc_conversion.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-5000
conda init bash
conda activate blinx
source activate blinx

python vcf_to_wfabc.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/neut/${SLURM_ARRAY_TASK_ID}/merged.vcf
python vcf_to_wfabc.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/sdn/${SLURM_ARRAY_TASK_ID}/merged.vcf
python vcf_to_wfabc.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/ssv/${SLURM_ARRAY_TASK_ID}/merged.vcf
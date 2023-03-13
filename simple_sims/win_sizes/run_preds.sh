#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=8G
#SBATCH -c 1
#SBATCH --time=1:00:00
#SBATCH -J win_size_predict
#SBATCH -o logfiles/predict.%A.%a.out
#SBATCH -e logfiles/predict.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-5000
conda activate blinx
source activate blinx

for swp in neut ssv sdn 
do 
    for size in 1 3 11 51 101 201
    do
        cd /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/win_sizes/k${size}

        echo Rep: $SLURM_ARRAY_TASK_ID
        echo Sweep: $swp 
        echo Size: $size
        echo 

        timesweeper detect -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/merged.vcf \
            --benchmark \
            -o /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/ \
            --hft \
            -y config.yaml
    done
done

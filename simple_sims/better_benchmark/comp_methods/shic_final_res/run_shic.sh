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
#SBATCH --array=0-5000
conda init bash
conda activate diploshic
source activate diploshic

for swp in neut sdn ssv
do
    for win in $(seq 0 10)
    do
        #diploSHIC fvecSim diploid \
        #/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/${SLURM_ARRAY_TASK_ID}.final.${swp}.win_${win}.msOut \
        #/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/${SLURM_ARRAY_TASK_ID}.final.${swp}.win_${win}.fvec

        diploSHIC predict --simData \
            /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/train_benchmark/shic_model.json \
            /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/train_benchmark/shic_model.weights.hdf5 \
            /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/${SLURM_ARRAY_TASK_ID}.final.${swp}.win_${win}.fvec \
            /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/${SLURM_ARRAY_TASK_ID}.final.${swp}.win_${win}.shicres.csv
    done
done
#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=8G
#SBATCH -c 1
#SBATCH --time=2:00:00
#SBATCH -J ts_predict
#SBATCH -o logfiles/ts_predict.%A.%a.out
#SBATCH -e logfiles/ts_predict.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-5000:50
conda init bash
conda activate blinx
source activate blinx

module load r

for i in $(seq $SLURM_ARRAY_TASK_ID $(($SLURM_ARRAY_TASK_ID+50)))
do
    for swp in neut sdn ssv
    do
        python vcf_to_slattice.py -i /work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${i}/merged.vcf
    done
done
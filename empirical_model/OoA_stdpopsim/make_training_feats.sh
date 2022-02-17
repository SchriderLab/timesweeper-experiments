#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=2G
#SBATCH --ntasks=1
#SBATCH --time=02:00:00
#SBATCH -J make_feats
#SBATCH -o logfiles/make_feats.%A.%a.out
#SBATCH -e logfiles/make_feats.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=1-2501:100

conda activate blinx
conda deactivate
conda activate blinx
source activate blinx

for i in hard neut soft
do  
    for id in $(seq ${SLURM_ARRAY_TASK_ID} $((${SLURM_ARRAY_TASK_ID} + 100)))
    do
        indir=sims/vcfs/${i}/${id}

        python /proj/dschridelab/lswhiteh/timesweeper/src/make_training_features.py cli \
        -s 5 2 1 3 3 3 1 3 4 3 3 3 4 3 4 3 3 4 8 5 \
        -p 2 \
        -i $indir/merged.vcf.gz \
        --sweep $i
    done
done

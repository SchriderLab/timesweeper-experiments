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
#SBATCH --array=0-5000
conda init bash
conda activate blinx
source activate blinx

for swp in neut sdn ssv
do
    ifile="/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/${SLURM_ARRAY_TASK_ID}.multivcf.final"
    freqfile="/work/users/l/s/lswhiteh/timesweeper-experiments/simple_sims/better_benchmark/test_benchmark/vcfs/${swp}/${SLURM_ARRAY_TASK_ID}/${SLURM_ARRAY_TASK_ID}.sf"
    spectfile="${freqfile}.fspect"
    resfile="${freqfile}.res"
    rm $resfile

    python vcf2sf.py -v $ifile -o $freqfile

    /work/users/l/s/lswhiteh/timesweeper-experiments/SF2/SweepFinder2 -f $freqfile $spectfile
    /work/users/l/s/lswhiteh/timesweeper-experiments/SF2/SweepFinder2 -l 1000 $freqfile $spectfile $resfile
done

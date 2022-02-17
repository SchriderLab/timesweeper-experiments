#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=8G
#SBATCH --ntasks=8
#SBATCH --time=00:30:00
#SBATCH -J train_nets
#SBATCH -o logfiles/train_nets.%A.%a.out
#SBATCH -e logfiles/train_nets.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

conda activate blinx

python /proj/dschridelab/lswhiteh/timesweeper/src/nets.py \
    -i /proj/dschridelab/lswhiteh/timesweeper-experiments/empirical_model/OoA_stdpopsim/ \
    -o /proj/dschridelab/lswhiteh/timesweeper-experiments/empirical_model/OoA_stdpopsim/results \
    -n OoA_stdpopsim \
    -t AFS

python /proj/dschridelab/lswhiteh/timesweeper/src/nets.py \
    -i /proj/dschridelab/lswhiteh/timesweeper-experiments/empirical_model/OoA_stdpopsim/ \
    -o /proj/dschridelab/lswhiteh/timesweeper-experiments/empirical_model/OoA_stdpopsim/results \
    -n OoA_stdpopsim \
    -t HFS
#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=4G
#SBATCH --ntasks=8
#SBATCH --time=2-00:00:00
#SBATCH -J download
#SBATCH -o download.%A.out
#SBATCH -e download.%A.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

for i in $(cut samp_data/filtered_samps.tsv -f9)
do
    wget $i -t 0 &
done
wait
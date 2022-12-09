#!/bin/bash
#SBATCH --partition=general
#SBATCH --constraint=rhel8
#SBATCH --mem=4G
#SBATCH --ntasks=8
#SBATCH --time=2-00:00:00
#SBATCH -J download
#SBATCH -o download.%A.out
#SBATCH -e download.%A.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu

cd ..
mkdir -p bams/raw
for i in $(cut samp_data/filtered/filtered_samps.tsv -f9)
do
    wget -nc -P bams/raw/ $i -t 0 &
done
wait
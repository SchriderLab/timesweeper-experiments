#!/bin/bash
#SBATCH --partition=general
#SBATCH --mem=32G
#SBATCH -c 16
#SBATCH --time=2-00:00:00
#SBATCH -J merge_proc_vcf
#SBATCH -o merge_proc_vcf.%A.out
#SBATCH -e merge_proc_vcf.%A.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu


conda activate blinx
snakemake -c all --rerun-incomplete
#!/bin/bash
#SBATCH --partition=dschridelab
#SBATCH --constraint=rhel8
#SBATCH --mem=8G
#SBATCH -c 6
#SBATCH --time=6:00:00
#SBATCH -J ss10_sim
#SBATCH -o logfiles/sims/ss10.%A.%a.out
#SBATCH -e logfiles/sims/ss10.%A.%a.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=lswhiteh@email.unc.edu
#SBATCH --array=0-2490:10

#conda init bash
#conda activate blinx
#source activate blinx

configfile=config.yaml
python simulate_custom.py yaml ${configfile}

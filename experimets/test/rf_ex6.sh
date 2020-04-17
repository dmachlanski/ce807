#!/bin/bash
# FILE: rf_ex6.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N rf_ex6
#$ -pe smp 5
source activate ce807
python ../../run.py -c rf -m test -f=0.5 -v=1 -b --min_ss=20 -n=5 -j=5
conda deactivate
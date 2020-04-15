#!/bin/bash
# FILE: rf_ex2.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N rf_ex2
#$ -pe smp 10
source activate ce807
python ../../run.py -c rf -m test -f=0.1 -v=1 -b --min_ss=20 -n=10 -j=10
conda deactivate
#!/bin/bash
# FILE: rf_ex2.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N rf_ex2
#$ -pe smp 5
source activate ce807
python ../../run.py -c rf -m cv -j=5 -v=1 -b -n=3
conda deactivate
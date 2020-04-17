#!/bin/bash
# FILE: xts_ex6.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N xts_ex6
#$ -pe smp 5
source activate ce807
python ../../run.py -c xts -m test -f=0.5 -v=1 -b --min_ss=20 -n=5 -j=5
conda deactivate
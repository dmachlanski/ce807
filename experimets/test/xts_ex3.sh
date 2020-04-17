#!/bin/bash
# FILE: xts_ex3.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N xts_ex3
#$ -pe smp 5
source activate ce807
python ../../run.py -c xts -m test -f=1.0 -v=1 -b --min_ss=20 -n=5 -j=5
conda deactivate
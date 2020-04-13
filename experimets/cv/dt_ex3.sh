#!/bin/bash
# FILE: dt_ex3.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N dt_ex3
#$ -pe smp 5
source activate ce807
python ../../run.py -c dt -m cv -j=5 -v=1 -b --max_features sqrt --min_ss=10
conda deactivate
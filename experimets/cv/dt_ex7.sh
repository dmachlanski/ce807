#!/bin/bash
# FILE: dt_ex7.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N dt_ex7
#$ -pe smp 5
source activate ce807
python ../../run.py -c dt -m cv -j=5 -v=1 -b --min_ss=20 --max_depth=100
conda deactivate
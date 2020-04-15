#!/bin/bash
# FILE: dt_ex9.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N dt_ex9
#$ -pe smp 5
source activate ce807
python ../../run.py -c dt -m cv -j=5 -v=1 -b --min_ss=20 --max_depth=10
conda deactivate
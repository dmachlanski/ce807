#!/bin/bash
# FILE: dt_ex1.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N dt_ex1
#$ -pe smp 5
source activate quadflor
python ../../run.py -c dt -m cv -j=5 -v=1
conda deactivate
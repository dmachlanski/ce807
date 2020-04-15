#!/bin/bash
# FILE: dt_ex1.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N dt_ex1
source activate ce807
python ../../run.py -c dt -m test -f=0.1 -v=1 -b --min_ss=20
conda deactivate
#!/bin/bash
# FILE: dt_ex2.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N dt_ex2
source activate ce807
python ../../run.py -c dt -m test -f=0.2 -v=1 -b --min_ss=20
conda deactivate
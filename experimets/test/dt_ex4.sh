#!/bin/bash
# FILE: dt_ex4.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N dt_ex4
source activate ce807
python ../../run.py -c dt -m test -f=1.0 -v=1 -b --min_ss=20
conda deactivate
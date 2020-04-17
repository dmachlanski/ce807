#!/bin/bash
# FILE: dt_ex5.sh
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q all.q
#$ -N dt_ex5
source activate ce807
python ../../run.py -c dt -m test -f=0.01 -v=1 -b --min_ss=20 -d pubmed
conda deactivate
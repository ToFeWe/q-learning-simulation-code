#!/bin/bash
#PBS -l select=1:ncpus=1:mem=50GB:arch=icelake
#PBS -l walltime=0:10:00
#PBS -A "AlgColl"


module load Python/3.11.3
cd $PBS_O_WORKDIR

source ./q_env/bin/activate

python compress_all_files.py
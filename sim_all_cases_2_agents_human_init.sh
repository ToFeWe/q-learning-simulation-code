#!/bin/bash
#PBS -l select=1:ncpus=1:mem=500MB:arch=icelake
#PBS -l walltime=71:59:00
#PBS -A "AlgColl"
#PBS -r y
#PBS -o pbs_output/o_files/2_agents/grid_search/job_array_index_[^array_index^].OU
#PBS -e pbs_output/e_files/2_agents/grid_search/job_array_index_[^array_index^].ER

me=`basename $0`
LOGFILE=$PBS_O_WORKDIR/"pbs_output/log_files"/$PBS_JOBNAME"."$PBS_JOBID"_"$PBS_ARRAY_INDEX".log"

echo "$PBS_JOBID ($PBS_JOBNAME) @ `hostname` at `date` in "$RUNDIR" START" > $LOGFILE
echo "`date +"%d.%m.%Y-%T"`" >> $LOGFILE

echo >> $LOGFILE
echo "GLOBAL PARAMETERS" >> $LOGFILE
echo "---------------------------" >> $LOGFILE
echo "Node      : "`hostname` >> $LOGFILE
echo "RunDir    : "$PBS_O_WORKDIR >> $LOGFILE
echo "# CPUs    : "$NCPUS >> $LOGFILE
echo "# Threads : "$OMP_NUM_THREADS >> $LOGFILE


module load Python/3.11.3

cd $PBS_O_WORKDIR
#cd /home/werner01/Documents/alg_price

# Note that the environment was created ex ante
source ./q_env/bin/activate

shopt -s extglob

echo >> $LOGFILE
echo "RUNNING INITAL TESTS....." >> $LOGFILE
pytest .. -v >> $LOGFILE

echo "STARTING..." >> $LOGFILE
echo "---------------------------" >> $LOGFILE

eval 'python run_mc_simulation.py parameter_2_agent_base_human_init parameter_2_agent_cases_human_init '$PBS_ARRAY_INDEX | tee -a ${LOGFILE}

echo >> $LOGFILE
qstat -f $PBS_JOBID >> $LOGFILE

echo "$PBS_JOBID ($PBS_JOBNAME) @ `hostname` at `date` in "$RUNDIR" END" >> $LOGFILE
echo "`date +"%d.%m.%Y-%T"`" >> $LOGFILE

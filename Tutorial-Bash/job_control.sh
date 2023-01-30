#!/usr/bin/env bash
# NOTE: This file should be sourced instead of executed
#
# see https://www.gnu.org/software/bash/manual/html_node/Job-Control-Basics.html
# Terms
#  - Process - executed programs
#  - Job/Pipeline - set of processes run sequentially
#  - Process group - group of processes tied to a specific terminal window
#    - Process group ID - the ID assigned to the current terminal and all processes run inside it
#    - background processes have a different group ID than foreground processes
#  - Job specification (jobspec) - the integer assigned to a job relative to a terminal

################################################################################
echo "Initiating dummy jobs"
sleep 101 & # job %1
sleep 102 & # job %2
sleep 103 & # job %3
sleep 104 & # job %4

jobs -l
echo

# get job PIDs
njobs=$(jobs | wc -l)
job_pid=()
for j in $(seq $njobs); do
    job_pid[$j]="$(jobs -l | fgrep [${j}] | awk '{print $2}')"
    #echo "Job ${j} PID = ${job_pid[${j}]}"
done
#echo "Job PIDs = ${job_pid[@]}"

################################################################################
echo "Suspend (pause) a job"
# Can use job ID or process ID
kill -STOP %+ # targets %4, which remains current job
kill -STOP %- # targets %3, which becomes current job and %4 becomes previous job
kill -STOP ${job_pid[2]} # Becomes current job
kill -STOP %1 # Becomes current job and %2 becomes previous job
jobs -l
echo

################################################################################
echo "Resume suspended job"
# Can only use job ID
bg %% # targets %1 but %2 is now current job because priority given to stopped jobs
bg % # %2
bg % # %4
bg % # %3
echo; jobs -l; echo

# fg - not practical to impliment in a script

################################################################################
echo "Pause script until background process finishes"
sleep 1 & # job %4
wait %
echo

################################################################################
echo "Kill (terminate) a job"
kill %1 %2 %3
# Changes to job status are not printed until bash tries printing a prompt
jobs -l # Some jobs still shown as running
echo

# Not clear to me what causes bash to print change in status but the cmds below work
echo "Force bash to show any remaining change of status"
sleep 0 # any simple command works
#echo " " | xargs echo > /dev/null # Piping stdout into other commands works
echo

echo "Remaining jobs"
jobs -l
echo

################################################################################
# stty

# ps, top, htop

################################################################################
echo "Search for and kill any remaining sleep jobs"
if pgrep -q sleep; then 
    pkill sleep # This could be run outside the if statement
    #Can also run killall sleep 
fi;


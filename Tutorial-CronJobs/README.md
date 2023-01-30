# Tutorial-CronJobs

## Introduction
Adding a cronjob via crontab is not particularlly difficult. You essentially
configure the timing of the jobs and then provide it the commands to run. The
challenge is in (1) understanding the environment that the cron job is run in
and what setup is needed to run the desired scripts and (2) how to scale up
one's use of cron jobs so that many complicated cron jobs can be managed

Regarding the environment, none of the usual environment variables are defined
(e.g. `PATH`). Therefore, many commands that work when run from command line
(e.g. `source ~/.bash_profile` or `python /path/to/script.py`) may not work.  
As a basic check, make sure any cronjob defines the relevant PATH variables (or
uses absolute paths) for any commands and files. Also, only try to execute
scripts that have permission to be executed by the user.

## Advanced techniques
- Preventing a cronjob from starting if the previous one has not finished
- Changing the mailing address of cronjob diagnostic information (or stopping
  the mailing all-together) 
- Storing multiple crontab files and then using them to set the single user
  crontab file as needed

#!/bin/bash
#
# You should only work under the /scratch/users/<username> directory.
#
# Example job submission script
#
# TODO:
#   - Set name of the job below changing "Test" value.
#   - Set the requested number of tasks (cpu cores) with --ntasks parameter.
#   - Select the partition (queue) you want to run the job in:
#     - short : For jobs that have maximum run time of 120 mins. Has higher priority.
#     - long  : For jobs that have maximum run time of 7 days. Lower priority than short.
#     - longer: For testing purposes, queue has 31 days limit but only 3 nodes.
#   - Set the required time limit for the job with --time parameter.
#     - Acceptable time formats include "minutes", "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds"
#   - Put this script and all the input file under the same directory.
#   - Set the required parameters, input and output file names below.
#   - If you do not want mail please remove the line that has --mail-type
#   - Put this script and all the input file under the same directory.
#   - Submit this file using:
#      sbatch examle_submit.sh

# -= Resources =-
#
#SBATCH --job-name=ecm_run
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --partition=mid
#SBATCH --qos=users
#SBATCH --time=24:00:00
#SBATCH --output=ecm_run-%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=adansik22@ku.edu.tr

################################################################################
##################### !!! DO NOT EDIT BELOW THIS LINE !!! ######################
################################################################################


# create separate directory for each patient to direct outputs

if [ -d "patients" ]; then
  echo "Patient directories already created"
elif [ ! -d "patients" ]; then 
  echo "Creating patient directories" 
  mkdir patients 
  cd terminals/
  for i in *.tsv ; do 
    mkdir ../patients/${i%.tsv}  ; 
  done
  cd ..
fi

# load modules

module load anaconda/2022.10
module load R/4.2.0

# activate environment

source activate ecm_momix

# run get_membership.py

if [  -s "patients/C3L.00001/C3L.00001_membership_df.csv" ]   ; then 
	echo "Skipping parameter sweep"  
elif [ ! -s "patients/C3L.00001/C3L.00001_membership_df.csv" ] ; then 
	echo "Starting parameter sweep" 
	python scripts/get_memberships.py  
	echo "Parameter sweep done"
fi

# run get_parameterlist.R

if [  -s "g34_parameter_list.csv" ] || [ ! -s "patients/C3L.00001/C3L.00001_membership_df.csv" ]  ; then 
	echo "Skipping parameter listing"  
elif [ ! -s "g34_parameter_list.csv" ] && [ -s "patients/C3L.00001/C3L.00001_membership_df.csv" ] ; then 
	echo "Starting parameter listing" 
	R CMD BATCH scripts/get_parameterlist.R  
	echo "Parameter listing done"
fi

# run get_networks.py

if [  -s "patients/C3L.00001/C3L.00001_nodes.csv" ] || [ ! -s "g34_parameter_list.csv" ]   ; then 
	echo "Skipping network construction"  
elif [ ! -s "patients/C3L.00001/C3L.00001_nodes.csv" ] && [ -s "g34_parameter_list.csv" ] ; then 
	echo "Starting network construction" 
	python scripts/get_networks.py  
	echo "Network construction done"
fi





















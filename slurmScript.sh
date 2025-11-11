#!/bin/bash
#SBATCH --job-name=APSingleCodebase_Simulation
#SBATCH --nodes=1                   
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --mem=5980mb

echo "Total $# arguments passed to me are: $*"

# default parameter in case nothing was passed in
#drug_delivery_schedule=1
#dailyDose=0.1
#VconcST=1.75
#supplyScalar=1
#RUNS=1

RUNS=$SLURM_ARRAY_TASK_ID

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --Dose_schedule) Dose_schedule="$2"; shift 2;;
    --dailyDose) dailyDose="$2"; shift 2;;
    --Read_in_gradient) Read_in_gradient="$2"; shift 2;;
    --VEGFconc) VEGFconc="$2"; shift 2;;
    --VconcST) VconcST="$2"; shift 2;;
    *) echo "Unknown parameter: $1"; shift;;
  esac
done

# ml purge
ml foss

# Run the executable with specified parameters
./springAgent $Dose_schedule $dailyDose $Read_in_gradient $VconcST $VEGFconc $RUNS


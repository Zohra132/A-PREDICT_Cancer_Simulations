#!/bin/bash
#SBATCH --job-name=Optimiser
#SBATCH --nodes=1                   
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=72:00:00
#SBATCH --partition=ncpu
#SBATCH --mem=7G

echo "Total $# arguments passed to me are: $*"
echo "Running job $SLURM_JOB_ID, array task $SLURM_ARRAY_TASK_ID"


# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --pop_size) pop_size="$2"; shift 2;;
    --n_gen) n_gen="$2"; shift 2;;
    --threshold) threshold="$2"; shift 2;;
    --cx_prob) cx_prob="$2"; shift 2;;
    --mut_prob) mut_prob="$2"; shift 2;;
    --output_filename) output_filename="$2"; shift 2;;

    # Multi-value argument (vegf)
    --vegf) shift; vegf="";
            while [[ $# -gt 0 && $1 != --* ]]; do
              vegf="$vegf $1"
              shift
            done;;

    --schedule_min) schedule_min="$2"; shift 2;;
    --schedule_max) schedule_max="$2"; shift 2;;
    --dose_min) dose_min="$2"; shift 2;;
    --dose_max) dose_max="$2"; shift 2;;

    *) echo "Unknown parameter: $1"; shift;;
  esac
done


#Load environment
ml purge
ml foss
ml Python

source ~/envs/myenv/bin/activate

# Make output unique per run

run_id=$SLURM_ARRAY_TASK_ID
output_filename="${output_filename}_run_${run_id}"


echo "Running with parameters:"
echo "pop_size=$pop_size"
echo "n_gen=$n_gen"
echo "threshold=$threshold"
echo "cx_prob=$cx_prob"
echo "mut_prob=$mut_prob"
echo "vegf=$vegf"
echo "schedule_min=$schedule_min"
echo "schedule_max=$schedule_max"
echo "dose_min=$dose_min"
echo "dose_max=$dose_max"
echo "output=$output_filename"


# Run Python script
python3 main.py \
  --pop_size "$pop_size" \
  --n_gen "$n_gen" \
  --threshold "$threshold" \
  --cx_prob "$cx_prob" \
  --mut_prob "$mut_prob" \
  --output_filename "$output_filename" \
  --vegf $vegf \
  --schedule_min "$schedule_min" \
  --schedule_max "$schedule_max" \
  --dose_min "$dose_min" \
  --dose_max "$dose_max" 


#!/bin/bash


analysis=""
camp_subfolder_name="EA-Optimiser/2026.04.19-20.15.15"
camp_home="/camp/home/sohrabz"

# Example parameter sweeps
pop_size=(100)
n_gen=(50)
threshold=(0.75)
cx_prob=(0.9)
mut_prob=(0.1)

vegf_values="8"

job_count=0
batch_limit=20  # Submit this many jobs before waiting
#delay_time=600   # Delay time in seconds (600 = 10 minutes)

for p in "${pop_size[@]}"; do
  for g in "${n_gen[@]}"; do
    for t in "${threshold[@]}"; do
      for cx in "${cx_prob[@]}"; do
        for mut in "${mut_prob[@]}"; do

          sbatch --array=1-10%10 slurm_script.sh \
            --pop_size $p \
            --n_gen $g \
            --threshold $t \
            --cx_prob $cx \
            --mut_prob $mut \
            --output_filename results \
            --vegf $vegf_values \
            --schedule_min 100 \
            --schedule_max 7000 \
            --dose_min 0.01 \
            --dose_max 80

          ((job_count++))

        done
      done
    done
  done
done

echo "All jobs submitted! Total job arrays: $job_count"

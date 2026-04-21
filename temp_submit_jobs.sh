#code Bentley Lab created, currently confidential as paper under review Au et al Cancer Cell 2026
#!/bin/bash

numberOfRuns=10
analysis="APREDICT_dose"
camp_subfolder_name="APSingleCodebase/APREDICT_dose_2025.09.09-20.22.24"
camp_home="/camp/lab/bentleyk/home/shared/a-predict-cancer-simulations"

# parameter set 1
#Dose_schedule=(2880)
#dailyDose=(0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5 6.0 6.5 7.0 7.5 8.0 8.5 9.0 9.5 10)
#Read_in_gradient=(0)
#VEGFconc=(0.8 0.9 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3.0 3.1 3.2 3.3 3.4 3.5 3.6 3.7 3.8 3.9 4.0 4.1 4.2 4.3 4.4 4.5 4.6 4.7 4.8 4.9 5.0 5.1 5.2 5.3 5.4 5.5 5.6 5.7 5.8 5.9 6.0 6.1 6.2 6.3 6.4 6.5 6.6 6.7 6.8 6.9 7.0 7.1 7.2 7.3 7.4 7.5 7.6 7.7 7.8 7.9 8.0)
#VconcST=(0)

# parameter set 2
Dose_schedule=(2880)
dailyDose=(0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5 6.0 6.5 7.0 7.5 8.0 8.5 9.0 9.5 10)
Read_in_gradient=(2)
VEGFconc=(0)
VconcST=(0.04 0.08 0.12 0.16 0.20 0.24 0.28 0.32 0.36 0.40)

# Counter for submitted jobs
job_count=0
batch_limit=20  # Submit this many jobs before waiting
#delay_time=600   # Delay time in seconds (600 = 10 minutes)

for Dose_schedule in "${Dose_schedule[@]}"; do
  for dailyDose in "${dailyDose[@]}"; do
    for Read_in_gradient in "${Read_in_gradient[@]}"; do
      for VEGFconc in "${VEGFconc[@]}"; do
        for VconcST in "${VconcST[@]}"; do

          sbatch --array 1-10 slurmScript.sh \
                      --Dose_schedule $Dose_schedule \
                      --dailyDose $dailyDose \
                      --Read_in_gradient $Read_in_gradient \
                      --VEGFconc $VEGFconc \
                      --VconcST $VconcST \
#          ((job_count++))

          # If batch limit reached, pause before next batch
#          if (( job_count % batch_limit == 0 )); then
#            echo "Submitted  jobs. Sleeping for 10 minutes before continuing..."
#            sleep 600
#          fi

        done
      done
    done
  done
done

echo "All jobs submitted! Total job arrays: $job_count"

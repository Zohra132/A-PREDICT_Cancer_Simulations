analysis="APREDICT_dose"

numberOfRuns=10 # number of slurm runs. Used slurm array id instead in slurmScript

# File name and location so sync with nemo
timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
#local_output_foldername="camp_output_analysis_"$analysis"_"$timestamp
camp_subfolder_name="APSingleCodebase/"$analysis"_"$timestamp

echo "camp folder name: $camp_subfolder_name"

#mkdir $local_output_foldername
camp_home="/camp/lab/bentleyk/home/shared/a-predict-cancer-simulations"

echo "analysis type: $analysis"
echo "number of runs: $numberOfRuns"
echo "uploading simulation files to nemo..."

# Sync files with nemo (automatically create folder with same permissions as local files)
rsync -ar --include="*/" --include="*.cpp" --include="*.h" --include="*.sh" --include="makefile" --include="requirements" --exclude="*" ./ login.nemo.thecrick.org:"$camp_home"/"$camp_subfolder_name"/


# build project on nemo
ssh -v login.nemo.thecrick.org  "echo  \"log in successful... setting up environment\"; cd $camp_home/$camp_subfolder_name; chmod +x slurmScript.sh; ml purge; ml foss; echo \"running make... \"; ./buildSpringAgent.sh --camp; echo \" finished building spring agent\"; exit;"

# Create the job submission script
cat > temp_submit_jobs.sh << EOF
#!/bin/bash

numberOfRuns=10
analysis="$analysis"
camp_subfolder_name="$camp_subfolder_name"
camp_home="$camp_home"

# parameter set 1
#Dose_schedule=(2880)
#dailyDose=(0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0)
#Read_in_gradient=(0)
#VEGFconc=(0.8 1.6 2.4 3.2 4 4.8 5.6 6.4 7.2 8)
#VconcST=(0)

# parameter set 2
Dose_schedule=(2880)
dailyDose=(0.005 0.01 0.015 0.02 0.025 0.03 0.035 0.04 0.045 0.05 0.06 0.07 0.08 0.09 0.1 0.2 0.3 0.4 0.5)
Read_in_gradient=(2)
VEGFconc=(0)
VconcST=(0.08 0.12 0.16 0.20 0.24 0.28 0.32 0.36 0.40)

# parameter set 3
#Dose_schedule=(2880)
#dailyDose=(0.005 0.01 0.015 0.02 0.025 0.03 0.035 0.04 0.045 0.05 0.06 0.07 0.08 0.09 0.1 0.2 0.3 0.4 0.5)
#Read_in_gradient=(0)
#VEGFconc=(0.8 1.6 2.4 3.2 4 4.8 5.6 6.4 7.2 8)
#VconcST=(0)

# parameter set 4
Dose_schedule=(2880)
dailyDose=(0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0)
Read_in_gradient=(2)
VEGFconc=(0)
VconcST=(0.08 0.12 0.16 0.20 0.24 0.28 0.32 0.36 0.40)

# Counter for submitted jobs
job_count=0
batch_limit=20  # Submit this many jobs before waiting
#delay_time=600   # Delay time in seconds (600 = 10 minutes)

for Dose_schedule in "\${Dose_schedule[@]}"; do
  for dailyDose in "\${dailyDose[@]}"; do
    for Read_in_gradient in "\${Read_in_gradient[@]}"; do
      for VEGFconc in "\${VEGFconc[@]}"; do
        for VconcST in "\${VconcST[@]}"; do

          sbatch --array 1-10 slurmScript.sh \\
                      --Dose_schedule \$Dose_schedule \\
                      --dailyDose \$dailyDose \\
                      --Read_in_gradient \$Read_in_gradient \\
                      --VEGFconc \$VEGFconc \\
                      --VconcST \$VconcST \\
#          ((job_count++))

          # If batch limit reached, pause before next batch
#          if (( job_count % batch_limit == 0 )); then
#            echo "Submitted $job_count jobs. Sleeping for 10 minutes before continuing..."
#            sleep 600
#          fi

        done
      done
    done
  done
done

echo "All jobs submitted! Total job arrays: \$job_count"
EOF

# Copy and run the submission script
scp temp_submit_jobs.sh login.nemo.thecrick.org:$camp_home/$camp_subfolder_name/submit_jobs.sh
ssh login.nemo.thecrick.org "cd $camp_home/$camp_subfolder_name && chmod +x submit_jobs.sh && ./submit_jobs.sh"


# get the results back to this local machine from nemo
#rsync -ar login.nemo.thecrick.org:"$camp_home/$camp_subfolder_name"/analysis_APREDICT_doseschedule_* .

echo "All camp jobs submitted. Wait for runs to finish (check with sacct or squeue -u <username>) then copy output files from $camp_home/$camp_subfolder_name"

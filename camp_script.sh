REMOTE_USER=sohrabz
REMOTE_HOST=login.nemo.thecrick.org
SSH_KEY=~/.ssh/id_rsa  

N_RUNS=10 # number of slurm runs

# File name and location to sync with nemo
timestamp=$(date "+%Y.%m.%d-%H.%M.%S")
camp_subfolder_name="EA-Optimiser/$timestamp"
camp_home="/camp/home/$REMOTE_USER"

camp_home="/camp/home/sohrabz"

echo "camp folder name: $camp_subfolder_name"
echo "number of runs: $numberOfRuns"
echo "uploading simulation files to nemo..."

#Sync files with nemo (automatically create folder with same permissions as local files)
ssh -i ~/.ssh/id_rsa sohrabz@login.nemo.thecrick.org "mkdir -p $camp_home/$camp_subfolder_name"

#rsync files
rsync -av \
  --include=*/ \
  --include=*.cpp \
  --include=*.h \
  --include=*.sh \
  --include=*.py \
  --include=*.txt \
  --include=makefile \
  --include=requirements \
  --exclude=* \
  ./ $REMOTE_USER@$REMOTE_HOST:"$camp_home/$camp_subfolder_name/"


# build project on nemo
ssh -i $SSH_KEY $REMOTE_USER@$REMOTE_HOST "
  echo  \"log in successful... setting up environment\"; 
  cd '$camp_home/$camp_subfolder_name'; 
  chmod +x slurm_script.sh; 
    echo  \"execute permissions added to slurm script\"; 
  chmod +x buildSpringAgent.sh;
    echo  \"execute permissions added to buildSpringAgent\"; 

  
  ml purge; 
  ml foss; 

  echo 'Building SpringAgent...';
  bash ./buildSpringAgent.sh;
  echo 'SpringAgent build finished';

  ml GCC/14.2.0

  echo 'finished preparing environment on NEMO';
  exit;
"

# Create the job submission script
cat > submit_jobs.sh << EOF
#!/bin/bash


analysis="$analysis"
camp_subfolder_name="$camp_subfolder_name"
camp_home="$camp_home"

# Example parameter sweeps
pop_size=(100)
n_gen=(50)
threshold=(0.75)
cx_prob=(0.9)
mut_prob=(0.1)

# VEGF list (fixed)
vegf_values="8"

job_count=0
batch_limit=20  # Submit this many jobs before waiting
#delay_time=600   # Delay time in seconds (600 = 10 minutes)

for p in "\${pop_size[@]}"; do
  for g in "\${n_gen[@]}"; do
    for t in "\${threshold[@]}"; do
      for cx in "\${cx_prob[@]}"; do
        for mut in "\${mut_prob[@]}"; do

          sbatch --array=1-${N_RUNS}%${N_RUNS} slurm_script.sh \\
            --pop_size \$p \\
            --n_gen \$g \\
            --threshold \$t \\
            --cx_prob \$cx \\
            --mut_prob \$mut \\
            --output_filename results \\
            --vegf \$vegf_values \\
            --schedule_min 100 \\
            --schedule_max 7000 \\
            --dose_min 0.01 \\
            --dose_max 80

          ((job_count++))

        done
      done
    done
  done
done

echo "All jobs submitted! Total job arrays: \$job_count"
EOF

# Copy and run the submission script
scp -i $SSH_KEY submit_jobs.sh $REMOTE_USER@$REMOTE_HOST:$camp_home/$camp_subfolder_name/submit_jobs.sh
ssh -i $SSH_KEY $REMOTE_USER@$REMOTE_HOST "
  cd $camp_home/$camp_subfolder_name &&
  chmod +x submit_jobs.sh && 
  ./submit_jobs.sh
"

# get the results back to this local machine from nemo
#rsync -ar login.nemo.thecrick.org:"$camp_home/$camp_subfolder_name"*
echo "All camp jobs submitted. Wait for runs to finish (check with sacct or squeue -u <username>) then copy output files from $camp_home/$camp_subfolder_name"


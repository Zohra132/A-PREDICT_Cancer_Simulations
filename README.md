# Multi-Objective Evolutionary Optimisation of Cancer Treatment Strategies Using MEMAgent Sring 
This project implements a Python-based optimiser, running experiements locally or on a HPC cluster. 

It builds upon the MemAgent-Spring Model developed within Cellular Adaptive Behaviour Lab. Bentley Lab created code, currently confidential as paper under review Au et al Cancer Cell 2026, has been annotated at the top of each file.

## Run setup
Install system and python dependencies:
```bash
chmod +x setup.sh
./setup.sh
```
macOS users must have Homebrew installed.


## Build simulation
Build the springAgent executable with data output:
```
bash ./BuildSpringAgent.sh 
```

Build the springAgent executable with graphics but no data output:
```bash
./BuildSpringAgent.sh --graphics 
```

## Run simulation
Example command: 
```bash
./SpringAgent 2880 5 1 0.04 0.8 1
```

This must be run with runtime arguments. 


## Run optimiser (Local)
Example command:
```bash
python3 main.py 
    --pop_size 100
    --n_gen 50
    --threshold 0.9 
    --cx_prob 0.9 
    --mut_prob 0.1 
    --output_filename results
    --vegf 8 7.2 6.4 
    --schedule_min 100 
    --schedule_max 7000 
    --dose_min 1 
    --dose_max 800
```


## Run on HPC cluster
Ensure access is set up on cluster
1. SSH into cluster:
```bash
ssh <your-username>@<cluster-address>
```

2. Copy files to the cluster
```bash
scp ~/<full/local/path>/BuildSpringAgent.sh \ 
<full/local/path>/slurm_script.sh \ 
<full/local/path>/camp_script.sh \ 
<username>@<cluster-address>:<remote_directory>
```

3. Run the job script
```bash
./camp_script.sh
```

## Optimiser Output Files
After running the optimiser, results are saved to CSV files using the specified --output_filename prefix. The results are saved to a folder using the --output_filename prefix

### Output files
Final Pareto front (best solutions only):
{output_filename}_run_${run_id}_pareto.csv

Full final generation (all individuals):
{output_filename}_run_${run_id}_full.csv

Pareto front for every generation:
{output_filename}_run_${run_id}_pareto_gen_vegf{vegf}.csv


Folders 'pop100-main, 'pop100-initial', 'pilot_runs_0.7-0.25' and 'pilot_runs_0.9-0.1', contain the output files of 10 runs, from 4 separate configurations.


## Plot Graphs
Six plotting scripts are provided to visualise and comapre optimisation results. Each script requires the output folder produced by `main.py` to be specified.

### For individual runs:

```bash
python3 plot_paretofront.py
python3 plot_all_graphs.py
```


### For multiple independent runs

```bash
python3 plot_all_paretofront.py
python3 plot_all_scheduledose.py
python3 plot_combined_convergence.py
python3 plot_combined_paretofront.py
python3 plot_combined_scheduledose.py
```

These scripts expect multiple `*_pareto.csv` and `*_full.csv` files to be present in the output folder. 

Plots are saved as `.png` files.

Folders 'pop100-main, 'pop100-initial', 'pilot_runs_0.7-0.25' and 'pilot_runs_0.9-0.1', contain graphs generated from these scripts.
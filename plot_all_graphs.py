#plots given 2 params- for a all .csv in a given folder
import csv
import matplotlib.pyplot as plt
import statistics


folder = "pop100-v3"
runs = [2, 3, 4, 5, 6, 7, 8, 9, 10]

#schedule,dose,vegfconc,vascular,time
param1 = "schedule" #objective: vascular or time #x-axis
param2 = "dose"  #schedule or dose #y-axis



output = f"{param1}_vs_{param2}_all_runs_comparison.png"

#fig, axes = plt.subplots(2, 1, figsize=(5, 10))  # for 2 graphs
fig, axes = plt.subplots(2, 5, figsize=(15, 8)) # for 10 graphs
#fig, axes = plt.subplots(2, 2, figsize=(10, 10)) # for 10 graphs#
plt.tight_layout(rect=[0, 0.15, 1, 1])
plt.subplots_adjust(hspace=0.3) 
axes = axes.flatten()
all_mean_param1 = []
all_mean_param2 = []


for i, run in enumerate(runs):

    full_file = f"results_run_{run}_full.csv"
    paretofront_file = f"results_run_{run}_pareto.csv"

    param1_full, param2_full = [], []
    param1_pareto, param2_pareto = [], []

    #Load full population
    with open(f"{folder}/{full_file}", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            param1_full.append(float(row[param1]))
            param2_full.append(float(row[param2]))

    #Pareto front points
    with open(f"{folder}/{paretofront_file}", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            param1_pareto.append(float(row[param1]))
            param2_pareto.append(float(row[param2]))


    mean_param2 = statistics.mean(param2_full)
    std_param2 = statistics.stdev(param2_full) if len(param2_full) > 1 else 0

    mean_param1 = statistics.mean(param1_full)
    std_param1 = statistics.stdev(param1_full) if len(param1_full) > 1 else 0

    all_mean_param2.append(mean_param2)
    all_mean_param1.append(mean_param1)

    ax = axes[i]

    ax.scatter(
        param1_full, param2_full,
        c='lightgray', s=20, alpha=0.3
    )

    ax.scatter(
        param1_pareto, param2_pareto,
        c='black', s=40
    )

    ax.set_title(f"Run {run}")
    ax.set_xlabel(param1)
    ax.set_ylabel(param2)
    ax.grid(alpha=0.2)

    # Stats text under each subplot
    stats_text = (
        f"μ_{param1}={mean_param1:.2f}, σ={std_param1:.2f}\n"
        f"μ_{param2}={mean_param2:.2f}, σ={std_param2:.2f}"
    )


    ax.text(
        0.5, -0.3, stats_text,
        transform=ax.transAxes,
        ha='center',
        fontsize=7,
        clip_on=False   
    )


overall_mean_param2 = statistics.mean(all_mean_param2)
overall_std_param2 = statistics.stdev(all_mean_param2)

overall_mean_param1 = statistics.mean(all_mean_param1)
overall_std_param1 = statistics.stdev(all_mean_param1)


summary_text = (
    f"Overall Statistics Across Runs:\n"
    f"{param1}: μ = {overall_mean_param1:.3f}, σ = {overall_std_param1:.3f}    "
    f"{param2}: μ = {overall_mean_param2:.3f}, σ = {overall_std_param2:.3f}"
)


plt.figtext(0.5, 0.05, summary_text, ha='center', fontsize=9)



plt.tight_layout()

plt.subplots_adjust(bottom=0.25)
plt.savefig(f"{folder}/{output}", dpi=300)
plt.show()
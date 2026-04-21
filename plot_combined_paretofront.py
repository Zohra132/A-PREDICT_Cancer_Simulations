import csv
import matplotlib.pyplot as plt
import statistics
import numpy as np

folder = "pop100-main"
runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

plt.figure(figsize=(8, 6))

all_mean_vascular = []
all_mean_time = []
pareto_mean_vascular = []
pareto_mean_time = []

all_pareto_times = []
all_pareto_vasculars = []

for run in runs:
    times_full, vasculars_full = [], []
    times_pareto, vasculars_pareto = [], []

    #full population
    with open(f"{folder}/results_run_{run}_full.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vascular = float(row["vascular"])
            time = float(row["time"])
            if vascular > 0 and time < 99999:
                times_full.append(time)
                vasculars_full.append(vascular)

    #pareto
    with open(f"{folder}/results_run_{run}_pareto.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vascular = float(row["vascular"])
            time = float(row["time"])
            if vascular > 0 and time < 99999:
                times_pareto.append(time)
                vasculars_pareto.append(vascular)

    mean_vascular = statistics.mean(vasculars_full)
    std_vascular = statistics.stdev(vasculars_full) if len(vasculars_full) > 1 else 0

    mean_time = statistics.mean(times_full)
    std_time = statistics.stdev(times_full) if len(times_full) > 1 else 0

    all_mean_vascular.append(mean_vascular)
    all_mean_time.append(mean_time)

    if len(vasculars_pareto) > 0:
        pareto_mean_vascular.append(statistics.mean(vasculars_pareto))
        pareto_mean_time.append(statistics.mean(times_pareto))


    #plot FULL per run
    plt.scatter(
        times_full, vasculars_full,
        marker='x', s=20, alpha=0.15,
        label="Full population" if run == runs[0] else ""
    )

    #plot Pareto per run
    plt.scatter(
        times_pareto, vasculars_pareto,
        s=40, alpha=0.5,
        label="Pareto (per run)" if run == runs[0] else ""
    )


plt.xlabel("Time (minimise)")
plt.ylabel("Vascular score (maximise)")
plt.title("Pareto Front Across All Runs")
plt.ylim(0, 1.05)
#plt.ylim(0.8, 1.02)
#plt.yticks(np.arange(0.8, 1.01, 0.05))

plt.grid(alpha=0.3)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.legend()

overall_mean_vascular = statistics.mean(all_mean_vascular)
overall_std_vascular = statistics.stdev(all_mean_vascular)

overall_mean_time = statistics.mean(all_mean_time)
overall_std_time = statistics.stdev(all_mean_time)

pareto_mean_vascular_overall = statistics.mean(pareto_mean_vascular)
pareto_std_vascular = statistics.stdev(pareto_mean_vascular)

pareto_mean_time_overall = statistics.mean(pareto_mean_time)
pareto_std_time = statistics.stdev(pareto_mean_time)

"""
summary_text = (
    f"Full: μ_v={overall_mean_vascular:.3f}, σ_v={overall_std_vascular:.3f} | "
    f"μ_t={overall_mean_time:.2f}, σ_t={overall_std_time:.2f}\n"
    f"Pareto: μ_v={pareto_mean_vascular_overall:.3f}, σ_v={pareto_std_vascular:.3f}"
    f"μ_t={pareto_mean_time_overall:.2f}, σ_t={pareto_std_time:.2f}"
)

plt.figtext(0.5, 0.05, summary_text, ha='center', fontsize=10)
"""

plt.tight_layout()
plt.subplots_adjust(bottom=0.25)
plt.savefig(f"{folder}/combined_pareto_all_runs.png", dpi=300, bbox_inches='tight')
plt.show()
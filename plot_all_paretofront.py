#plots VEGF againts TIME - for a all .csv in a given folder
import csv
import matplotlib.pyplot as plt
import statistics


folder = "0.9-0.1"
runs = [1, 2, 3, 4]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

all_mean_vascular = []
all_mean_time = []
pareto_mean_vascular = []
pareto_mean_time = []


for i, run in enumerate(runs):
    times_full, vasculars_full = [], []
    times_pareto, vasculars_pareto = [], []

    #Load FULL population
    with open(f"{folder}/results_run_{run}_full.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vascular = float(row["vascular"])
            time = float(row["time"])
            if vascular > 0 and time < 99999:
                times_full.append(time)
                vasculars_full.append(vascular)

    # Load Pareto
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


    ax = axes[i]

    ax.scatter(
        times_full, vasculars_full,
        marker='x', s=30, c='gray', alpha=0.3
    )

    ax.scatter(
        times_pareto, vasculars_pareto,
        marker='o', s=60, c='black', alpha=0.9
    )

    ax.set_title(f"Run {run}")
    ax.set_xlabel("Time (minimise)")
    ax.set_ylabel("Vascular score (maximise)")
    ax.set_ylim(0, 1.05)


    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


    stats_text = (
        f"μ_v={mean_vascular:.2f}, σ_v={std_vascular:.2f}\n"
        f"μ_t={mean_time:.2f}, σ_t={std_time:.2f}"
    )

    ax.text(
        0.5, -0.25, stats_text,
        transform=ax.transAxes,
        ha='center',
        fontsize=9
    )


#full stats
overall_mean_vascular = statistics.mean(all_mean_vascular)
overall_std_vascular = statistics.stdev(all_mean_vascular)

overall_mean_time = statistics.mean(all_mean_time)
overall_std_time = statistics.stdev(all_mean_time)

#pareto stats
pareto_mean_vascular_overall = statistics.mean(pareto_mean_vascular)
pareto_mean_time_overall = statistics.mean(pareto_mean_time)


summary_text = (
    f"Full Population (across runs):\n"
    f"Vascular: μ = {overall_mean_vascular:.3f}, σ = {overall_std_vascular:.3f}    "
    f"Time: μ = {overall_mean_time:.2f}, σ = {overall_std_time:.2f}\n\n"
    f"Pareto Front (across runs):\n"
    f"Vascular: μ = {pareto_mean_vascular_overall:.3f}    "
    f"Time: μ = {pareto_mean_time_overall:.2f}"
)

plt.figtext(0.5, 0.05, summary_text, ha='center', fontsize=11)


plt.tight_layout()
plt.subplots_adjust(bottom=0.25)

plt.savefig(f"{folder}/vascular_vs_time_all_runs_comparison.png", dpi=300)
plt.show()
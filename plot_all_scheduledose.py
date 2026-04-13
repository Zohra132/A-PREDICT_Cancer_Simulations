#plots SCHEDULE againts DOSE - for a all .csv in a given folder
import csv
import matplotlib.pyplot as plt
import statistics


folder = "0.9-0.1"
runs = [1, 2, 3, 4]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()  # easier indexing
all_mean_schedule = []
all_mean_dose = []


for i, run in enumerate(runs):
    schedules_full, doses_full = [], []
    schedules_pareto, doses_pareto = [], []

    #Load FULL population
    with open(f"{folder}/results_run_{run}_full.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            schedules_full.append(float(row["schedule"]))
            doses_full.append(float(row["dose"]))

    # Load Pareto
    with open(f"{folder}/results_run_{run}_pareto.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            schedules_pareto.append(float(row["schedule"]))
            doses_pareto.append(float(row["dose"]))

    mean_schedule = statistics.mean(schedules_full)
    std_schedule = statistics.stdev(schedules_full) if len(schedules_full) > 1 else 0

    mean_dose = statistics.mean(doses_full)
    std_dose = statistics.stdev(doses_full) if len(doses_full) > 1 else 0

    all_mean_schedule.append(mean_schedule)
    all_mean_dose.append(mean_dose)

    ax = axes[i]

    ax.scatter(
        schedules_full, doses_full,
        c='lightgray', s=30, alpha=0.3
    )

    ax.scatter(
        schedules_pareto, doses_pareto,
        c='black', s=60
    )

    ax.set_title(f"Run {run}")
    ax.set_xlabel("Schedule")
    ax.set_ylabel("Dose")
    ax.grid(alpha=0.2)

    # Add stats inside subplot
    stats_text = (
        f"μ_s={mean_schedule:.1f}, σ_s={std_schedule:.1f}\n"
        f"μ_d={mean_dose:.3f}, σ_d={std_dose:.3f}"
    )

    ax.text(0.5, -0.25, stats_text,
            transform=ax.transAxes,
            ha='center', fontsize=9)

overall_mean_schedule = statistics.mean(all_mean_schedule)
overall_std_schedule = statistics.stdev(all_mean_schedule)

overall_mean_dose = statistics.mean(all_mean_dose)
overall_std_dose = statistics.stdev(all_mean_dose)



summary_text = (
    f"Overall Statistics Across Runs:\n"
    f"Schedule: μ = {overall_mean_schedule:.3f}, σ = {overall_std_schedule:.3f}    "
    f"Dose: μ = {overall_mean_dose:.2f}, σ = {overall_std_dose:.2f}"
)

plt.figtext(0.5, 0.05, summary_text, ha='center', fontsize=11)

plt.tight_layout()
plt.subplots_adjust(bottom=0.2)

plt.savefig(f"{folder}/schedule_vs_dose_all_runs_comparison.png", dpi=300)
plt.show()
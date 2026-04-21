#plots TIME againts SCHEDULE - for a all .csv in a given folder
import csv
import matplotlib.pyplot as plt
import statistics


folder = "pop100-main"
runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
output = "schedule_vs_time_all_runs_comparison.png"

fig, axes = plt.subplots(5, 4, figsize=(16, 20))
axes = axes.flatten()
all_mean_time = []
all_mean_schedule = []


for i, run in enumerate(runs):

    full_file = f"results_run_{run}_full.csv"
    paretofront_file = f"results_run_{run}_pareto.csv"

    times_full, schedule_full = [], []
    times_pareto, schedule_pareto = [], []

    # Load FULL population
    with open(f"{folder}/{full_file}", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            times_full.append(float(row["time"]))
            schedule_full.append(float(row["schedule"]))

    # Load Pareto
    with open(f"{folder}/{paretofront_file}", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            times_pareto.append(float(row["time"]))
            schedule_pareto.append(float(row["schedule"]))


    mean_schedule = statistics.mean(schedule_full)
    std_schedule = statistics.stdev(schedule_full) if len(schedule_full) > 1 else 0

    mean_time = statistics.mean(times_full)
    std_time = statistics.stdev(times_full) if len(times_full) > 1 else 0

    all_mean_schedule.append(mean_schedule)
    all_mean_time.append(mean_time)

    ax = axes[i]

    ax.scatter(
        times_full, schedule_full,
        c='lightgray', s=30, alpha=0.3
    )

    ax.scatter(
        times_pareto, schedule_pareto,
        c='black', s=60
    )

    ax.set_title(f"Run {run}")
    ax.set_xlabel("Time (timesteps)")
    ax.set_ylabel("Schedule")
    ax.grid(alpha=0.2)

    # Stats text under each subplot
    stats_text = (
        f"μ_s={mean_schedule:.1f}, σ_s={std_schedule:.1f}\n"
        f"μ_t={mean_time:.2f}, σ_t={std_time:.2f}"
    )

    ax.text(
        0.5, -0.25, stats_text,
        transform=ax.transAxes,
        ha='center',
        fontsize=9
    )

overall_mean_schedule = statistics.mean(all_mean_schedule)
overall_std_schedule = statistics.stdev(all_mean_schedule)

overall_mean_time = statistics.mean(all_mean_time)
overall_std_time = statistics.stdev(all_mean_time)



summary_text = (
    f"Overall Statistics Across Runs:\n"
    f"Schedule: μ = {overall_mean_schedule:.3f}, σ = {overall_std_schedule:.3f}    "
    f"Time: μ = {overall_mean_time:.2f}, σ = {overall_std_time:.2f}"
)

plt.figtext(0.5, 0.05, summary_text, ha='center', fontsize=11)



plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.savefig(f"{folder}/{output}", dpi=300)
plt.show()
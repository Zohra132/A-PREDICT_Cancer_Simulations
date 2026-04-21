import csv
import matplotlib.pyplot as plt
import statistics
import numpy as np

folder = "pop100-main"
runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

plt.figure(figsize=(8, 6))

all_mean_dose = []
all_mean_schedule = []
pareto_mean_dose = []
pareto_mean_schedule = []

all_pareto_schedules = []
all_pareto_doses = []

for run in runs:
    schedules_full, doses_full = [], []
    schedules_pareto, doses_pareto = [], []

    #full population
    with open(f"{folder}/results_run_{run}_full.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dose = float(row["dose"])
            schedule = float(row["schedule"])
            if dose > 0 and schedule < 99999:
                schedules_full.append(schedule)
                doses_full.append(dose)

    #pareto
    with open(f"{folder}/results_run_{run}_pareto.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dose = float(row["dose"])
            schedule = float(row["schedule"])
            if dose > 0 and schedule < 99999:
                schedules_pareto.append(schedule)
                doses_pareto.append(dose)

    mean_dose = statistics.mean(doses_full)
    std_dose = statistics.stdev(doses_full) if len(doses_full) > 1 else 0

    mean_schedule = statistics.mean(schedules_full)
    std_schedule = statistics.stdev(schedules_full) if len(schedules_full) > 1 else 0

    all_mean_dose.append(mean_dose)
    all_mean_schedule.append(mean_schedule)

    if len(doses_pareto) > 0:
        pareto_mean_dose.append(statistics.mean(doses_pareto))
        pareto_mean_schedule.append(statistics.mean(schedules_pareto))


    #plot FULL per run
    plt.scatter(
        schedules_full, doses_full,
        marker='x', s=20, alpha=1, color='black',
        label="Full population" if run == runs[0] else ""
    )

    #plot Pareto per run
    plt.scatter(
        schedules_pareto, doses_pareto,
        s=40, alpha=1, color='steelblue',
        label="Pareto (per run)" if run == runs[0] else ""
    )


plt.xlabel("Schedule")
plt.ylabel("Dose")

plt.grid(alpha=0.3)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.legend()

overall_mean_dose = statistics.mean(all_mean_dose)
overall_std_dose = statistics.stdev(all_mean_dose)

overall_mean_schedule = statistics.mean(all_mean_schedule)
overall_std_schedule = statistics.stdev(all_mean_schedule)

pareto_mean_dose_overall = statistics.mean(pareto_mean_dose)
pareto_std_dose = statistics.stdev(pareto_mean_dose)

pareto_mean_schedule_overall = statistics.mean(pareto_mean_schedule)
pareto_std_schedule = statistics.stdev(pareto_mean_schedule)

"""
summary_text = (
    f"Full: μ_v={overall_mean_dose:.3f}, σ_v={overall_std_dose:.3f} | "
    f"μ_t={overall_mean_schedule:.2f}, σ_t={overall_std_schedule:.2f}\n"
    f"Pareto: μ_v={pareto_mean_dose_overall:.3f}, σ_v={pareto_std_dose:.3f}"
    f"μ_t={pareto_mean_schedule_overall:.2f}, σ_t={pareto_std_schedule:.2f}"
)

plt.figtext(0.5, 0.05, summary_text, ha='center', fontsize=10)
"""
plt.tight_layout()
plt.subplots_adjust(bottom=0.25)
plt.savefig(f"{folder}/combined_schedule-dose.png", dpi=300, bbox_inches='tight')
plt.show()




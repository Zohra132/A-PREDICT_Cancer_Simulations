#plots SCHEDULE againts DOSE - for a single .csv
import csv
import matplotlib.pyplot as plt
import statistics


schedules_full, doses_full = [], []
schedules_pareto, doses_pareto = [], []

#Full population
with open("results_run_2_full.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        schedule = float(row["schedule"])
        dose = float(row["dose"])
        schedules_full.append(schedule)
        doses_full.append(dose)

#Pareto front
with open("results_run_2_pareto.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        schedule = float(row["schedule"])
        dose = float(row["dose"])
        schedules_pareto.append(schedule)
        doses_pareto.append(dose)



# Statistics - Full population
mean_schedule_full = statistics.mean(schedules_full)
std_schedule_full = statistics.stdev(schedules_full)

mean_dose_full = statistics.mean(doses_full)
std_dose_full = statistics.stdev(doses_full)

plt.figure(figsize=(8,6))

#Full population
plt.scatter(
    schedules_full, doses_full,
    c='lightgray', s=30, alpha=0.3, label="Full population"
)

#Pareto front
plt.scatter(
    schedules_pareto, doses_pareto,
    c='black', s=80, label="Pareto front"
)

plt.xlabel("Schedule")
plt.ylabel("Dose")
plt.title("Run 2")
plt.legend()
plt.grid(alpha=0.2)

stats_text = (
    f"Full Population Statistics:\n"
    f"Schedule → Mean = {mean_schedule_full:.2f}, Std = {std_schedule_full:.2f}\n"
    f"Dose → Mean = {mean_dose_full:.4f}, Std = {std_dose_full:.4f}"
)
plt.subplots_adjust(bottom=0.25)
plt.figtext(0.5, 0.02, stats_text, ha="center", fontsize=10)
 
#plt.savefig("pop24-gen4-0.7-0.25/schedule_vs_dose_run2.png", dpi=300)
plt.show()
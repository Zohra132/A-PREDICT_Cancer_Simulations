#plots TIME againts SCHEDULE - for a single .csv
import csv
import matplotlib.pyplot as plt
import statistics


times_full, schedule_full = [], []
times_pareto, schedule_pareto = [], []

# Full population
with open("results_run_2_full.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        times_full.append(float(row["time"]))
        schedule_full.append(float(row["schedule"]))

# Pareto front
with open("results_run_2_pareto.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        times_pareto.append(float(row["time"]))
        schedule_pareto.append(float(row["schedule"]))


mean_schedule_full = statistics.mean(schedule_full)
std_schedule_full = statistics.stdev(schedule_full)

mean_time_full = statistics.mean(times_full)
std_time_full = statistics.stdev(times_full)



plt.figure(figsize=(8, 6))

plt.scatter(
    times_full, schedule_full,
    c='lightgray', s=30, alpha=0.3, label="Full population"
)

plt.scatter(
    times_pareto, schedule_pareto,
    c='black', s=80, label="Pareto front"
)

plt.xlabel("Time (timesteps)")
plt.ylabel("Schedule")
plt.title("Run 4")
plt.legend()
plt.grid(alpha=0.2)

stats_text = (
    f"Full Population Statistics:\n"
    f"Schedule → Mean = {mean_schedule_full:.2f}, Std = {std_schedule_full:.2f}\n"
    f"TIme → Mean = {mean_time_full:.4f}, Std = {std_time_full:.4f}"
)
plt.subplots_adjust(bottom=0.25)
plt.figtext(0.5, 0.02, stats_text, ha="center", fontsize=10)
 
#plt.savefig("pop24-gen4-0.9-0.1/schedule_vs_time_run4.png", dpi=300)
plt.show()
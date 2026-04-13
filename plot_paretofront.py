#plots VCONC against TIME - for a single .csv
import csv
import matplotlib.pyplot as plt
import statistics

times_full, vasculars_full = [], []
times_pareto, vasculars_pareto = [], []

# Load full population
with open("results_run_2_full.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        vascular = float(row["vascular"])
        time = float(row["time"])
        if vascular > 0 and time < 99999:
            times_full.append(time)
            vasculars_full.append(vascular)

# Load Pareto front
with open("results_run_2_pareto.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        vascular = float(row["vascular"])
        time = float(row["time"])
        if vascular > 0 and time < 99999:
            times_pareto.append(time)
            vasculars_pareto.append(vascular)


mean_vascular_full = statistics.mean(vasculars_full)
std_vascular_full = statistics.stdev(vasculars_full)

mean_time_full = statistics.mean(times_full)
std_time_full = statistics.stdev(times_full)


fig, ax = plt.subplots(figsize=(10, 7))

#Full population
ax.scatter(
    times_full, vasculars_full,
    marker='x', s=30, c='gray', alpha=0.3,
    label='Full population'
)

#Pareto front
ax.scatter(
    times_pareto, vasculars_pareto,
    marker='o', s=80, c='black', alpha=0.9,
    label='Pareto front'
)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_xlabel("Time (minimise)")
ax.set_ylabel("Vascular score (maximise)")
plt.ylim(0, 1.05)
ax.legend()

plt.title("Run 4")
stats_text = (
    f"Full Population Statistics:\n"
    f"Vascular → Mean = {mean_vascular_full:.2f}, Std = {std_vascular_full:.2f}\n"
    f"Time → Mean = {mean_time_full:.4f}, Std = {std_time_full:.4f}"
)
plt.subplots_adjust(bottom=0.25)
plt.figtext(0.5, 0.02, stats_text, ha="center", fontsize=10)
 
#plt.savefig("pop24-gen4-0.9-0.1/paretofront-run4.png", dpi=300, bbox_inches='tight')
plt.show()

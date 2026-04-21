import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

folder = "pop100-main"
runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

all_points = []

for run in runs:
    df = pd.read_csv(f"{folder}/results_run_{run}_pareto.csv")

    for _, row in df.iterrows():
        v = float(row["vascular"])
        t = float(row["time"])

        if v > 0 and t < 99999:
            all_points.append((t, v))

all_points = np.array(all_points)
times = all_points[:, 0]
vasculars = all_points[:, 1]

#non-dominated filter
def is_dominated(i, times, vasculars):
    for j in range(len(times)):
        if j == i:
            continue

        # j dominates i if:
        # better or equal in both, and strictly better in one
        if (
            (times[j] <= times[i] and vasculars[j] >= vasculars[i]) and
            (times[j] < times[i] or vasculars[j] > vasculars[i])
        ):
            return True
    return False


pareto_mask = []
for i in range(len(times)):
    pareto_mask.append(not is_dominated(i, times, vasculars))

pareto_mask = np.array(pareto_mask)

pareto_times = times[pareto_mask]
pareto_vasculars = vasculars[pareto_mask]

#sort
sorted_idx = np.argsort(pareto_times)
pareto_times = pareto_times[sorted_idx]
pareto_vasculars = pareto_vasculars[sorted_idx]


#prints points to terminal
print("\nGlobal Pareto Front Points:")
print("Time\tVascular")
for t, v in zip(pareto_times, pareto_vasculars):
    print(f"{t:.4f}\t{v:.4f}")

print("\nAll Pareto Front Points:")
print("Time\tVascular")
for t, v in zip(times, vasculars):
    print(f"{t:.4f}\t{v:.4f}")


#plot
plt.figure(figsize=(7, 6))
plt.scatter(times, vasculars, alpha=0.2, s=20, label="All Pareto points")

#global Pareto front
plt.scatter(pareto_times, pareto_vasculars, color='black', s=60, label="Global Pareto front")
plt.plot(pareto_times, pareto_vasculars, color='black', linewidth=2)

plt.xlabel("Time (minimise)")
plt.ylabel("Vascular score (maximise)")
plt.title("Global Pareto Front (All Runs Combined)")

#plt.ylim(0, 1.05)
plt.ylim(0.6, 1.02)
plt.yticks(np.arange(0.6, 1.01, 0.05))
plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig(f"{folder}/global_pareto_front.png", dpi=300)
plt.show()
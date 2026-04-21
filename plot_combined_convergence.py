import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

folder = "pop100-main"
runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

all_conv = []

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)

for run in runs:
    df = pd.read_csv(f"{folder}/results_run_{run}_pareto_gen_vegf8.0.csv")

    conv = df.groupby('generation').agg(
        best_vascular=('vascular', 'max'),
        best_time=('time', 'min')
    ).reset_index()

    all_conv.append(conv)

    # plot individual run
    plt.plot(
        conv['generation'],
        conv['best_vascular'],
        alpha=0.3
    )

# align generations
gens = sorted(set().union(*[c['generation'] for c in all_conv]))

# mean vascular
mean_vasc = []
for g in gens:
    vals = [c[c['generation'] == g]['best_vascular'].values[0]
            for c in all_conv if g in c['generation'].values]
    mean_vasc.append(np.mean(vals))

plt.plot(gens, mean_vasc, color='black', linewidth=3, label='Mean')

plt.axhline(y=0.9, color='red', linestyle='--', label='Threshold')
plt.xlabel("Generation")
plt.ylabel("Best vascular score")
plt.title("Convergence (Vascular)")
plt.legend()
plt.grid(alpha=0.3)


plt.subplot(1, 2, 2)

# individual runs 
for conv in all_conv:
    plt.plot(
        conv['generation'],
        conv['best_time'],
        alpha=0.3
    )

#extended mean
max_gen = max(c['generation'].max() for c in all_conv)
full_gens = np.arange(0, max_gen + 1)

aligned_time = []

for conv in all_conv:
    c = conv.set_index('generation').reindex(full_gens)

    c['best_time'] = c['best_time'].ffill()

    aligned_time.append(c['best_time'].values)

aligned_time = np.array(aligned_time)

mean_time = np.mean(aligned_time, axis=0)

plt.plot(full_gens, mean_time, color='black', linewidth=3, label='Mean')

plt.xlabel("Generation")
plt.ylabel("Best time")
plt.title("Convergence (Time)")
plt.legend()
plt.grid(alpha=0.3)


plt.tight_layout()
plt.savefig(f"{folder}/combined_convergence_all_runs.png", dpi=300)
plt.show()
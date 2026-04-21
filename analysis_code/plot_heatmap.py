import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
import re

folder_path = "./results0.6-0.05/"
files = glob.glob(os.path.join(folder_path, "*.csv"))

print(f"Found {len(files)} files.")

results = []

for file in files:

    filename = os.path.basename(file)

    # extract parameters from filename
    dose = float(re.search(r"dose_(\d+\.?\d*)", filename).group(1))
    vconc = float(re.search(r"Vconc_(\d*\.?\d*)", filename).group(1))

    # read raw lines
    with open(file) as f:
        lines = f.readlines()

    # time: extract the second row 
    time = np.array([x for x in lines[2].strip().split("\t") if x != ""], dtype=float)

    # VASC: third from last row 
    vasc_row = np.array([x for x in lines[7].strip().split("\t") if x != ""], dtype=float)



    vasc_metric = np.trapezoid(vasc_row, time) #area under curve
    #vasc_metric = np.max(vasc_row) #max vasc_score
    #vasc_metric = np.mean(vasc_row) #mean vasc score
    #vasc_metric = vasc_row[-1] #final vasc score


    results.append({
        "dose": dose,
        "vconc": vconc,
        "VASC_score": vasc_metric
    })

df = pd.DataFrame(results)

# average runs
df = df.groupby(["dose","vconc"]).mean().reset_index()

# create heatmap matrix
heatmap_data = df.pivot(index="dose", columns="vconc", values="VASC_score")

plt.figure(figsize=(8,6))

ax = sns.heatmap(
    heatmap_data,
    cmap="plasma",
    #annot=True,
    #fmt=".1f",
    #linewidths=0.5
)

plt.xlabel("Vconc")
plt.ylabel("Dose")

cbar = ax.collections[0].colorbar
#cbar.ax.invert_yaxis()

low = heatmap_data.min().min()
high = heatmap_data.max().max()

cbar.set_ticks([low, high])
cbar.set_ticklabels(["Low vasc", "High vasc"])

plt.tight_layout()
plt.savefig(f"heatmap-plots/heatmap-vasc_dose-vconc_AUC.png", dpi=300, bbox_inches="tight")
plt.show()
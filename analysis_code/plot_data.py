#Code Bentley Lab created, currently confidential as paper under review Au et al Cancer Cell 2026
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

filename = "simulation_data_param_set_1_new_format.csv"
df = pd.read_csv(filename)

# used to automatically display the formatted name on the graph eg "Dll4 Average" instead of "dll4_average"
output_names = {
    "drug_gut_mgL": "Drug Gut (mg/L)",
    "drug_blood_mgL": "Drug Blood (mg/L)",
    "drug_blood_nM": "Drug Blood (nM)",
    "vasc_score": "Vascularisation Score",
    "vegfr_inhibition": "VEGFR Inhibition",
    "dll4_average": "Dll4 Average"
}

# select the output you want from
output = "dll4_average"

# select which dose you want
dose = 0.5

# Filter for dose
# df_dose = df[df["dose"] == dose]
df_dose = df[df["dose"] == dose].copy()

# Detect which gradient is in the data
gradient_value = df_dose["gradient"].iloc[0]  # safe since all rows have same gradient

# based on the gradient value select the correct vegf output
if gradient_value == 2:
    vegf_output = "VconcST"
else:
    vegf_output = "Vconc"

# Group by time and condition, take mean across runs
# grouped = df_dose.groupby(["dose", vegf_output, "hours"], as_index=False).mean(numeric_only=True)

grouped = df_dose.groupby([vegf_output, "hours"]).agg(mean_val=(output, "mean"), std_val=(output, "std")).reset_index()

# Get each unique VconcST/Vconc value for this dose
vegf_concentration_values = grouped[vegf_output].unique()

plt.figure(figsize=(8, 5))

bar_step = 10  # display a standard error bar every 10 data points

# Plot output (eg Dll4) over time for each value of VconcST/Vconc
for value in sorted(vegf_concentration_values):
    # original plotting
    # df_output_for_vegf_value = grouped[grouped[vegf_output] == value].sort_values(by="hours")
    # plt.plot(df_output_for_vegf_value["hours"], df_output_for_vegf_value[f"{output}"],
    #          linewidth=1, alpha=0.8, linestyle="-", label=f"{vegf_output} = {value}")

    # plotting with sd as low alpha shaded area.
    df_plot = grouped[grouped[vegf_output] == value].sort_values("hours")

    # plot mean line
    plt.plot(
        df_plot["hours"], df_plot["mean_val"],
        linewidth=1.5, label=f"{vegf_output} = {value}"
    )

    # add std shading
    plt.fill_between(
        df_plot["hours"],
        df_plot["mean_val"] - df_plot["std_val"],
        df_plot["mean_val"] + df_plot["std_val"],
        alpha=0.2
    )

    # plot sd as bars but only for some points
    # plt.errorbar(
    #     df_plot["hours"][::bar_step],  # pick every nth point
    #     df_plot["mean_val"][::bar_step],
    #     yerr=df_plot["std_val"][::bar_step],
    #     # fmt='o',
    #     capsize=1,
    #     elinewidth=0.5,
    #     markeredgewidth=0.5,
    #     alpha=0.8
    # )

# automatically populate graph labels and legends using the param_names list to get the formatted text.
plt.xlabel("Hours")
plt.ylabel(f"{output_names[output]}")
plt.title(f"{output_names[output]} Over Time (Dose = {dose})")
plt.legend()
plt.grid(True)
# plt.show() # uncomment this if you want to just show the graph and not save it

# create output directory if needed
output_dir = "new_plots"
os.makedirs(output_dir, exist_ok=True)

# Construct a descriptive filename
outfile = os.path.join(
    output_dir,
    f"axitinib_{output}_gradient_{gradient_value}_{vegf_output}_dose_{dose}_.png"
)

# save the figure to the outile loction
plt.savefig(outfile, dpi=300, bbox_inches="tight")
plt.close()  # close the figure so next plot starts fresh


#Code Bentley Lab created, currently confidential as paper under review Au et al Cancer Cell 2026
import plotly.graph_objects as go
import pandas as pd
import re

filename = "simulation_data_param_set_5_new_format.csv"
df = pd.read_csv(filename)

# Detect which gradient is in the data
gradient_value = df["gradient"].iloc[0]  # safe since all rows have same gradient

# based on the gradient value select the correct vegf output (Vconc or VconcST)
if gradient_value == 2:
    vegf_output = "VconcST"
else:
    vegf_output = "Vconc"

# Use regex to automate graph title label
match = re.search(r"param_set_(\d+)", filename)
if match:
    param_set_name = f"Parameter Set {match.group(1)}"
else:
    param_set_name = None

# select only the final time point (max hours = 166.5)
max_time = df['hours'].max()
df_max_time_rows = df[df['hours'] == max_time]  # get all rows with max time

# get the mean vasc_score for each dose and vegf concentration combination over all repeats
df_avg = df_max_time_rows.groupby(['dose', vegf_output])['vasc_score'].mean().reset_index()

# ilter out vegf concentrations to scale axis properly
if param_set_name == "Parameter Set 1" or param_set_name == "Parameter Set 3":
    df_avg_filtered = df_avg[df_avg[vegf_output] >= 1.6]

if param_set_name == "Parameter Set 2" or param_set_name == "Parameter Set 4":
    df_avg_filtered = df_avg[df_avg[vegf_output] >= 0.12]


# create pivot table as is the correct format for plotly z array
z_data = df_avg_filtered.pivot(index='dose', columns=vegf_output, values='vasc_score')

# z_data = df_avg.pivot(index='dose', columns=vegf_output, values='vasc_score')

fig = go.Figure(data=go.Contour(
    z=z_data.values,    # average vasc_score
    x=z_data.columns,   # vegf concentration (x-axis)
    y=z_data.index,     # Drug dose (y-axis)
    contours=dict(
        coloring="heatmap",
        showlabels=True,
        labelfont=dict(size=20, color="white")  # controls contour label font
    ),
    colorbar=dict(
        title="Vascular Score",
        title_font=dict(size=30),  # colorbar title
        tickfont=dict(size=20)     # colorbar tick labels
    )
))

fig.update_layout(
    title=f"{param_set_name}: Average Vascular Score at {max_time} hours",
    title_font=dict(size=30),  # main title font
    xaxis=dict(
        title="VEGF concentration",
        title_font=dict(size=30),  # x-axis label
        tickfont=dict(size=20)     # x-axis tick labels
    ),
    yaxis=dict(
        title="Drug dose",
        title_font=dict(size=30),  # y-axis label
        tickfont=dict(size=20)     # y-axis tick labels
    ),
)

fig.show()

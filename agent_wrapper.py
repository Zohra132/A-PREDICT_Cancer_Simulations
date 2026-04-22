#agent_wrapper.py
import subprocess
import pandas as pd
import numpy as np
import os


def run_simulation(drug_schedule, dailyDose, vegfconc, runID, output):

    os.makedirs(output, exist_ok=True)

    cmd = [
        "../springAgent",
        str(drug_schedule),
        str(dailyDose),
        "0", #readInGradient
        "0.04", #VconcST
        str(vegfconc),
        str(runID)
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=output)

    vegf_str = str(int(vegfconc)) if vegfconc.is_integer() else str(vegfconc)
    filename = f"{drug_schedule}_dose_{dailyDose}_gradient_0_VconcST_0.04_Vconc_{vegf_str}_run_{runID}.csv"
    #return filename
    return os.path.join(output, filename)


def parse_output(filename) -> dict:
    rows = []
    with open(filename, "r") as f:
        for line in f:
            # split on any whitespace and remove empty entries
            parts = [p for p in line.strip().split() if p]
            if len(parts) > 0:
                rows.append(list(map(float, parts)))
    
    rows = [np.array(r) for r in rows]
    
    data = {
        "params": rows[0],
        "time_hours": rows[1],
        "drug_tumour": rows[2],
        "drug_gut": rows[3],
        "drug_blood_mgL": rows[4],
        "drug_blood_nM": rows[5],
        "vascularisation": rows[6],
        "drugEffect_VR2": rows[7],
        "dll4": rows[8]
    }

    return data

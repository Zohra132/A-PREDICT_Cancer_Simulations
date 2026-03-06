#agent_warpper.py
import os
import shutil
import subprocess
import pandas as pd
import numpy as np
import experiment_config


def run_simulation(drug_schedule, dailyDose, vegfconc, runID):
    cmd = [
        "./SpringAgent",
        str(drug_schedule),
        str(dailyDose),
        "0", #readInGradient
        "0.04", #VconcST
        str(vegfconc),
        str(runID)
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    vegf_str = str(int(vegfconc)) if vegfconc.is_integer() else str(vegfconc)
    filename = f"{drug_schedule}_dose_{dailyDose}_gradient_0_VconcST_0.04_Vconc_{vegf_str}_run_{runID}.csv"
    return filename


def parse_output(filename) -> dict:

    rows = []

    with open(filename, "r") as f:
        for line in f:
            # split on any whitespace and remove empty entries
            parts = [p for p in line.strip().split() if p]
            if len(parts) > 0:
                rows.append(list(map(float, parts)))
    
    rows = [np.array(r) for r in rows]
        
    def to_float_list(row):
        # remove empty strings
        return [float(x) for x in row if x.strip()!='']
     
        #1: 2880    0   0   0   0.8   1   1           ← parameters
        #2:                                           ← empty line
        #3: 0  0.25 0.5 0.75 1 1.25 ...               ← time 
        #4: 0 0 0 0 ...                               ← drug tumour
        #5: 0 0 0 0 ...                               ← drug gut
        #6: 0 0 0 0 ...                               ← mg/L blood
        #7: 0 0 0 0 ...                               ← nM blood
        #8: 0 0 0 0 ...                               ← supplyLine - vascularisation score
        #9: 0 0 0 0 ...                               ← drugEffect
        #10: 0 2038.89 53.53 ... 1450                 ← Dll4_store

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

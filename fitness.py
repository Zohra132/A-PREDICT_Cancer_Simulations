#fitness.py
import numpy as np



def evaluate_run(data, threshold=0.9):

    vascular = np.array(data["vascularisation"])
    time = np.array(data["time_hours"])

    peak_vascular = np.max(vascular)

    #find first time threshold is reached
    for v, t in zip(vascular, time):
        if v >= threshold:
            return peak_vascular, t

    # threshold never reached
    return peak_vascular, 99999
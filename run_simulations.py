import subprocess
import itertools
from multiprocessing import Pool, cpu_count

def run_simulation(args):

    drug_schedule, dailyDose, VEGFconc, runID, readInGradient, VconcST = args

    cmd = [
        "./SpringAgent",
        str(drug_schedule),
        str(dailyDose),
        str(readInGradient),
        str(VconcST),
        str(VEGFconc),
        str(runID)
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    filename = f"{drug_schedule}_dose_{dailyDose}_gradient_{readInGradient}_VconcST_{VconcST}_Vconc_{VEGFconc}_run_{runID}.csv"
    return filename


if __name__ == "__main__":
    drug_schedule = 2940
    VEGFconc_values = [8.0, 7.2, 6.4, 5.6, 4.8, 4.0, 3.2, 2.4, 1.6, 0.8]
    dailyDose_values = [0.05, 0.1, 0.2]
    num_runs = 1



    param_list = [
        (drug_schedule, dailyDose, VEGFconc, runID, 0, 0.04)
        for dailyDose, VEGFconc in itertools.product(dailyDose_values, VEGFconc_values)
        for runID in range(num_runs)
    ]

    #multiprocessing to run simulations in parallel
    n_processes = min(cpu_count(), len(param_list))
    with Pool(processes=n_processes) as pool:
        results = pool.map(run_simulation, param_list)

    for filename in results:
        print("Output file:", filename)


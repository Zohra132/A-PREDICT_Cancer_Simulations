# main.py
import os
import csv
from nsga import run_nsga
from deap import tools
import argparse




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.9, help="vascularisation threshold")
    args = parser.parse_args()

    THRESHOLD = args.threshold
    POP_SIZE = 4
    NGEN = 2
    CX_PB = 0.7
    MUT_PB = 0.25

    output_file = "optimiser-run4.csv"
    file_exists = os.path.isfile(output_file)



    VEGF_levels = [8.0, 4.0, 0.8]
    for vegf in VEGF_levels:
        print(f"Running optimization for VEGF = {vegf}")

        final_population = run_nsga(
            vegfconc=vegf,
            pop_size=POP_SIZE,
            ngen=NGEN,
            cxpb=CX_PB,
            mutpb=MUT_PB,
            threshold=THRESHOLD
        )

        #performs non-dominated sorting on the whoel populationa dn returns the first front
        pareto = tools.sortNondominated(
            final_population,
            k=len(final_population),
            first_front_only=True
        )[0]

        with open(output_file, 'a', newline='') as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(['schedule', 'dose', 'vegfconc', 'vascular', 'time'])
                file_exists = True

            for ind in pareto:
                writer.writerow([
                    ind[0], #schedule
                    ind[1], #dose 
                    vegf,
                    ind.fitness.values[0],
                    ind.fitness.values[1]
                ])

    print(f'Pareto saved to {output_file}')


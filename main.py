#main.py
import os
import csv
from nsga import run_nsga
from deap import tools
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    """
    Example command:
    python3 main.py 
    --pop_size 100
    --n_gen 50
    --threshold 0.9 
    --cx_prob 0.9 
    --mut_prob 0.1 
    --output_filename results
    --vegf 8 7.2 6.4 
    --schedule_min 100 
    --schedule_max 7000 
    --dose_min 1 
    --dose_max 800
    """
    
    parser.add_argument("--pop_size", type=int, default=8, help="population size must be a multiple of 4") 
    parser.add_argument("--n_gen", type=int, default=10, help="number of generations")
    parser.add_argument("--threshold", type=float, default=0.9, help="vascularisation threshold")
    parser.add_argument("--cx_prob", type=float, default=0.9, help="crossover probability")
    parser.add_argument("--mut_prob", type=float, default=0.1, help="mutation probability")
    parser.add_argument("--output_filename", type=str, default="output123", help="output file")
    parser.add_argument("--vegf", type=float, nargs="+", default=[8.0, 7.2, 6.4], help="one or more VEGF levels")
    parser.add_argument("--schedule_min", type=int, default=100, help="minimium schedule timesteps")
    parser.add_argument("--schedule_max", type=int, default=7000, help="maximum schedule timesteps")
    parser.add_argument("--dose_min", type=float, default=1, help="minimium drug dose")
    parser.add_argument("--dose_max", type=float, default=800, help="maximum drug dose")

    args = parser.parse_args()
    
    POP_SIZE = args.pop_size
    NGEN = args.n_gen
    THRESHOLD = args.threshold
    CX_PB = args.cx_prob
    MUT_PB = args.mut_prob
    FILENAME = args.output_filename
    VEGF = args.vegf
    SCHEDULE_MIN = args.schedule_min
    SCHEDULE_MAX = args.schedule_max
    DOSE_MIN = args.dose_min
    DOSE_MAX = args.dose_max
    run_number = 1



    for vegf in VEGF:
        print(f"Running optimization for VEGF = {vegf}")

        final_population, pareto_log = run_nsga(
            vegfconc=vegf,
            pop_size=POP_SIZE,
            ngen=NGEN,
            cxpb=CX_PB,
            mutpb=MUT_PB,
            threshold=THRESHOLD,
            schedule_min=SCHEDULE_MIN,
            schedule_max=SCHEDULE_MAX,
            dose_min=DOSE_MIN,
            dose_max=DOSE_MAX,
            output=FILENAME
        )

        pareto_gen_file = os.path.join(FILENAME, f"{FILENAME}_pareto_gen_vegf{vegf}.csv")
        with open(pareto_gen_file, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    'generation',
                    'schedule',
                    'dose',
                    'vegfconc',
                    'vascular',
                    'time',
                    'converged_at'
                ]
            )
            writer.writeheader()
            writer.writerows(pareto_log)


        run_number += 1 

        pareto_file = os.path.join(FILENAME, f"{FILENAME}_pareto.csv")
        full_file   = os.path.join(FILENAME, f"{FILENAME}_full.csv")

        pareto_exists = os.path.isfile(pareto_file)
        full_exists = os.path.isfile(full_file)

        #performs non-dominated sorting on the whole populationa and returns the first front
        pareto = tools.sortNondominated(
            final_population,
            k=len(final_population),
            first_front_only=True
        )[0]

        with open(pareto_file, 'a', newline='') as f:
            writer = csv.writer(f)

            if not pareto_exists:
                writer.writerow(['schedule', 'dose', 'vegfconc', 'vascular', 'time'])
                #file_exists = True
                pareto_exists=True

            for ind in pareto:
                writer.writerow([
                    ind[0], #schedule
                    ind[1], #dose 
                    vegf,
                    ind.fitness.values[0],
                    ind.fitness.values[1]
                ])

        # Write full final population
        with open(full_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not full_exists:
                writer.writerow(['schedule', 'dose', 'vegfconc', 'vascular', 'time'])
                full_exists = True
            for ind in final_population:
                writer.writerow([
                    ind[0],
                    ind[1],
                    vegf,
                    ind.fitness.values[0],
                    ind.fitness.values[1]
                ])

    print(f'Pareto saved to {pareto_file}')
    print(f"Full population saved to {full_file}")


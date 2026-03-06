# main.py
import os
import csv
from nsga import run_nsga
from deap import tools
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    """
    parser.add_argument("--pop_size", type=int, default=4, help="population size")
    parser.add_argument("--n_gen", type=int, default=2, help="number of generations")
    parser.add_argument("--threshold", type=float, default=0.9, help="vascularisation threshold")
    parser.add_argument("--cx_prob", type=float, default=0.7, help="crossover probability")
    parser.add_argument("--mut_prob", type=float, default=0.25, help="mutation probability")
    parser.add_argument("--output_filename", type=str, default="output", help="output file")
    parser.add_argument("--schedule_min", type=int, default=60, help="minimium schedule timesteps")
    parser.add_argument("--schedule_max", type=int, default=8640, help="maximum schedule timesteps")
    parser.add_argument("--dose_min", type=int, default=60, help="minimium drug dose")
    parser.add_argument("--dose_max", type=int, default=8640, help="maximum drug dose")
    """

    parser.add_argument("pop_size", type=int, nargs="?", default=4, help="population size")
    parser.add_argument("n_gen", type=int, nargs="?", default=2, help="number of generations")
    parser.add_argument("threshold", type=float,nargs="?",  default=0.9, help="vascularisation threshold")
    parser.add_argument("cx_prob", type=float, nargs="?", default=0.7, help="crossover probability")
    parser.add_argument("mut_prob", type=float, nargs="?", default=0.25, help="mutation probability")
    parser.add_argument("output_filename", type=str, nargs="?", default="output", help="output file")
    parser.add_argument("schedule_min", type=int, nargs="?", default=60, help="minimium schedule timesteps")
    parser.add_argument("schedule_max", type=int, nargs="?", default=8640, help="maximum schedule timesteps")
    parser.add_argument("dose_min", type=int, nargs="?", default=60, help="minimium drug dose")
    parser.add_argument("dose_max", type=int, nargs="?", default=8640, help="maximum drug dose")

    args = parser.parse_args()
    
    POP_SIZE = args.pop_size
    NGEN = args.n_gen
    THRESHOLD = args.threshold
    CX_PB = args.cx_prob
    MUT_PB = args.mut_prob
    SCHEDULE_MIN = args.schedule_min
    SCHEDULE_MAX = args.schedule_max
    DOSE_MIN = args.dose_min
    DOSE_MAX = args.dose_max

    output_file = "optimiser-run4.csv"
    #output_file = "{args.output_filename}.csv"
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
            threshold=THRESHOLD,
            schedule_min=SCHEDULE_MIN,
            schedule_max=SCHEDULE_MAX,
            dose_min=DOSE_MIN,
            dose_max=DOSE_MAX
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

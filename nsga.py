#nsga.py
import random
import numpy as np
from deap import base, creator, tools, algorithms
from fitness import evaluate_run
from agent_wrapper import run_simulation, parse_output
from functools import partial
import multiprocessing
import csv

#GRADIENT = 0
#VCONCST = 0.04

#SCHEDULE_MIN, SCHEDULE_MAX = 60, 8640  #timesteps: 1h to 24h
#DOSE_MIN, DOSE_MAX = 0, 5


def sample_schedule(schedule_min, schedule_max):
    return random.randint(
        schedule_min // 10,
        schedule_max // 10
    ) * 10

##types
def sample_dose(dose_min, dose_max):
    return round(random.uniform(dose_min, dose_max), 2)

if not hasattr(creator, "FitnessMulti"):
    creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0)) #maximize vascular_score, minimize time

if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMulti)

# Evaluation function
def evaluate_solution(individual, run_id, vegfconc, threshold=0.9):

    #Run SpringAgent simulation for a given schedule and dose.
    #Returns: (negative vascular score, time to threshold)

    schedule = int(individual[0]) #schedule as int
    dose = round(float(individual[1]), 2) #round the float to 2dp

    #schedule, dose = individual
    filename = run_simulation(int(schedule), dose, vegfconc, run_id)
    data = parse_output(filename) ######FIX to ensure correct line
    obj1, obj2 = evaluate_run(data, threshold)
    return obj1, obj2


##initialisation
def make_toolbox(schedule_min, schedule_max, dose_min, dose_max):
    toolbox = base.Toolbox()
    toolbox.register(
        "attr_schedule", 
        random.randrange, 
        schedule_min, 
        schedule_max +1, 
        10
    )
    toolbox.register("attr_dose", sample_dose, dose_min, dose_max)
    toolbox.register(
        "individual", 
        tools.initCycle, 
        creator.Individual, 
        (toolbox.attr_schedule, toolbox.attr_dose), 
        n=1
    )
    toolbox.register(
        "population", 
        tools.initRepeat, 
        list, 
        toolbox.individual
    )


    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=0.5)
    toolbox.register("select", tools.selNSGA2)

    return toolbox


##helper functions enforces bounds and enforces 2 decimal point num for dose
def repair_individual(ind, schedule_min, schedule_max, dose_min, dose_max):
    # schedule stays integer and within bounds
    ind[0] = int(round(ind[0] / 10.0)) * 10
    ind[0] = max(schedule_min, min(schedule_max, ind[0]))

    # dose stays float within bounds, 2 dp only
    ind[1] = round(ind[1], 2)
    ind[1] = max(dose_min, min(dose_max, ind[1]))

    return ind


#algorithm
def run_nsga(vegfconc, pop_size, ngen, cxpb, mutpb, threshold, schedule_min, schedule_max, dose_min, dose_max):
    toolbox = make_toolbox(schedule_min, schedule_max, dose_min, dose_max)
    pool = multiprocessing.Pool()

    # Initialize population
    population = toolbox.population(n=pop_size) #each individual [schedule, dose]

    run_counter = 0 

    # ----- Evaluate initial population -----
    args_list = [(ind, i, vegfconc) for i, ind in enumerate(population)] #(individual1, 0, vegfconc) (individual2, 1, vegfconc)...

    results = pool.starmap(evaluate_solution, args_list) #runs all simulations in parallel

    for ind, fit in zip(population, results):
        ind.fitness.values = fit #(individual).fitness.values = (obj1, obj2)

    run_counter += len(population)

    population = tools.selNSGA2(population, len(population)) #performs non-dominated sorting, assigns crowding distance, prepares population for selection
    
    # ----- Evolution -----
    for gen in range(1, ngen + 1):
        print(f"Generation {gen} (VEGF: {vegfconc})")

        #parent selection
        offspring = tools.selTournamentDCD(population, len(population)) #select offspring
        offspring = [toolbox.clone(ind) for ind in offspring] #clone so parents are not modified

        # Crossover
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                repair_individual(child1, schedule_min, schedule_max, dose_min, dose_max)
                repair_individual(child2, schedule_min, schedule_max, dose_min, dose_max)
                del child1.fitness.values
                del child2.fitness.values

        # Mutation
        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                repair_individual(mutant, schedule_min, schedule_max, dose_min, dose_max)
                del mutant.fitness.values

        # Evaluate valid individuals
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        args_list = [(ind, run_counter + idx, vegfconc)
                     for idx, ind in enumerate(invalid_ind)]

        results = pool.starmap(
            partial(evaluate_solution, threshold=threshold),
            args_list
        )

        #assign fitnesds
        for ind, fit in zip(invalid_ind, results):
            ind.fitness.values = fit
        
        run_counter += len(invalid_ind) 

        #chooses best from parent+offspring
        population = toolbox.select(population + offspring, k=pop_size)

        best = tools.selBest(population, 1)[0]
        print(f"Best this gen: schedule={best[0]}, dose={best[1]}, fitness={best.fitness.values}")


    pool.close()
    pool.join()

    return population
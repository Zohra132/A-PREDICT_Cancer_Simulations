#nsga.py
import random
from deap import base, creator, tools
from fitness import evaluate_run
from agent_wrapper import run_simulation, parse_output
from functools import partial
import multiprocessing
import copy



if not hasattr(creator, "FitnessMulti"):
    creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0)) #maximize vascular_score, minimize time

if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMulti)

# Evaluation function
def evaluate_solution(individual, run_id, vegfconc, threshold=0.75):

    #Runs SpringAgent simulation for a given schedule and doseand returns negative vascular score, time to threshold
    schedule = int(individual[0]) #schedule as int
    dose = round(float(individual[1]), 2) #round the float to 2dp

    #schedule, dose = individual
    dose = int(dose) if dose.is_integer() else str(dose)
    filename = run_simulation(int(schedule), dose, vegfconc, run_id)
    data = parse_output(filename) 
    obj1, obj2 = evaluate_run(data, threshold)
    return obj1, obj2

def mutate_individual(ind, schedule_min, schedule_max, dose_min, dose_max):
    ind[0] = int(ind[0])
    ind[1] = float(ind[1])
    ind[0] += random.choice([-200, -100, -50, 50, 100, 200])
    ind[1] += random.gauss(0, 0.2)
    repair_individual(ind, schedule_min, schedule_max, dose_min, dose_max)
    return (ind,)

##initialisation
def make_toolbox(schedule_min, schedule_max, dose_min, dose_max, mutpb):
    toolbox = base.Toolbox()
    toolbox.register(
        "attr_schedule", 
        random.randrange, 
        schedule_min, 
        schedule_max +1, 
        10
    )
    toolbox.register(
        "attr_dose",
        lambda: round(random.uniform(dose_min, dose_max), 2)
    )
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
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", mutate_individual, 
                    schedule_min=schedule_min, 
                    schedule_max=schedule_max, 
                    dose_min=dose_min, 
                    dose_max=dose_max)
    toolbox.register("clone", copy.deepcopy)
    toolbox.register("select", tools.selNSGA2)

    return toolbox


##helper functions enforces bounds and enforces 2 decimal point num for dose
def repair_individual(ind, schedule_min, schedule_max, dose_min, dose_max):
    # schedule stays integer and within bounds
    ind[0] = int(round(ind[0] / 10.0)) * 10
    ind[0] = max(schedule_min, min(schedule_max, ind[0]))

    #dose stays float within bounds, 2 dp only
    ind[1] = round(ind[1], 2)
    ind[1] = max(dose_min, min(dose_max, ind[1]))

    return ind

def pareto_signature(front):
    return {
        (round(ind.fitness.values[0], 1), #1 .dp
        round(ind.fitness.values[1])) #its an int anyway
        for ind in front
    }


#algorithm
def run_nsga(
        vegfconc, 
        pop_size, 
        ngen, 
        cxpb, 
        mutpb, 
        threshold, 
        schedule_min, 
        schedule_max, 
        dose_min, 
        dose_max):
    
    if pop_size % 4 != 0:
        raise ValueError("Population size must be divisible by 4")
    
    toolbox = make_toolbox(schedule_min, schedule_max, dose_min, dose_max, mutpb)
    pool = multiprocessing.Pool()

    # Initialize population
    population = toolbox.population(n=pop_size) #each individual [schedule, dose]

    for ind in population:
        repair_individual(ind, schedule_min, schedule_max, dose_min, dose_max)

    run_counter = 0 

    #Evaluate initial population
    args_list = [(ind, i, vegfconc) for i, ind in enumerate(population)] 
    results = pool.starmap(evaluate_solution, args_list) #runs all simulations in parallel

    for ind, fit in zip(population, results):
        ind.fitness.values = fit 

    run_counter += len(population)
    population = tools.selNSGA2(population, len(population)) #performs non-dominated sorting, assigns crowding distance, prepares population for selection

    pareto_log = []
    pareto_front = tools.sortNondominated(population, len(population), True)[0]
    prev_pareto = pareto_signature(pareto_front)
    stagnation_count = 0       
    stagnation_limit = 5 #stop if no improvement for 5 many gens
 
    #Evolution
    for gen in range(1, ngen + 1):
        print(f"Generation {gen} (VEGF: {vegfconc})")

        #parent selection:tournament/rank
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

        #Mutation
        for mutant in offspring:
            if random.random() < mutpb:
                (mutant, ) = toolbox.mutate(mutant)
                del mutant.fitness.values

        #Evaluate valid individuals
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        args_list = [(ind, run_counter + idx, vegfconc) for idx, ind in enumerate(invalid_ind)]

        results = pool.starmap(
            partial(evaluate_solution, threshold=threshold),
            args_list
        )

        #assign fitness
        for ind, fit in zip(invalid_ind, results):
            ind.fitness.values = fit
        
        run_counter += len(invalid_ind) 

        #chooses best from parent+offspring
        population = toolbox.select(population + offspring, k=pop_size)
        
        pareto_front = tools.sortNondominated(
            population,
            k=len(population),
            first_front_only=True
        )[0]

        for ind in pareto_front:
            pareto_log.append({
                'generation': gen,
                'schedule': ind[0],
                'dose': ind[1],
                'vegfconc': vegfconc,
                'vascular': ind.fitness.values[0],
                'time': ind.fitness.values[1],
                'converged_at': ''
            })        

        current_pareto = pareto_signature(pareto_front)

        if prev_pareto is not None and current_pareto == prev_pareto:
            stagnation_count += 1
        else:
            stagnation_count = 0
            prev_pareto = current_pareto

        if stagnation_count >= stagnation_limit:
            print(f"Converged at generation {gen} (Pareto stagnation)")
            break

    pool.close()
    pool.join()

    return population, pareto_log
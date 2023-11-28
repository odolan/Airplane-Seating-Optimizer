import pandas as pd
import random
from person import Person
from airplane import Airplane
from citizen import Citizen
from copy import deepcopy
from tqdm import tqdm
import statistics

# runs tournament to select parent boarding orders to use as parents for next rounds
def tournament_selection(population, num_survivors):
    survivors = []

    for i in range(num_survivors):
        opponents = random.sample(population, 2)
        winner = opponents[0].battle(opponents[1])
        # deep copy so when a citizen wins multiple times they aren't copied
        survivors.append(deepcopy(winner))

    return survivors

# runs genetic algorithm
def genetic(generations, rows, cols, population_size, num_to_replace):
    passenger_master_list = []
    population = []

    # builds a master list of passengers - this should NOT be mutated after creation :)
    for row in range(rows):
        for col in range(cols):
            passenger_master_list.append(Person(random.uniform(0, 0.35), (row, col)))

    # builds X simulations with same set of passengers, airplane dimensions, etc. but random orderings
    # (from citizen to citizen) to compare, battle, and let the best ordering win out!
    print("BUILDING INITIAL POPULATION...")
    for i in tqdm(range(population_size)):
        population.append(Citizen(rows, cols, deepcopy(passenger_master_list)))

    # update over generations
    for generation in tqdm(range(generations)):

        print("Running Tournaments...")
        # perform tournaments - challenge each member of the population to "survive"
        population = tournament_selection(population, population_size - num_to_replace)

        # mutate some of the surviving members of the population
        print("Running Mutation...")
        for i in range(int(population_size / 6)):
            mutate_index = random.randint(0, len(population) - 1)
            population[mutate_index].mutate(rows)

        print("Running Crossovers...")
        # some of the fit survivors will reproduce, create offspring similar to them
        for i in range(num_to_replace):
            parent1 = population[random.randint(0, len(population) - 1)]
            parent2 = population[random.randint(0, len(population) - 1)]

            population.append(parent1.reproduce(parent2, deepcopy(passenger_master_list)))

        scores = []

        print("Final Scoring...")
        for citizen in population:
            scores.append(citizen.score)

        print("GENERATION ", str(generation + 1), " MIN SCORE IN POPULATION: ", min(scores))
        print("GENERATION ", str(generation + 1), " SCORE: ", statistics.mean(scores))

# GENETIC: generations, rows, cols, pop_size, num to replace
genetic(200, 25, 3, 500, 50)
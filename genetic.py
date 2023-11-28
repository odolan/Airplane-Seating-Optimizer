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

# produces a crossover to combine two parents into one child
def crossover(parent1, parent2):
    # Assuming both parents are lists of people
    crossover_point = len(parent1) // 2

    # Combine the first half of parent1 with the unique individuals from parent2
    child = parent1[:crossover_point]
    child_set = set(child)

    for person in parent2[crossover_point:]:
        if person not in child_set:
            child.append(person)
            child_set.add(person)

    return child

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

        # perform tournaments - challenge each member of the population to "survive"
        population = tournament_selection(population, population_size - num_to_replace)

        for i in range(15):
            mutate_index = random.randint(0, len(population) - 1)
            population[mutate_index].mutate(rows)

        scores = []

        for citizen in population:
            scores.append(citizen.score)

        print("GENERATION ", str(generation + 1), " MIN SCORE IN POPULATION: ", min(scores))
        print("GENERATION ", str(generation + 1), " SCORE: ", statistics.mean(scores))

genetic(100, 8, 3, 100, 0)
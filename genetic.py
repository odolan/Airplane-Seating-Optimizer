import pandas as pd
import random
from person import Person
from airplane import Airplane
import copy

# runs tournament to select parent boarding orders to use as parents for next rounds
def tournament_selection(population, population_fitness, num_of_winners, tournament_size):
    winners = []

    while len(winners) < num_of_winners:
        # Combine the lists using zip and random sample
        population_tuples = [tuple(individual) for individual in population] # convert list to tuple
        population_and_fitness = dict(zip(population_tuples, population_fitness))

        random_tournament = dict(random.sample(list(population_and_fitness.items()), tournament_size))
        # best_boarding_order = min(random_tournament, key=lambda k: random_tournament[k])
        # worst_boarding_order = max(random_tournament, key=lambda k: random_tournament[k])
        best_boarding_order = min(random_tournament, key=lambda k: random_tournament[k])
        worst_boarding_order = max(random_tournament, key=lambda k: random_tournament[k])
        for value in random_tournament.values():
            print(value)
        print(random_tournament[best_boarding_order], random_tournament[worst_boarding_order])


        # random_sample = random.sample(combined_data, tournament_size)
        # random_sample_fitnesses, random_sample_population = zip(*random_sample)

        # print(random_sample_population, random_sample_fitnesses)

        winners.append(1)


# calculates the fitness of a specific boarder ordering 
def fitness(rows, seats_per_row, boarding_order):
    airplane = Airplane(rows=rows, columns=seats_per_row, passengers=boarding_order)

    # ticks through seating all passengers and produces fitness score
    while airplane.single_tick():
        continue

    # note: this score is not normalized
    return airplane.ticks_needed

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

def mutate(member):
    return member

# produces a random bordering order for a plane
def produce_boarding_ordering(rows, cols):
    # generate passengers
    passengers = []

    for row in range(rows):
        for col in range(cols):
            passengers.append(Person(random.uniform(0, 0.35), (row, col)))
        
    random.shuffle(passengers)
    return passengers

# runs genetic algorithm
def genetic(generations):
    rows = 20
    seats_per_row = 4

    # generate a random batch of 100 boarding orders
    population = [produce_boarding_ordering(rows, seats_per_row) for i in range(10)]

    for generation in range(generations):

        # get the fitness of the current population
        population_copy = copy.deepcopy(population)
        population_fitness = [fitness(rows, seats_per_row, i) for i in population_copy]

        # perform tournament selection
        selected_parents = tournament_selection(population=population, population_fitness=population_fitness, num_of_winners=1, tournament_size=1)

        # # perform crossover
        # offspring = [crossover(parent1, parent2) for parent1, parent2 in zip(selected_parents[::2], selected_parents[1::2])]

        # # perform random mutations
        # offspring = [mutate(child) if random.uniform(0, 1) < mutation_rate else child for child in offspring]

        # # update the population with the new offspring
        # population = offspring

genetic(1)
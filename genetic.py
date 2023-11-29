import pandas as pd
import random
from person import Person
from airplane import Airplane
from citizen import Citizen
from copy import deepcopy
from tqdm import tqdm
import statistics
import matplotlib.pyplot as plt

# runs a tournament on the supplied population that will output the given number of survivor
# a tournament is a random pairing of two citizens from the population, and the one with the lowest score (best seating)
# is returned
def tournament_selection(population, num_survivors):
    survivors = []

    for i in range(num_survivors):
        opponents = random.sample(population, 2)
        winner = opponents[0].battle(opponents[1])
        # deep copy so when a citizen wins multiple times they aren't copied
        survivors.append(deepcopy(winner))

    return survivors

min_scores = []
avg_scores = []

# runs genetic algorithm, returns the initial efficient solution among the random population
# and the final, most efficient solution among the random population
def genetic(generations, rows, cols, population_size, num_to_replace, num_to_mutate):
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

    # EXTRACT THE INTIAL MINIMUM FROM THE RANDOMLY GENERATED POPULATION
    min_score = 9999
    initial_min_score_citizen = None

    for citizen in population:
        if citizen.score < min_score:
            min_score = citizen.score
            initial_min_score_citizen = citizen

    # update over generations
    for generation in tqdm(range(generations)):

        print("Running Tournaments...")
        # perform tournaments - challenge each member of the population to "survive"
        population = tournament_selection(population, population_size - num_to_replace)

        # mutate some of the surviving members of the population
        print("Running Mutation...")
        for i in range(num_to_mutate):
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
        min_scores.append(min(scores))
        avg_scores.append(statistics.mean(scores))
    
    plt.ylabel("Generation Score")
    plt.xlabel("Generation")
    x = range(1, generations + 1)
    plt.plot(x, avg_scores, label="Average")
    plt.plot(x, min_scores, label="Minimum")
    plt.legend()
    plt.savefig("ScoreGraph.png")

    min_score = 9999
    final_min_score_citizen = None

    for citizen in population:
        if citizen.score < min_score:
            min_score = citizen.score
            final_min_score_citizen = citizen

    return (initial_min_score_citizen, final_min_score_citizen)


# GENETIC FUNC ARGS: generations, rows, cols, pop_size, num to replace, num to mutate
initial, final = genetic(350, 10, 3, 600, 20, 200)

plt.clf()
plt.xlabel("Nth Passenger in Seating Order")
plt.ylabel("Row of Seat Assignment For nth Passenger")

x = range(len(initial.specific_ordering))
initial_row_data = []
final_row_data = []

for i in range(len(initial.specific_ordering)):
    initial_row_data.append(initial.specific_ordering[i].seat_assignment[0])
    final_row_data.append(final.specific_ordering[i].seat_assignment[0])

plt.scatter(x, initial_row_data, label="Initial")
plt.scatter(x, final_row_data, label="Final")
plt.legend()
plt.savefig("RowGraph.png")

plt.clf()
plt.xlabel("Nth Passenger in Seating Order")
plt.ylabel("Delay Probability of nth Passenger")
initial_row_data = []
final_row_data = []

for i in range(len(initial.specific_ordering)):
    initial_row_data.append(initial.specific_ordering[i].delay_prob)
    final_row_data.append(final.specific_ordering[i].delay_prob)

plt.scatter(x, initial_row_data, label="Initial")
plt.scatter(x, final_row_data, label="Final")
plt.legend()
plt.savefig("DelayGraph.png")


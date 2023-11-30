import pandas as pd
import random
from person import Person
from airplane import Airplane
from citizen import Citizen
from copy import deepcopy
from tqdm import tqdm
import statistics
import matplotlib.pyplot as plt
import numpy as np

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
def genetic(generations, cols, rows, population_size, num_to_replace, num_to_mutate):

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
    
    # plt.ylabel("Generation Score")
    # plt.xlabel("Generation")
    # x = range(1, generations + 1)
    # plt.plot(x, avg_scores, label="Average")
    # plt.plot(x, min_scores, label="Minimum")
    # plt.legend()
    # plt.savefig("ScoreGraph.png")

    min_score = 9999
    final_min_score_citizen = None

    # recover best boarder ordering from the population
    for citizen in population:
        if citizen.score < min_score:
            min_score = citizen.score
            final_min_score_citizen = citizen

    return (final_min_score_citizen)


def get_slowness(ordering):
    return [person.delay_prob for person in ordering]

def get_row_positon(ordering):
    return [person.seat_assignment[0] for person in ordering]

data_x = np.array([]) 
data_y = np.array([])
for _ in range(150):
    print(_)
    ordering = genetic(generations=40, rows=20, cols=3, population_size=100, num_to_replace=15, num_to_mutate=20).specific_ordering
    slowness_vals = get_slowness(ordering)
    data_y = np.append(data_y, slowness_vals, axis=0)
    row_vals = get_row_positon(np.array(ordering))
    data_x = np.append(data_x, row_vals, axis=0)

x_flat = data_x.flatten()
y_flat = data_y.flatten()

print(x_flat.shape)
print(y_flat.shape)


np.savetxt('x_data.txt', x_flat, delimiter=',', header='X Data')
np.savetxt('y_data.txt', y_flat, delimiter=',', header='Y Data')


plt.scatter(x_flat, y_flat, c='blue', marker='o', label='Data Points', alpha=0.02)
plt.xlabel('Position in Line')
plt.ylabel('Slowness')
plt.title('Scatter Plot of Position vs Slowness')
plt.legend()
plt.show()

# plt.clf()
# plt.xlabel("Nth Passenger in Seating Order")
# plt.ylabel("Row of Seat Assignment For nth Passenger")

# x = range(len(initial.specific_ordering))
# initial_row_data = []
# final_row_data = []

# for i in range(len(initial.specific_ordering)):
#     initial_row_data.append(initial.specific_ordering[i].seat_assignment[0])
#     final_row_data.append(final.specific_ordering[i].seat_assignment[0])

# plt.scatter(x, initial_row_data, label="Initial")
# plt.scatter(x, final_row_data, label="Final")
# plt.legend()
# plt.savefig("RowGraph.png")

# plt.clf()
# plt.xlabel("Nth Passenger in Seating Order")
# plt.ylabel("Delay Probability of nth Passenger")
# initial_row_data = []
# final_row_data = []

# for i in range(len(initial.specific_ordering)):
#     initial_row_data.append(initial.specific_ordering[i].delay_prob)
#     final_row_data.append(final.specific_ordering[i].delay_prob)

# plt.scatter(x, initial_row_data, label="Initial")
# plt.scatter(x, final_row_data, label="Final")
# plt.legend()
# plt.savefig("DelayGraph.png")


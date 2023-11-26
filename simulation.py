import random
from person import Person
from airplane import Airplane

# runs a random simulation of an airplane with given dimensions, assigns a passenger to each seat,
# they board in random order
def random_simulation(num_rows, num_cols):
    # generate passengers
    passengers = []

    for row in range(num_rows):
        for col in range(num_cols):
            passengers.append(Person(random.uniform(0, 0.35), (row, col)))
        
    random.shuffle(passengers)

    airplane = Airplane(num_rows, num_cols, passengers)

    # no body needed, function returns boolean, runs as long as is needed
    while airplane.single_tick():
        print(airplane)

    return airplane.ticks_needed


def single_simulation(passenger_list, num_rows, num_cols):
    pass

print(random_simulation(10, 3))
from airplane import Airplane
from person import Person
from copy import deepcopy
import statistics
import random

# Represents a citizen in the population (one single simulation that has a tick count, specific passenger ordering,
# challenged by other citizens to survive, merge/mutates)
class Citizen():
    specific_ordering = []
    airplane = None
    score = 999999
    num_rows = 0
    num_cols = 0

    # creates a simulation for an airplane with given number of rows and columns, starts with random ordering
    # of passengers from supplied master list
    def __init__(self, num_rows, num_cols, passenger_set):
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.specific_ordering = deepcopy(passenger_set)
        random.shuffle(self.specific_ordering)
        
        self.airplane = Airplane(num_rows, num_cols, deepcopy(self.specific_ordering))
        self.score = self.calc_score()

    # mutates this citizen's ordering, updates the airplane too
    def mutate(self, num_swaps):
        for swap in range(num_swaps):
            first = random.randint(0, len(self.specific_ordering) - 1)
            second = random.randint(0, len(self.specific_ordering) - 1)

            temp = self.specific_ordering[first]
            self.specific_ordering[first] = self.specific_ordering[second]
            self.specific_ordering[second] = temp

        ## UPDATE THE ORDERING WITH AIRPLANE
        self.airplane = Airplane(self.num_rows, self.num_cols, deepcopy(self.specific_ordering))
        self.score = self.calc_score()

    # returns a citizen that is the "offspring" of this and the supplied other citizen
    def reproduce(self, other_citizen):
        pass

    # forces this citizen to "battle" with the other to survive, returns the victor/survivor of the two (simply the one with
    # the highest score)
    def battle(self, other_citizen):
        if (self.score <= other_citizen.score):
            return self
        else:
            return other_citizen

    # returns a string representation of this citizen, namely the ordering of the passengers it uses
    def __str__(self):
        result = "PASSENGER ORDER: "
        for passenger in self.specific_ordering:
            result += "\n"
            result += str(passenger)
        
        result += str("\nTicks Needed: ", self.score)

    # calculates a score for this simulation by running a "seating" multiple times (since seatings can vary due to delays)
    def calc_score(self):
        scores = []

        for i in range(250):
            scores.append(self.airplane.calc_ticks())
            self.airplane = Airplane(self.num_rows, self.num_cols, deepcopy(self.specific_ordering))
        
        return statistics.mean(scores)

# passengers = []

# for row in range(30):
#     for col in range(3):
#         passengers.append(Person(random.uniform(0, 0.25), (row, col)))

# citizen = Citizen(30, 3, passengers)

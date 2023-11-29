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
        
        self.update_ordering(self.specific_ordering)

    # mutates this citizen's ordering, updates the airplane too
    def mutate(self, num_swaps):
        for swap in range(num_swaps):
            first = random.randint(0, len(self.specific_ordering) - 1)

            lower_bound = max(0, first - 5)
            upper_bound = min(len(self.specific_ordering) - 1, first + 5)
            second = random.randint(lower_bound, upper_bound)

            temp = self.specific_ordering[first]
            self.specific_ordering[first] = self.specific_ordering[second]
            self.specific_ordering[second] = temp

        ## UPDATE THE ORDERING WITH AIRPLANE
        self.airplane = Airplane(self.num_rows, self.num_cols, deepcopy(self.specific_ordering))
        self.score = self.calc_score()

    # HELPER FUNCTION FOR REPRODUCTION: removes passenger from the list with the supplied seat assignment
    def remove_pass_with_assign(self, passenger_master_list, assignment):
        for i in range(len(passenger_master_list)):
            if passenger_master_list[i].seat_assignment == assignment:
                passenger_master_list.pop(i)
                break

    # returns a citizen that is the "offspring" of this and the supplied other citizen
    # supplied list must already be a deep copy - will be mutated!
    def reproduce(self, other_citizen, passenger_master_list):
        crossover_list = [None] * len(self.specific_ordering)
        random.shuffle(passenger_master_list)

        # List of tuples of seat arrangments that have been sat - easy way to check for citizen equality/presence due to the deepcopying that has been done,
        # who knows what kind of errors would pop up
        used_seatings = []
        new_citizen = Citizen(self.num_rows, self.num_cols, passenger_master_list)

        # initially tries to assign orderings from parents specifically
        for i in range(int(len(self.specific_ordering))):
            rand_index = random.randint(0, len(self.specific_ordering) - 1)
            try_count = 0
            if i % 2 == 0:
                rand_passenger = self.specific_ordering[rand_index]
                # regenerate random passengers if this passenger (checked by the list of seat assignments added) already part of child
                while (crossover_list[rand_index] != None or rand_passenger.seat_assignment in used_seatings) and try_count < len(passenger_master_list) * 2:
                    rand_index = random.randint(0, len(self.specific_ordering) - 1)
                    rand_passenger = self.specific_ordering[rand_index]
                    try_count += 1

                # just couldn't get one... skip and will let be randomly assigned
                if try_count >= len(passenger_master_list) * 2:
                    continue

                # once a unique has been found, assign a copy to the final list, add its seat assignment to the "seen", remove it from the master list
                # so passengers that aren't added in this way are added in the end

                crossover_list[rand_index] = deepcopy(rand_passenger)
                used_seatings.append(rand_passenger.seat_assignment)
                self.remove_pass_with_assign(passenger_master_list, rand_passenger.seat_assignment)
            else:
                rand_passenger = other_citizen.specific_ordering[rand_index]
                while (crossover_list[rand_index] != None or rand_passenger.seat_assignment in used_seatings) and try_count < len(passenger_master_list) * 2:
                    rand_index = random.randint(0, len(self.specific_ordering) - 1)
                    rand_passenger = other_citizen.specific_ordering[rand_index]
                    try_count += 1

                if try_count >= len(passenger_master_list) * 2:
                    continue

                crossover_list[rand_index] = deepcopy(rand_passenger)
                used_seatings.append(rand_passenger.seat_assignment)
                self.remove_pass_with_assign(passenger_master_list, rand_passenger.seat_assignment)
        
        # whatever is not filled is just randomly assigned
        for index in range(len(crossover_list)):
            if crossover_list[index] == None:
                rand_passenger = random.choice(passenger_master_list)
                self.remove_pass_with_assign(passenger_master_list, rand_passenger.seat_assignment)
                crossover_list[index] = rand_passenger

        new_citizen.update_ordering(crossover_list)
        return new_citizen

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
            result += passenger.visualize()
        
        result += "\nScore:"
        result += str(self.score)
        return result

    # calculates a score for this simulation by running a "seating" multiple times (since seatings can vary due to delays)
    def calc_score(self):
        scores = []

        for i in range(25):
            scores.append(self.airplane.calc_ticks())
            self.airplane = Airplane(self.num_rows, self.num_cols, deepcopy(self.specific_ordering))
        
        self.score = statistics.mean(scores)
        return self.score
    
    # EFFECT: Runs the necessary updates associated with changing the passenger ordering for a specific citizen
    # (Changing airplane, updating score, etc...)
    def update_ordering(self, new_ordering):
        self.specific_ordering = new_ordering
        # initial airplane set up for the first score calculation
        self.airplane = Airplane(self.num_rows, self.num_cols, deepcopy(self.specific_ordering))
        self.calc_score()

# passengers = []

# for row in range(5):
#     for col in range(3):
#         passengers.append(Person(random.uniform(0, 0.25), (row, col)))

# citizen1 = Citizen(5, 3, passengers)
# citizen2 = Citizen(5, 3, passengers)

# print(citizen1)
# print(citizen2)

# child = citizen1.reproduce(citizen2, passengers)

# print(child)
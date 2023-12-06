from airplane import Airplane
from copy import deepcopy
import statistics
import random

# Represents a citizen in the population (one single simulation that has a tick count, specific passenger ordering,
# challenged by other citizens to survive, merge/mutates)
class Citizen():
    # the unique order in which people are sat on airplanes for this citizen
    specific_ordering = []
    # the airplane used to run simulations - reset (rebuild) after running a simulation
    airplane = None
    # number of ticks (takes average) to run previous simulation
    score = 999999
    # dimensions to be used for this citizen (used to rebuild airplanes)
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

            # lower_bound = max(0, first - 5)
            # upper_bound = min(len(self.specific_ordering) - 1, first + 5)
            # second = random.randint(lower_bound, upper_bound)

            second = random.randint(0, len(self.specific_ordering) - 1)

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
    # NOTE: supplied "master list" must already be a deep copy - will be mutated!
    def reproduce(self, other_citizen, passenger_master_list):
        crossover_list = [None] * len(self.specific_ordering)
        random.shuffle(passenger_master_list)

        # List of tuples of seat arrangments that have been sat - used to check for passenger equality/presence in a list
        used_seatings = []

        # Citizen that will be the offspring (list updated at end of method)
        new_citizen = Citizen(self.num_rows, self.num_cols, passenger_master_list)

        # Will make n attempts to draw each of the n passengers using "information" from each passenger
        for i in range(int(len(self.specific_ordering))):
            rand_index = random.randint(0, len(self.specific_ordering) - 1)
            try_count = 0

            # 50/50 chance, pull from parent1 (self)
            if i % 2 == 0:
                # random passenger, will see if we can write this to the list
                rand_passenger = self.specific_ordering[rand_index]
                # BOOLEANS: 1. Prevent overwrites   2. Prevent duplicates   3. Don't try too much (might not be any options!)
                while (crossover_list[rand_index] != None or rand_passenger.seat_assignment in used_seatings) and try_count < len(passenger_master_list) * 2:
                    rand_index = random.randint(0, len(self.specific_ordering) - 1)
                    rand_passenger = self.specific_ordering[rand_index]
                    try_count += 1

                # just couldn't get one... skip and will let be randomly assigned
                if try_count >= len(passenger_master_list) * 2:
                    continue

                # once a unique has been found, assign a copy to the final list, add its seat assignment to the "seen", remove it from the master list
                # so passengers that aren't added with "unique" information can be randomly assigned at the end
                crossover_list[rand_index] = deepcopy(rand_passenger)
                used_seatings.append(rand_passenger.seat_assignment)
                self.remove_pass_with_assign(passenger_master_list, rand_passenger.seat_assignment)
            # 50/50 chance, pull from parent2 (other)
            else:
                # ** same code as above, see comments **
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
    # and takes the avg. of seatings, assigns that number as the "score"
    def calc_score(self):
        scores = []

        for i in range(20):
            scores.append(self.airplane.calc_ticks())
            self.airplane = Airplane(self.num_rows, self.num_cols, deepcopy(self.specific_ordering))
        
        self.score = statistics.mean(scores)
        return self.score
    
    # EFFECT: Runs the necessary updates associated with changing the passenger ordering for a specific citizen
    # (Changing airplane, updating score + running simulation, etc...)
    def update_ordering(self, new_ordering):
        self.specific_ordering = new_ordering
        # initial airplane set up for the first score calculation
        self.airplane = Airplane(self.num_rows, self.num_cols, deepcopy(self.specific_ordering))
        self.calc_score()
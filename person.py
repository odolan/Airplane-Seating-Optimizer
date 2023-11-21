import random

# Represents a passenger on the plane.
class Person:
    delay = None
    # where the passenger will be seated on the airplane
    seat_assignment = None
    # number of ticks that took place before passenger was seated
    seat_time = None
    id = random.randint(100000, 999999) # random 6 digit ID

    # a set of "groups" a passenger belongs to, such as first class, veteran, frequent flier, family w/ young child, etc.
    classes = {}

    # creates a new person with the given delay factor and seat assignment
    def __init__(self, delay, seat_assignment, special_classes):
        self.delay = delay
        self.seat_assignment = seat_assignment
        for category in special_classes:
            self.classes.append(category)

    # checks to see if the person is in their respective seat, given that they are at the provided current location
    def isInSeat(self, current_loc):
        if self.seat_assignment == current_loc:
            return True
        else :              
            return False
    
    # notes this passenger that they arrived at their seat assignment after supplied number of ticks (time)
    def seat_time(self, time):
        self.seat_time = time

    # Returns a string of information about the passenger, including their id and seat assignment
    def __str__(self):
        return str("Passenger " + str(self.id) + " seated at " + str(self.seat_assigment))

    # Method used to visualize a passenger on the airplane (not just generic information about them)
    def visualize(self):
        return str(self.seat_assignment)
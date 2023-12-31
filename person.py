import random

# Represents a passenger on the plane.
class Person:
    # probability between 0 and 1 that, when an action is available for the person to take, they actually take it
    # (old people / families more inclined to miss actions, for example)
    delay_prob = None
    # where the passenger will be seated on the airplane
    # IN THE FORM (row, column)
    seat_assignment = None
    # number of ticks that took place before passenger was seated
    seat_time = None
    id = random.randint(100000, 999999) # random 6 digit ID, unused

    # a set of "groups" a passenger belongs to, such as first class, veteran, frequent flier, family w/ young child, etc.
    classes = {}

    # creates a new person with the given delay factor and seat assignment
    def __init__(self, delay, seat_assignment, special_classes={}):
        self.delay_prob = delay
        self.seat_assignment = seat_assignment
        for category in special_classes:
            self.classes.append(category)

    # checks to see if the person is in their respective seat, given that they are at the provided current location
    def isInSeat(self):
        if self.seat_time is not None:
            return True
        else :              
            return False

    # Returns a string of information about the passenger, including their id and seat assignment
    def __str__(self):
        return "o"

    # Method used to visualize a passenger on the airplane (not just generic information about them)
    def visualize(self):
        result = "("
        result += str(self.seat_assignment[0])
        result += ", "
        result += str(self.seat_assignment[1])
        result += ") - "
        result += str(self.delay_prob)
        return result

    # returns true with probability of 1 - delay_prob, false with probability of delay_prob
    def take_action(self):
        return random.uniform(0, 1) > self.delay_prob

    # seats this passenger in their seat assignment, at current time/tick count
    def seat(self, tick_count):
        self.seat_time = tick_count
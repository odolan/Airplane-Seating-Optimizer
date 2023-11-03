from passenger import Passenger

# represents a seat on an airplane
class Seat:
    holding = None

    def __init__(self):
        self.holding = None

    def set_holding(self, passenger: Passenger):
        self.holding = passenger

    def __str__(self):
        return "Holding " + str(self.passenger)
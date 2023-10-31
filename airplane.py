import numpy as np
import math
from seat import Seat
from walkway import Walkway

# represents an airplane with certain seat layout (dimensions) and a list of passengers to board
class Airplane:
    passengers = []
    rows = 1
    cols = 1
    seats = np.empty( (1, 1) )


    def __init__(self, *args, **kwargs):
        self.passengers = kwargs.get('passengers')
        self.rows = kwargs.get('rows')
        self.cols = kwargs.get('cols')

        # add an extra column as the "walkway" in the middle
        self.seats = np.array( (self.rows, self.cols + 1) )

        for rowIndex in range(self.rows):
            halfway = math.ceil(self.cols / 2)

            for colIndex in range(halfway):
                self.seats[rowIndex][colIndex] = Seat()
            
            # would be good if the walkway would be a linked list
            self.seats[rowIndex][halfway] = Walkway()

            for colIndex in range(halfway + 1, self.cols):

    # this is the function called to run a "tick" of movement of passengers in the walkway
    def run_tick(self):
        pass

    # prints a string representation of the seating chart of the plane
    def __str__(self):
        for row in range(len(self.seats)):
            rowMessage = str(row, " ")
            for col in range(len(self.seats[row])):
                rowMessage.join(str(self.seats[row][col]))

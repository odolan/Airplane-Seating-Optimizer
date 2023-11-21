from aisle import *
from person import Person
from seat import Seat

# represents a configured airplane with one middle aisle and rows/columns of seats on either side, 
# and a list of passengers who will be boarding the plane
class Airplane:

    # Example diagram 

    ##########################
    #        ABOVE ROWS      #
    #   1 2 3 4 5 6 7 8 9 10 #
    # 1 X X X X X X X X X X  # 
    # 2 X X X X X X X X X X  #
    # 3 X X X X X X X X X X  #
# nose  A A A A A A A A A A  END 
    # 4 X X X X X X X X X X  #
    # 5 X X X X X X X X X X  #
    # 6 X X X X X X X X X X  #
    #        BELOW ROWS      #
    ##########################

    # should have length of "columns" parameter, each array inside should be of size "rows"
    above_cols = []
    aisle = None
    below_cols = []

    # builds an airplane with given dimensions and list of passengers
    # (columns = seats per row on each side)
    def __init__(self, rows, columns, passengers):
        self.aisle = Aisle(rows)

        # builds out seats in specified dimensions
        for above_column in range(columns / 2):
            self.above_cols.append([])
            for row in range(rows):
                self.above_cols[above_column].append(Seat())

        for below_column in range(columns / 2):
            self.below_cols.append([])
            for row in range(rows):
                self.below_cols[below_column].append(Seat())

    # Represents this airplane from a "top-down" view. See figure above for an example
    def __str__(self):
        result = ''

        for col in self.above_cols:
            result += str(col)

        result += str(self.aisle)

        for col in self.below_cols:
            result += str(col)
    
        return result
# represents a position node in the aisle linked list
class AisleNode:
    # the node "ahead" of this - closer to the head of the plane
    ahead = None
    # the node "behind" this - closer to the nose of the plane
    behind = None
    # what is "in" this node at the moment, has an underscore as should not be accessed directly by other objects
    _passenger = None
    
    # ** no init function needed **

    # adds a new node to the END of this list - meaning AHEAD of this node, close to the TAIL of the plane
    def add_to_end(self, node):
        if (self.ahead == None):
            node.behind = self
            self.ahead = node
        else:
            self.ahead.add_to_end(node)

    # updates this node to now reference the given person, throws an error if the node already holds a person.
    def add_person_to_node(self, person):
        if self._passenger != None:
            self._passenger = person
        else:
            return ValueError
        
    # represents the current state of this aisle node as a string
    def __str__(self):
        if self._passenger:
            return str(self._passenger)
        else:
            return '_'

    # runs one single tick of movement on this cell, moving passengers forward/to seats as appropriate.
    # given the number of the current "tick" to pass to passengers as appropriate
    def single_tick(self, tick_count):
        # only does something if this node has a passenger
        if self.passenger != None and self.passenger.take_action():
            # Is the passenger currently in their row? --> Make progress towards seating them
            if self.passenger.seat_assignment == self.row:
                self.passenger.seat_time = tick_count # set the time that the passenger sat at 
                self.passenger = None # remove person from aisle
            # If not, make progress towards moving them towards their row (guaranteed to be ahead of them)
            # (Does not check if there is an ahead cell - if the passenger isn't in there current row, there ought to be one ahead of them,
            # if there is not, implies an issue with setup)
            elif not self.ahead.passenger:
                self.ahead.add_person_to_node(self.passenger)
                self.passenger = None

# represents a list of aisle cells for a certain number of rows in an airplane
class Aisle:
    head = None

    # initializes an aisle of given number of rows (nodes) that is at least 1, holds a reference to the first cell
    # (closest to the nose of the airplane - where passengers enter from)
    def __init__(self, rows):
        self.head = AisleNode()

        for i in range(1, rows):
            self.head.add_to_end(AisleNode())

    # represents the current state of this aisle as a string
    def __str__(self):
        output = ''
        current_node = self.head

        while current_node:
            output += str(current_node) + ' -> '
            current_node = current_node.ahead

        # represents the end of the seating area in the airplane
        output += " X"
        return output

    # returns the last node in this aisle
    def get_last_node(self):
        last_node = self.head

        while last_node.behind:
            last_node = last_node.behind
        
        return last_node
    
    # returns true if no passengers are in the aisle
    def empty(self):
        current_node = self.head

        while current_node:
            if current_node.passenger != None:
                return False
            current_node = current_node.ahead
        
        return True
    
    # runs a single tick of movement on the passengers in the aisle.
    # starts from the END of the airplane (closest to the tail) and ends at the BEGINNING of the airplane (closest to the nose)
    # to allow all passengers to move as soon as possible/appropriate
    def run_tick(self):
        tail = self.get_last_node()

        while tail:
            tail.single_tick()
            tail = tail.behind
import copy

rows = 34

# represents a person who is going to board the plane
class Person:
    def __init__(self, delay, seat_assignment, passenger_data):
        self.delay = delay
        self.seat_assignment = seat_assignment
        self.passenger_data = passenger_data

    # checks to see if the person is in their respective seat
    def isInSeat(self, row):
        if self.seat_assignment == row:
            return True
        else :              
            return False
    

# represents a position node in the aisle linked list
class AisleNode:
    ahead = None
    behind = None
    passenger = None
    
    def __init__(self, row):
        self.row = row

    # adds a new node behind the current node in the plane
    def add_to_end(self, node):
        if (self.behind == None):
            self.behind = node
        else:
            self.behind.add_to_end(node)

    def add_person_to_node(self, person):
        self.passenger = person

    # ticks this cell, moving the person it may or may not contain as appropriate
    def single_tick():
        pass
        
    # represents the current state of this aisle as a string
    def __str__(self):
        pass



# represents a list of aisle cells for a certain number of rows in an airplane
class Aisle:
    head = None

    # initializes an aisle of given number of rows (nodes)
    def __init__(self, rows):
        self.head = AisleNode(0)
        
        for i in range(rows - 1):
            self.head.add_to_end(AisleNode(i))

    # initializes one time-unit of movements throughout the aisle. individuals will move as appropriate when possible during the tic
    def onTick():
    
        pass

    # returns the last node in the linked list
    def get_last_node(self):
        last_node = self.head

        while last_node.next:
            last_node = last_node.behind
        
        return last_node
    
    # returns true if no one is in the aisle 
    def empty(self):
        current_node = self.head

        while current_node:
            if current_node.passenger != None:
                return False
            current_node = current_node.behind
        
        return True



def simulate_seating(_passengers):
    passengers = copy.deepcopy(_passengers) # make a copy we can mutate

    all_passengers_seated = False

    aisle = Aisle(rows)

    # FOR NOW, just count number of ticks needed to seat the plane in full
    tickCount = 0

    # continue to seat passengers until everyone is in their seats
    while not all_passengers_seated and not aisle.empty():
        current_row = aisle.get_last_node()

        # one tic is going through the aisle and making appropriates updates to passenger positions 
        while current_row:

            # check to see if this aisle position has a passenger
            if current_row.passenger != None:

                # check if we can seat this passenger in the current row 
                if current_row.passenger.seat_assignment == current_row.row:
                    # this is where we need to pause the simulation for the number of ticks 

                    current_row.passenger = None # remove person from aisle
                else:
                    # if we can move this person forward, move them forward and remove them from the current aisle position
                    if current_row.behind and current_row.behind.passenger == None:
                        current_row.behind.passenger = current_row.passenger
                        current_row.passenger = None
                
                # if we are looking at the first aisle position and its empty, 
            current_row = current_row.ahead

        tickCount += 1

        # add the next person to the aisle if no one is in the first aisle position
        # if aisle.head.passenger == None:
        #     if len(passengers) > 0:
        #         pass
        #     else:
        #         all_passengers_seated

        
    return tickCount

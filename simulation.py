import copy


## ** A WORK IN PROGRESS ** ##

# runs a full simulation of seating the given list of passengers, seating them in the order in which they were supplied to the function
def simulate_seating(passengers):
    passengers = copy.deepcopy(passengers) # make a copy we can mutate

    all_passengers_seated = False

    # runs a simulation/builds aisle using number of rows needed based on list of passengers' seat assignments
    numRowsNeeded = getMaxRow(passengers)
    aisle = Aisle(numRowsNeeded)

    # FOR NOW, just count number of ticks needed to seat the plane in full
    tickCount = 0

    # continue to seat passengers until everyone is in their seats
    while not all_passengers_seated:
        current_row = aisle.get_last_node()

        print(aisle)
        print()

        # one tic is going through the aisle and making appropriates updates to passenger positions 
        while current_row:

            # # check to see if this aisle position has a passenger
            # if current_row.passenger != None:

            #     # check if we can seat this passenger in the current row 
            #     if current_row.passenger.seat_assignment == current_row.row:

            #         # this is where we need to pause this persons ability to enter the row to create slow downs
            #         if current_row.passenger.delay == 0:
            #             current_row.passenger.seat_time(tickCount) # set the time that the passenger sat at 
            #             current_row.passenger = None # remove person from aisle
            #         else:
            #             current_row.passenger.delay -= 1
            #     else:
            #         # if we can move this person forward, move them forward and remove them from the current aisle position
            #         if current_row.behind and current_row.behind.passenger == None:
            #             current_row.behind.passenger = current_row.passenger
            #             current_row.passenger = None
                
            # if we are looking at the first node in the aisle (first aisle position) add in a new passenger to the linked list
            if current_row.row == 0: 
                # if there are no more passengers to add 
                if len(passengers) < 1:
                    return tickCount

                # add passenger to aisle linked list
                if current_row.passenger == None:
                    current_row.passenger = passengers.pop(0)

            current_row = current_row.ahead

        tickCount += 1

    return tickCount

# # # Person (delay, row)
# # p1 = Person(3, 0)
# # p2 = Person(3, 3)
# # p3 = Person(3, 4)
# # p4 = Person(3, 1)
# # p5 = Person(3, 1)

# # passengers = [p1, p2, p3, p4, p5]

# randPassengers = []

# for i in range(90):
#     randPassengers.append(Person(random.randint(0, 8), int(i / 3)))

# random.shuffle(randPassengers)

# # print(getMaxRow(passengers))
# # print(simulate_seating(passengers))
# print(simulate_seating(randPassengers))
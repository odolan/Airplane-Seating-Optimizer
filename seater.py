from passenger import Passenger
from collections import deque

# seats = [[] * 38]
seats = [[] * 5]

"""
Example seat layout with row and aisle

(0,0)(0,1)  (0,2)(0,3)(0,4)
(1,0)(1,1)  (1,2)(1,3)(1,4)
(2,0)(2,1)  (2,2)(2,3)(2,4)
(3,0)(3,1)  (3,2)(3,3)(3,4)
(4,0)(4,1)  (4,2)(4,3)(4,4)

"""

p1 = Passenger(seat=(0,0), speed=5)
p2 = Passenger(seat=(0,1), speed=5)
p3 = Passenger(seat=(0,2), speed=5)
p4 = Passenger(seat=(0,3), speed=5)
p5 = Passenger(seat=(0,4), speed=5)

p6 = Passenger(seat=(1,0), speed=5)
p7 = Passenger(seat=(1,1), speed=5)
p8 = Passenger(seat=(1,2), speed=5)
p9 = Passenger(seat=(1,3), speed=5)
p10 = Passenger(seat=(1,4), speed=5)

p11 = Passenger(seat=(2,0), speed=5)
p12 = Passenger(seat=(2,1), speed=5)
p13 = Passenger(seat=(2,2), speed=5)
p14 = Passenger(seat=(2,3), speed=5)
p15 = Passenger(seat=(2,4), speed=5)

p16 = Passenger(seat=(3,0), speed=5)
p17 = Passenger(seat=(3,1), speed=5)
p18 = Passenger(seat=(3,2), speed=5)
p19 = Passenger(seat=(3,3), speed=5)
p20 = Passenger(seat=(3,4), speed=5)

p21 = Passenger(seat=(4,0), speed=5)
p22 = Passenger(seat=(4,1), speed=5)
p23 = Passenger(seat=(4,2), speed=5)
p24 = Passenger(seat=(4,3), speed=5)
p25 = Passenger(seat=(4,4), speed=5)

passengers = [
    p1, p2, p3, p4, p5, 
    p6, p7, p8, p9, p10, 
    p11, p12, p13, p14, p15, 
    p16, p17, p18, p19, p20, 
    p21, p22, p23, p24, p25
    ]

# given an indivudals seat and speed, and seating arrangement
# returns the time it takes the individual to travel straight to their seat
def time_to_seat(seat, speed, seating_arrangement):
    pass

# takes a list of people with seating arrangement
def seater(passengers): 
    # Initialize a queue to represent the order of passengers waiting in the aisle
    boarding_queue = deque(passengers)
    
    # Initialize a dictionary to store the position of each passenger
    position = {passenger: 0 for passenger in passengers}
    
    time = 0  # Initialize the time counter

    while boarding_queue:
        current_passenger = boarding_queue.popleft()  # Get the next passenger in the aisle
        seat_position = passengers.index(current_passenger)
        
        # Calculate the time it takes for the passenger to reach their seat
        time_to_seat = abs(seat_position - position[current_passenger])
        
        # Update the passenger's position
        position[current_passenger] = seat_position
        
        # Increment the total time
        time += time_to_seat
        
        # Print the boarding process for visualization
        print(f"Time {time}: {current_passenger} is seated at position {seat_position}")
    
    print(f"Total boarding time: {time} minutes")

time_to_seat = seater(passengers)
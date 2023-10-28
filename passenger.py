
class Passenger:
    speed = 0
    happiness = 100
    first_class = False
    seat = (0, 0)

    def __init__(self, *args, **kwargs):
        self.seat= kwargs.get('seat')
        self.speed = kwargs.get('speed')
        self.happiness = kwargs.get('happiness')
        self.first_class = kwargs.get('first_class', False)

    def __str__(self):
        return "Seat: {0}\nSpeed: {1}\nHappiness: {2}\nFirst Class: {3} ".format(self.seat, self.speed, self.happiness, self.first_class)



# test person 

# owen = Passenger(seat=(), speed=5, happiness=50, first_class=False)
import pygame
from genetic import genetic
import random
import time
# import citizen

class Passenger:
    def __init__(self, position, seat_assignment, color, delay):
        self.position = position
        self.seat_assignment = seat_assignment
        self.color = color
        self.step_size = 10.0  # Movement step size
        self.is_seated = False  # Flag to check if passenger is seated
        self.delay = delay

    def update_position(self):
        # Stop moving if already seated
        if self.is_seated:
            return

        # First, move to the correct row (y-coordinate)
        if self.position[0] < self.seat_assignment[0]:
            if random.uniform(0,1) > self.delay:
                self.position[0] += self.step_size

        # Check if passenger has reached their seat
        if self.position[0] >= self.seat_assignment[0]:
            self.is_seated = True
            self.position = self.seat_assignment  # Snap to the exact seat position

    def can_move(self, passenger_ahead):
        threshold_distance = 25

        # Check both X and Y coordinates
        
        return self.position[0] + threshold_distance < passenger_ahead.position[0] or self.position[1] != passenger_ahead.position[1]

def update_passenger_positions(people):
    for i in range(len(people) - 1, -1, -1):  # Start from the last passenger
        if i == 0 or people[i].can_move(people[i - 1]):
            people[i].update_position()
                

initial, final = genetic(75, 18, 3, 100, 8, 20)
# best_citizen = min(final_population, key=lambda citizen: citizen.score)  # Assuming lower score is better
# optimized_boarding_sequence = best_citizen.specific_ordering



def assign_colors(num_people):
    colors = []
    # Blue to red gradient
    start_rgb = (0, 0, 255)  # Blue
    end_rgb = (255, 0, 0)    # Red

    # Calculate the difference in each color channel
    diff_rgb = [end - start for start, end in zip(start_rgb, end_rgb)]

    for i in range(num_people):
        # Calculate the proportion of the gradient
        proportion = i / (num_people - 1)

        # Calculate the color
        color = tuple(int(start + diff * proportion) for start, diff in zip(start_rgb, diff_rgb))
        colors.append(color)

    return colors





seat_color_mapping = assign_colors(120)
print(seat_color_mapping)



def make_passenger(line):
    people = []
    aisle_width = 55  # Increased width of the aisle for a larger aisle
    seat_width = 26  # Width of each seat (adjust as needed)
    start_x = 250     # Starting X position for seats
    start_y = 250     # Starting Y position for seats
    aisle_center = start_x + aisle_width / 2  # Center line of the aisle

    
    for i, person in enumerate(line.specific_ordering):
        
        if person.seat_assignment is not None:
            
            if person.seat_assignment[1] in [0, 1, 2]:  # Left side of the aisle
                seat_y = (aisle_center - (seat_width * (person.seat_assignment[1] + 1)))
            else:  # Right side of the aisle
                seat_y = (aisle_center + (seat_width * (person.seat_assignment[1] - 2)))

            seat_x = (start_x) * person.seat_assignment[0] / 10
            
            seat_pos = (150 + seat_x, 40 + seat_y)
            
            
            passenger_color = seat_color_mapping[i]
            people.append(Passenger([10, 315], seat_pos, passenger_color, person.delay_prob))  # Use seat position
        
    return people

            



def draw_people(screen, people):
    for person in people:
        pygame.draw.circle(screen, person.color, (int(person.position[0]), int(person.position[1])), 8)





def run(order):
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Airplane Simulator")

    done = False

    font = pygame.font.Font(None, 36)  # You can choose another font and size

    done = False
    start_time = time.time()  # Record the start time

    
    image = pygame.image.load('Screenshot 2023-11-30 at 11.40.05 AM.png')
    image = pygame.transform.scale(image, (455, 300))  # Replace with desired size
    
    animation_started = False
    clock = pygame.time.Clock()
    fps = 30
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    animation_started = True
                    start_time = time.time()  # Record the start time when spacebar is pressed

        screen.fill("white")

        if animation_started:
            update_passenger_positions(order)  # Update positions each frame
            screen.blit(image, (125, 170))  # Replace (50, 50) with desired position
            draw_people(screen, order)


            # Calculate and render the time
            current_time = time.time() - start_time
            time_text = f'Time: {current_time:.2f}s'  # Format the time to a string
            time_surface = font.render(time_text, True, (0, 0, 0))  # Black color
            screen.blit(time_surface, (10, 10))  # Position of the text

            
            pygame.display.flip()
            clock.tick(fps)

    

run(make_passenger(initial))
run(make_passenger(final))
# Libraries
import pygame
import sys
import random
import math
import time

# Initialize Pygame
pygame.init()

# Constants
GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT = 1000, 700
DATA_WINDOW_WIDTH, DATA_WINDOW_HEIGHT = 800, 600
POINT_RADIUS = 5
FPS = 60

# Colors
POINT_ONE_COLOR = (255, 0, 0)
POINT_TWO_COLOR = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Font Style
font = pygame.font.SysFont(None, 30)

# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Function to check if two points are clicked within a certain radius
def is_clicked(pos, target):
    return distance(pos, target) < POINT_RADIUS

# Function to draw the line between two points
def draw_line(screen, start, end):
    pygame.draw.line(screen, WHITE, start, end, 2)

# Show Message Dialog
def show_dialog(message, screen):
    # Font
    font = pygame.font.Font(None, 36)
    dialog_box = pygame.Rect(100, 200, 600, 200)
    pygame.draw.rect(screen, WHITE, dialog_box)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=dialog_box.center)
    screen.blit(text, text_rect)
    pygame.display.flip()

# Function to generate 2n non-collinear points
def generate_non_collinear_points(num_points, width, height):
    points = []
    points1 = []
    points2 = []
    switch = 0
    while len(points) < 2*num_points:
        # Generate a random point
        x = random.randint(POINT_RADIUS, width-POINT_RADIUS)
        y = random.randint(POINT_RADIUS, height-POINT_RADIUS)
        # Check if the new point is collinear with any existing pair of points
        is_collinear = False
        for i in range(len(points) - 1):
            for j in range(i + 1, len(points)):
                p1, p2 = points[i], points[j]
                # Efficient check for collinearity (avoiding floating-point errors)
                if (p2[0] - p1[0]) * (y - p1[1]) == (p2[1] - p1[1]) * (x - p1[0]):
                    is_collinear = True
                    break
        if not is_collinear:
            points.append((x, y))
            if switch % 2 ==0:
                points1.append((x, y))
            else:
                points2.append((x, y))
            switch+=1
    return points1, points2

# Start Game
def start_game(screen, n):

    clock = pygame.time.Clock()

    # Generate random points
    points1, points2 = generate_non_collinear_points(n, GAME_WINDOW_WIDTH-100, GAME_WINDOW_HEIGHT-100)

    # Main game loop
    points = points1 + points2
    selected_points = []
    closed_points = []
    number_of_lines = 0
    running = True

    # Draw points
    for point1 in points1:
        pygame.draw.circle(screen, POINT_ONE_COLOR, point1, POINT_RADIUS)

    for point2 in points2:
        pygame.draw.circle(screen, POINT_TWO_COLOR, point2, POINT_RADIUS)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if a point is clicked
                for point in points:
                    if is_clicked(event.pos, point) and len(selected_points) < 2:
                        if point not in closed_points:
                            if not selected_points:
                                selected_points.append(point)
                            else:
                                if selected_points[0] in points1 and point in points2:
                                    selected_points.append(point)
                                elif selected_points[0] in points2 and point in points1:
                                    selected_points.append(point)

        # Draw line between selected points
        if len(selected_points) == 2:
            draw_line(screen, selected_points[0], selected_points[1])
            closed_points.extend(selected_points)
            selected_points.clear()
            number_of_lines+=1

        # Update display
        pygame.display.flip()
        pygame.display.update()

        # Cap the frame rate
        clock.tick(FPS)

        if number_of_lines==n:
            time.sleep(5)
            screen = create_screen(DATA_WINDOW_WIDTH, DATA_WINDOW_HEIGHT, "Completed")
            game_finished_screen(screen)
    
    pygame.quit()
    sys.exit()

# Draw Text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Draw Input Box
def draw_input_box(screen):
    pygame.draw.rect(screen, WHITE, (200, 200, 400, 50))
    pygame.draw.rect(screen, BLACK, (200, 200, 400, 50), 2)

# Draw Buttons
def draw_buttons(screen):
    start_button = pygame.Rect(200, 300, 150, 50)
    pygame.draw.rect(screen, POINT_TWO_COLOR, start_button)
    draw_text("Start", font, WHITE, screen, start_button.centerx, start_button.centery)

    quit_button = pygame.Rect(450, 300, 150, 50)
    pygame.draw.rect(screen, POINT_ONE_COLOR, quit_button)
    draw_text("Quit", font, WHITE, screen, quit_button.centerx, quit_button.centery)

    return start_button, quit_button

# Game Completed Dialog
def game_finished_screen(screen):
    screen.fill(GRAY)
    draw_text("Congratulations!", font, BLACK, screen, DATA_WINDOW_WIDTH // 2, DATA_WINDOW_HEIGHT // 2 - 100)
    draw_text("You've Finished the Game!", font, BLACK, screen, DATA_WINDOW_WIDTH // 2, DATA_WINDOW_HEIGHT // 2 - 50)
    quit_button = pygame.Rect(320, 300, 150, 50)
    pygame.draw.rect(screen, (2,75,48), quit_button)
    draw_text("Exit", font, WHITE, screen, quit_button.centerx, quit_button.centery)
    while True:
        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

# Get Number of Points from the user
def get_input(screen):
    
    input_text = ''
    screen.fill(GRAY)

    # Draw game name
    draw_text("Point Connect", pygame.font.SysFont(None, 40), BLACK, screen, DATA_WINDOW_WIDTH // 2, 50)
    draw_text("Enter Number of Points", pygame.font.SysFont(None, 30), BLACK, screen, DATA_WINDOW_WIDTH // 2, 175)

    # Draw Buttons
    start_button, quit_button = draw_buttons(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return int(input_text)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        draw_input_box(screen)
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(text_surface, (DATA_WINDOW_WIDTH // 2, 215))
        pygame.display.flip()

# Create a new screen
def create_screen(width, height, message):
    # Set up the display
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(message)
    return screen

# Main function
def main():
    # Set up the display
    screen = create_screen(DATA_WINDOW_WIDTH, DATA_WINDOW_HEIGHT, "Setup game")

    # Get User Input
    NUMBER_OF_POINTS = get_input(screen)

    # Start Game
    screen = create_screen(GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT, "Connect the points")
    screen.fill(BLACK)
    start_game(screen, NUMBER_OF_POINTS)

if __name__ == "__main__":
    main()
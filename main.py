import pygame
import math
import random
import time
import sys
import asyncio

# CONSTANTS
WIDTH = 640  # Screen width in pixels
HEIGHT = 640  # Screen height in pixels
PIXELS = 32  # Size of each square in the grid
SQUARES = int(WIDTH / PIXELS)  # Number of squares per row/column

# COLORS
BG1 = (156, 210, 54)  # Light green for background
BG2 = (147, 203, 57)  # Slightly darker green for background grid
RED = (255, 0, 0)  # Red color for apple
BLUE = (0, 0, 50)  # Blue color for snake
BLACK = (0, 0, 0)  # Black color for score text

class Snake:
    # Represents the player-controlled snake.

    def __init__(self):
        self.color = BLUE  # Snake's head color
        # Randomly position the snake's head within the grid
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.state = 'STOP'  # Initial direction (STOP means no movement)
        self.bodies = []  # List to store snake's body segments
        self.body_color = 50  # Starting color intensity for body segments

    def move_head(self):
        # Moves the snake's head based on its current state.
        if self.state == "UP":
            self.headY -= PIXELS
        elif self.state == "DOWN":
            self.headY += PIXELS
        elif self.state == "RIGHT":
            self.headX += PIXELS
        elif self.state == "LEFT":
            self.headX -= PIXELS

    def move_body(self):
        # Updates the positions of the snake's body segments.
        if len(self.bodies) > 0:
            # Iterate from the last body segment to the first
            for i in range(len(self.bodies) - 1, -1, -1):
                if i == 0:
                    # Move the first body segment to the previous head position
                    self.bodies[0].posX = self.headX
                    self.bodies[0].posY = self.headY
                else:
                    # Move the current segment to the previous segment's position
                    self.bodies[i].posX = self.bodies[i - 1].posX
                    self.bodies[i].posY = self.bodies[i - 1].posY

    def add_body(self):
        # Adds a new body segment to the snake.
        self.body_color += 10  # Increment body color intensity
        body = Body((0, 0, self.body_color), self.headX, self.headY)
        self.bodies.append(body)

    def draw(self, surface):
        # Draws the snake's head and body segments on the screen.
        pygame.draw.rect(surface, self.color, (self.headX, self.headY, PIXELS, PIXELS))
        for body in self.bodies:
            body.draw(surface)

    def die(self):
        # Resets the snake's position and state after it dies.
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []  # Clear body segments
        self.body_color = 50  # Reset body color intensity
        self.state = 'STOP'  # Stop movement

class Body:
    # Represents a segment of the snake's body.

    def __init__(self, color, posX, posY):
        self.color = color
        self.posX = posX
        self.posY = posY

    def draw(self, surface):
        # Draws the body segment on the screen.
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))

class Apple:
    # Represents the apple that the snake eats.

    def __init__(self):
        self.color = RED  # Color of the apple
        self.spawn()  # Randomly position the apple on the grid

    def spawn(self):
        # Randomly positions the apple within the grid.
        self.posX = random.randrange(0, WIDTH, PIXELS)
        self.posY = random.randrange(0, HEIGHT, PIXELS)

    def draw(self, surface):
        # Draws the apple on the screen.
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))

class Background:
    # Draws the grid-based background.

    def draw(self, surface):
        # Fills the screen with a checkerboard pattern.
        surface.fill(BG1)  # Fill the screen with the primary background color
        counter = 0  # Tracks the alternation between BG1 and BG2
        for row in range(SQUARES):
            for col in range(SQUARES):
                if counter % 2 == 0:
                    pygame.draw.rect(surface, BG2, (col * PIXELS, row * PIXELS, PIXELS, PIXELS))
                if col != SQUARES - 1:
                    counter += 1

class Collision:
    # Handles collision detection for the game.

    def between_snake_and_apple(self, snake, apple):
        # Checks if the snake's head overlaps the apple.
        distance = math.sqrt((snake.headX - apple.posX) ** 2 + (snake.headY - apple.posY) ** 2)
        return distance < PIXELS

    def between_snake_and_walls(self, snake):
        # Checks if the snake collides with the screen boundaries.
        return snake.headX < 0 or snake.headX >= WIDTH or snake.headY < 0 or snake.headY >= HEIGHT

    def between_head_and_body(self, snake):
        # Checks if the snake's head collides with its own body.
        for body in snake.bodies:
            distance = math.sqrt((snake.headX - body.posX) ** 2 + (snake.headY - body.posY) ** 2)
            if distance < PIXELS:
                return True
        return False

class Score:
    # Manages the player's score.

    def __init__(self):
        self.points = 0  # Starting score
        self.font = pygame.font.SysFont('monospace', 30, bold=False)  # Font for displaying the score

    def increase(self):
        # Increases the score by 1.
        self.points += 1

    def reset(self):
        # Resets the score to 0.
        self.points = 0

    def show(self, surface):
        # Displays the current score on the screen.
        label = self.font.render(f'Score: {self.points}', 1, BLACK)
        surface.blit(label, (5, 5))

async def main():
    # Main game loop.
    pygame.init()  # Initialize Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
    pygame.display.set_caption("SNAKE")  # Set window title

    # Create game objects
    snake = Snake()
    apple = Apple()
    background = Background()
    collision = Collision()
    score = Score()

    while True:  # Game loop
        # Draw all objects on the screen
        background.draw(screen)
        apple.draw(screen)
        snake.draw(screen)
        score.show(screen)

        # Handle events (e.g., key presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.state != "DOWN":
                    snake.state = "UP"
                elif event.key == pygame.K_DOWN and snake.state != "UP":
                    snake.state = "DOWN"
                elif event.key == pygame.K_RIGHT and snake.state != "LEFT":
                    snake.state = "RIGHT"
                elif event.key == pygame.K_LEFT and snake.state != "RIGHT":
                    snake.state = "LEFT"
                elif event.key == pygame.K_p:
                    snake.state = "STOP"

        # Check collisions and update game state
        if collision.between_snake_and_apple(snake, apple):
            apple.spawn()
            snake.add_body()
            score.increase()

        if snake.state != "STOP":
            snake.move_body()
            snake.move_head()

        if collision.between_snake_and_walls(snake) or collision.between_head_and_body(snake):
            snake.die()
            apple.spawn()
            score.reset()

        pygame.time.delay(110)  # Control game speed
        pygame.display.update()  # Refresh the screen

        # Pause for web hosting purposes
        await asyncio.sleep(0)

# Run the game loop asynchronously
asyncio.run(main())

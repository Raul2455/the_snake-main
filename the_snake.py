# pylint: disable=no-member

"""Модуль описывает простую игру 'Змейка' на основе библиотеки Pygame."""

import random
import sys
import pygame

# Initialize the pygame library
pygame.init()

# Set the dimensions of the grid and screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Define color constants
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK

# Define movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Define initial values for the snake
INITIAL_LENGTH = 1
INITIAL_SCORE = 0

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Изгиб питона")
clock = pygame.time.Clock()


class GameObject:
    """A base class for objects that appear on the game board."""

    def __init__(self, position=(0, 0), body_color=WHITE):
        """Initialize the game object with a given position and color."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Draw the game object on the given surface."""
        r = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, r)


class Snake(GameObject):
    """A class representing the snake in the game."""

    def __init__(self):
        """Initialize the snake with default values."""
        super().__init__()
        self.body_color = GREEN
        self.length = INITIAL_LENGTH
        self.positions = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        ]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = INITIAL_SCORE

    def draw(self, surface):
        """Draw the entire snake on the given surface."""
        for pos in self.positions:
            r = pygame.Rect(
                (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, r)

    def move(self):
        """Move the snake in the current direction."""
        cur = self.positions[0]
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Reset the snake to the default state."""
        self.length = INITIAL_LENGTH
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = INITIAL_SCORE

    def update_direction(self, new_direction):
        """Update the snake's direction to the new direction."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def get_head_position(self):
        """Get the position of the snake's head."""
        return self.positions[0]

    def handle_apple_collision(self, apple_position):
        """Handle collision with an apple, growing the snake if necessary."""
        if self.get_head_position() == apple_position:
            self.length += 1
            self.score += 1
            return True
        return False


class Apple(GameObject):
    """A class representing the apple in the game."""

    def __init__(self):
        """Initialize the apple with a random position."""
        super().__init__(position=self.randomize_position(), body_color=RED)

    def randomize_position(self):
        """Randomize the position of the apple."""
        return (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )


def handle_keys():
    """Handle key events and return a new direction if necessary."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return UP
            elif event.key == pygame.K_DOWN:
                return DOWN
            elif event.key == pygame.K_LEFT:
                return LEFT
            elif event.key == pygame.K_RIGHT:
                return RIGHT
    return None


def draw_objects(surface, snake, apple):
    """Draw all game objects on the given surface."""
    surface.fill(BOARD_BACKGROUND_COLOR)
    snake.draw(surface)
    apple.draw(surface)
    score_text = f"Score: {snake.score}"
    text_surface = pygame.font.SysFont("Arial", 36).render(
        score_text, True, WHITE
    )
    surface.blit(text_surface, (5, 5))
    pygame.display.update()


def main():
    """The main game loop."""
    snake = Snake()
    apple = Apple()

    while True:
        direction = handle_keys()
        if direction:
            snake.update_direction(direction)
            snake.move()
        if snake.handle_apple_collision(apple.position):
            apple.position = apple.randomize_position()

        draw_objects(screen, snake, apple)
        clock.tick(10)


if __name__ == "__main__":
    main()

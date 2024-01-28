# pylint: disable=no-member

import random
import sys
import pygame

# Инициализация Pygame
pygame.init()

# Константы размеров экрана и сетки
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Начальные параметры змейки
INITIAL_LENGTH = 1
INITIAL_SCORE = 0

# Настройка окна игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Изгиб питона")
clock = pygame.time.Clock()


class GameObject:
    """Класс для представления игрового объекта."""

    def __init__(self, position=(0, 0), body_color=WHITE):
        """Инициализация игрового объекта с позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта на игровом поле."""
        r = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, r)


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(self):
        """Инициализация змейки с начальными параметрами."""
        super().__init__()
        self.body_color = GREEN
        self.length = INITIAL_LENGTH
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = INITIAL_SCORE

    def draw(self, surface):
        """Отрисовка змейки на игровом поле."""
        for pos in self.positions:
            r = pygame.Rect(
                (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, r)

    def move(self):
        """Перемещение змейки в текущем направлении."""
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
        """Сброс змейки к начальным параметрам."""
        self.length = INITIAL_LENGTH
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = INITIAL_SCORE

    def update_direction(self, new_direction):
        """Обновление направления движения змейки."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def get_head_position(self):
        """Получить позицию головы змейки."""
        return self.positions[0]


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self):
        """Инициализация яблока в случайной позиции."""
        super().__init__(position=self.randomize_position(), body_color=RED)

    def randomize_position(self):
        """Получение случайной позиции для яблока."""
        return (random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1))


def handle_keys():
    """Обработка нажатий клавиш для управления змейкой."""
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
    """Отрисовка объектов на игровом поле и обновление экрана."""
    surface.fill(BLACK)
    snake.draw(surface)
    apple.draw(surface)
    score_text = f"Score: {snake.score}"
    text_surface = pygame.font.SysFont(
        "Arial", 36).render(score_text, True, WHITE)
    surface.blit(text_surface, (5, 5))
    pygame.display.update()


def main():
    """Главная функция игры."""
    snake = Snake()
    apple = Apple()

    while True:
        direction = handle_keys()
        if direction:
            snake.update_direction(direction)

        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.score += 1
            apple.position = apple.randomize_position()

        draw_objects(screen, snake, apple)
        clock.tick(10)


if __name__ == "__main__":
    main()

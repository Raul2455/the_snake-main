# pylint: disable=no-member

"""Модуль описывает простую игру 'Змейка' на основе библиотеки Pygame."""

import sys
import random
import pygame

# Инициализация pygame
pygame.init()

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Начальные значения
INITIAL_LENGTH = 5
INITIAL_SCORE = 0

# Настройка экрана и часов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Скорость игры
GAME_SPEED = 10


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """Инициализация игрового объекта."""
        self.position = position if position is not None else CENTER_POSITION
        self.body_color = body_color if body_color is not None else WHITE

    def draw_cell(self, surface, position=None, color=None):
        """Отрисовка ячейки."""
        position = position if position is not None else self.position
        color = color if color is not None else self.body_color
        rect = pygame.Rect(
            (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, color, rect)

    def draw(self, surface):
        """Отрисовка объекта. Должен быть переопределен в подклассах."""
        raise NotImplementedError(
            "Этот метод должен быть переопределен производными классами."
        )


class Snake(GameObject):
    """Класс змеи в игре 'Змейка'."""

    def __init__(self, position=None, body_color=GREEN):
        """Инициализация змеи."""
        super().__init__(position, body_color)
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.reset()

    def draw(self, surface):
        """Отрисовка змеи."""
        for pos in self.positions:
            self.draw_cell(surface, pos)

    def move(self):
        """Движение змеи."""
        head_position = self.get_head_position()
        x, y = self.direction
        new_head_position = (
            (head_position[0] + x) % GRID_WIDTH,
            (head_position[1] + y) % GRID_HEIGHT
        )
        if new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Сброс змеи к начальному состоянию."""
        self.length = INITIAL_LENGTH
        self.positions = [CENTER_POSITION]
        self.score = INITIAL_SCORE

    def update_direction(self, new_direction):
        """Обновление направления движения змеи."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def get_head_position(self):
        """Получение позиции головы змеи."""
        return self.positions[0]

    def handle_apple_collision(self, apple_position):
        """Обработка столкновения с яблоком."""
        if self.get_head_position() == apple_position:
            self.length += 1
            self.score += 1
            return True
        return False


class Apple(GameObject):
    """Класс яблока в игре 'Змейка'."""

    def __init__(self, position=None, body_color=RED):
        # Инициализация яблока с случайной позицией
        super().__init__(
            position=self.randomize_position(),
            body_color=body_color
        )

    def draw(self, surface):
        """Отрисовка яблока."""
        self.draw_cell(surface)

    def randomize_position(self):
        """Получение случайной позиции для яблока."""
        return (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )


def handle_keys():
    """Обработка нажатий клавиш."""
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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def draw_objects(surface, snake, apple):
    """Отрисовка всех объектов на поверхности."""
    surface.fill(BOARD_BACKGROUND_COLOR)
    snake.draw(surface)
    apple.draw(surface)
    score_text = f"Score: {snake.score}"
    font = pygame.font.SysFont("Arial", 36)
    text_surface = font.render(score_text, True, WHITE)
    surface.blit(text_surface, (5, 5))
    pygame.display.update()


def main():
    """Основной цикл игры."""
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
        clock.tick(GAME_SPEED)


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        sys.exit()

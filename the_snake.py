"""Игра 'Изгиб питона' на основе pygame."""

import random
import sys
import pygame

# Инициализация pygame
pygame.init()

# Константы для настройки окна и игровой сетки
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

# Цвет фона
BOARD_BACKGROUND_COLOR = BLACK

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Изгиб питона")
clock = pygame.time.Clock()


class GameObject:
    """Класс базового игрового объекта."""

    def __init__(self, position=(0, 0), body_color=WHITE):
        """Инициализирует объект с позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на переданной поверхности."""
        r = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, r)


class Snake(GameObject):
    """Класс змеи в игре."""

    def __init__(self):
        """Инициализирует змею в начальной позиции."""
        super().__init__(
            position=(
                GRID_WIDTH // 2,
                GRID_HEIGHT // 2
            ),
            body_color=GREEN
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def move(self):
        """Перемещает змею в текущем направлении и обрабатывает столкновения."""
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0] + x) % GRID_WIDTH), ((cur[1] + y) % GRID_HEIGHT))
        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Сбрасывает змею в начальное состояние."""
        self.length = 1
        self.positions = [(
            GRID_WIDTH // 2, GRID_HEIGHT // 2
        )]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def update_direction(self, new_direction):
        """Обновляет направление движения змеи, если новое направление не противоположно текущему."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]


class Apple(GameObject):
    """Класс яблока в игре."""

    def __init__(self):
        """Инициализирует яблоко в случайной позиции."""
        super().__init__(position=self.randomize_position(), body_color=RED)

    def randomize_position(self):
        """Возвращает случайную позицию для яблока на сетке."""
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))


def handle_keys():
    """Обрабатывает нажатия клавиш и возвращает новое направление движения."""
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


def draw_objects(snake, apple):
    """Отрисовывает все игровые объекты и обновляет экран."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    draw_score(snake.score)
    for position in snake.positions:
        snake.body_color = GREEN
        snake.position = position
        snake.draw(screen)
    apple.draw(screen)
    pygame.display.update()


def draw_score(score):
    """Отрисовывает счёт игры."""
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (5, 5))


def main():
    """Главная функция, в которой происходит игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(10)
        new_direction = handle_keys()
        if new_direction:
            snake.update_direction(new_direction)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.score += 1
            apple.position = apple.randomize_position()
        draw_objects(snake, apple)


if __name__ == "__main__":
    main()
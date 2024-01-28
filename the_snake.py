# Простая игра в змейку, созданная с помощью Pygame.
# pylint: disable=no-member

import random
import sys
import pygame

# Ошибки, связанные с Pygame, игнорируются для Pylint
# pylint: disable=no-member

# Инициализация Pygame
pygame.init()

# Размер дисплея, размер сетки и определения цвета
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Определения цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Определения направлений
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константы для начальных условий
INITIAL_LENGTH = 1
INITIAL_SCORE = 0

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Изгиб питона")
clock = pygame.time.Clock()


class GameObject:
    """Класс для общих игровых объектов."""

    def __init__(self, position=(0, 0), body_color=WHITE):
        """Инициализация игрового объекта с указанием положения и цвета."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта на игровой поверхности."""
        r = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, r)


class Snake(GameObject):
    """Класс, представляющий змею в игре."""

    def __init__(self):
        """Инициализация змейки значениям по умолчанию."""
        super().__init__()
        self.body_color = GREEN
        self.length = INITIAL_LENGTH
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = INITIAL_SCORE

    def draw(self, surface):
        """Отрисовка змейки на игровой поверхности."""
        for pos in self.positions:
            r = pygame.Rect(
                (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, r)

    def move(self):
        """Перемещает змейку в текущем направлении."""
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
        """Возвращает змейку в состояние по умолчанию."""
        self.length = INITIAL_LENGTH
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = INITIAL_SCORE

    def update_direction(self, new_direction):
        """Изменяет направление движения змеи."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def get_head_position(self):
        """Определение положения головы змеи."""
        return self.positions[0]


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализирует яблоко вызовом суперкласса."""
        super().__init__(position=self.randomize_position(), body_color=RED)

    def randomize_position(self):
        """Распределяет случайным образом положение яблока."""
        return (random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1))


def handle_keys():
    """Обрабатывает вводимые пользователем данные."""
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
    """Отрисовка всех игровых объектов на поверхности."""
    surface.fill(BLACK)
    snake.draw(surface)
    apple.draw(surface)
    text = pygame.font.SysFont('Arial', 36).render(
        f"Score: {snake.score}", True, WHITE)
    surface.blit(text, (5, 5))
    pygame.display.update()


def main():
    """Основной игровой цикл."""
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

        screen.fill(BLACK)
        draw_objects(screen, snake, apple)
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()

# Последняя новая строка добавлена в соответствии с PEP8
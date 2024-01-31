# pylint: disable=no-member

"""Модуль описывает простую игру 'Змейка' на основе библиотеки Pygame."""

import sys
import random
import pygame

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BOARD_BACKGROUND_COLOR = BLACK

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

INITIAL_LENGTH = 5
INITIAL_SCORE = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

GAME_SPEED = 10


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=CENTER_POSITION, body_color=WHITE):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, surface, position=None, color=None):
        """Отрисовывает одну ячейку объекта."""
        if position is None:
            position = self.position
        if color is None:
            color = self.body_color
        r = pygame.Rect(
            (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, color, r)

    def draw(self, surface):
        """Отрисовывает игровой объект на поверхности."""
        raise NotImplementedError("Этот метод должен быть переопределен "
                                  "производными классами.")


class Snake(GameObject):
    """Класс, представляющий змею в игре."""

    def __init__(self):
        super().__init__(body_color=GREEN)
        self.length = INITIAL_LENGTH
        self.positions = [CENTER_POSITION]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = INITIAL_SCORE

    def draw(self, surface):
        """Отрисовывает змею на игровом поле."""
        for pos in self.positions:
            self.draw_cell(surface, pos)

    def move(self):
        """Перемещает змею на одну позицию вперед."""
        head_position = self.get_head_position()
        x, y = self.direction
        new_head_position = ((head_position[0] + x) % GRID_WIDTH,
                             (head_position[1] + y) % GRID_HEIGHT)
        if new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Сброс змеи к начальным настройкам."""
        self.length = INITIAL_LENGTH
        self.positions = [CENTER_POSITION]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = INITIAL_SCORE

    def update_direction(self, new_direction):
        """Обновление направления движения змеи."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def get_head_position(self):
        """Получение текущей позиции головы змеи."""
        return self.positions[0]

    def handle_apple_collision(self, apple_position):
        """Обрабатывает столкновение с яблоком."""
        if self.get_head_position() == apple_position:
            self.length += 1
            self.score += 1
            return True
        return False


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        super().__init__(position=self.randomize_position(), body_color=RED)

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(surface)

    def randomize_position(self):
        """Случайным образом задает позицию яблока."""
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
    """Отрисовывает все объекты на игровом поле."""
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
    """Главная функция, запускающая игру."""
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
    main()

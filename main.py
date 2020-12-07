import pygame
import tkinter as tk
pygame.init()


screen_width = 1000
screen_height = 1000
snake_x = screen_height // 2
snake_y = screen_width // 2
display = pygame.display.set_mode((screen_width, screen_height))
snake_block = 50
red_color = (255, 0, 0)
rows = screen_height // snake_block
running = True


def draw_bored():
    x, y = 0, 0
    for _ in range(rows):
        x = x + snake_block
        y = y + snake_block

        # draws a line from start point given in parameter 3 to end point given in parameter 4
        pygame.draw.line(display, (128, 128, 128), (x, 0), (x, screen_width))
        pygame.draw.line(display, (128, 128, 128), (0, y), (screen_width, y))


def redraw_window():
    display.fill((0, 0, 0))
    snake.draw()
    draw_bored()
    pygame.display.update()


class Cube(object):

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, eyes=False):
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(display, self.color, (i*snake_block+1, j*snake_block+1, snake_block-2, snake_block-2))
        if eyes:
            centre = snake_block // 2
            radius = 6
            circle_middle = (i * snake_block + centre - radius, j * snake_block + 16)
            circle_middle2 = (i * snake_block + snake_block - radius * 2, j * snake_block + 16)
            pygame.draw.circle(display, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(display, (0, 0, 0), circle_middle2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos, game_finished):
        self.color = color
        self.game_finished = game_finished
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for snake_event in pygame.event.get():
            if snake_event.type == pygame.QUIT:
                self.game_finished = True
            if snake_event.type == pygame.KEYDOWN:
                if snake_event.key == pygame.K_UP:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                if snake_event.key == pygame.K_DOWN:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                if snake_event.key == pygame.K_LEFT:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                if snake_event.key == pygame.K_RIGHT:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def draw(self):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(True)
            else:
                c.draw()


snake = Snake((255, 0, 0), (10, 10), False)
draw_bored()
clock = pygame.time.Clock()
while running:
    pygame.time.delay(50)
    clock.tick(10)

    snake.move()
    if snake.game_finished:
        break
    redraw_window()

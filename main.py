import pygame
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()
screen_width = 1000
screen_height = 1000
display = pygame.display.set_mode((screen_width, screen_height))
snake_block = 25
red_color = (255, 0, 0)
rows = screen_height // snake_block
running = True


def draw_bored():
    x, y = 0, 0
    for _ in range(rows):
        x += snake_block
        y += snake_block
        # draws a line from start point given in parameter 3 to end point given in parameter 4
        pygame.draw.line(display, (128, 128, 128), (x, 0), (x, screen_width))
        pygame.draw.line(display, (128, 128, 128), (0, y), (screen_width, y))


def redraw_window():
    display.fill((0, 0, 0))
    snake.draw()
    snack.draw(display)
    draw_bored()
    pygame.display.update()


class Cube(object):

    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 0
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        # change the position of the cube
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, eyes=False):
        i = self.pos[0]
        j = self.pos[1]
        # draws the snake without eyes
        pygame.draw.rect(display, self.color,
                         (i * snake_block + 1, j * snake_block + 2, snake_block - 2, snake_block - 2))
        # draws with eyes if the eyes == True
        if eyes:
            center = snake_block // 2
            radius = 4
            # making both of the eyes for the head of the snake
            circle_middle = (i * snake_block + center - radius, j * snake_block + 6)
            circle_middle2 = (i * snake_block + snake_block - radius * 2, j * snake_block + 6)
            # drawing the eyes on the head
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
        self.score = 0

    def move(self):
        movingx = self.dirnx
        movingy = self.dirny
        # searches for a movement on keyboard
        for snake_event in pygame.event.get():
            if snake_event.type == pygame.QUIT:
                self.game_finished = True
            if snake_event.type == pygame.KEYDOWN:
                if snake_event.key == pygame.K_UP and len(self.body) == 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif snake_event.key == pygame.K_DOWN and len(self.body) == 1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif snake_event.key == pygame.K_LEFT and len(self.body) == 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif snake_event.key == pygame.K_RIGHT and len(self.body) == 1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                if snake_event.key == pygame.K_UP and movingy != 1 and movingx != 0 and len(self.body) > 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif snake_event.key == pygame.K_DOWN and movingx != 0 and movingy != -1 and len(self.body) > 1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif snake_event.key == pygame.K_LEFT and movingx != 1 and movingy != 0 and len(self.body) > 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif snake_event.key == pygame.K_RIGHT and movingx != -1 and movingy != 0 and len(self.body) > 1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        # checks for turns and move the snake
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            # checks if the snake touches the walls and end the game if the snake does
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    message_box(self.score)
                    snake.reset((10, 10))
                elif c.dirnx == 1 and c.pos[0] >= rows - 1:
                    message_box(self.score)
                    snake.reset((10, 10))
                elif c.dirny == 1 and c.pos[1] >= rows - 1:
                    message_box(self.score)
                    snake.reset((10, 10))
                elif c.dirny == -1 and c.pos[1] <= 0:
                    message_box(self.score)
                    snake.reset((10, 10))
                else:
                    c.move(c.dirnx, c.dirny)

    # draws the snake
    def draw(self):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(True)
            else:
                c.draw()

    # reset game
    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        # checks where to add a snake part
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        self.score += 1


def random_snack(item):
    positions = item.body
    while True:
        # random x and y
        x = random.randrange(rows)
        y = random.randrange(rows)
        # makes sure that the snack is not on the snake
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


# i dont really know
def message_box(score):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo('You Lost!', f'Score: {score}\nPlay again...')
    snake.score = 0
    try:
        root.destroy()
    except:
        pass


snake = Snake((255, 0, 0), (10, 10), False)
snack = Cube(random_snack(snake), color=(0, 255, 0))
clock = pygame.time.Clock()
while running:
    pygame.time.delay(50)
    clock.tick(10)
    if snake.body[0].pos == snack.pos:
        snake.add_cube()
        # new snack
        snack = Cube(random_snack(snake), color=(0, 255, 0))
    # checks if a part of the body touches an other part of it
    snake_body = snake.body.copy()
    snake_body.remove(snake.head)
    for body_cube in snake_body:
        if snake.head.pos == body_cube.pos:
            # moved body cube that was hit, so we can see the snake head
            snake.body.remove(body_cube)
            redraw_window()
            message_box(snake.score)
            snake.reset((10, 10))

    snake.move()
    if snake.game_finished:
        break
    redraw_window()

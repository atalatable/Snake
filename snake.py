# IMPORTING LIBS #

import sys

import os

from random import randint, choice

import pygame
from pygame.locals import *
from pygame import font

# DECLARATION OF GLOBAL VARIABLES #

# Screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Grid variables
GRID_SIZE = 50
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

# Direction variables
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# DECALRATION OF CLASES #

# Class : Snake
#
# Class for the snake
class Snake(object):
    def __init__(self):
        self.lenght = 1
        self.positions = [(GRID_SIZE * randint(0, GRID_WIDTH), GRID_SIZE * randint(0, GRID_HEIGHT))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        """ input : direction (UP, DOWN, LEFT, RIGHT)

            Change the direction of the snake based on given input
        """
        if self.lenght > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        """ Change the positions of the snake
        """
        head = self.get_head_position()
        x_coord, y_coord = self.direction
        new = (((head[0] + (x_coord*GRID_SIZE)) % SCREEN_WIDTH),
               (head[1] + (y_coord*GRID_SIZE)) % SCREEN_HEIGHT)

        # checking if snake touches himself
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            return 0
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.lenght:
                self.positions.pop()
            return 1

    def reset(self):
        """ Resets the settings of the snake when the game is loose
        """
        self.lenght = 1
        self.positions = [(GRID_SIZE * randint(0, GRID_WIDTH), GRID_SIZE * randint(0, GRID_HEIGHT))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        """ input : surface to draw on

            Draw the snake based on its positions on given surface
        """
        for position in self.positions:
            if position == self.positions[0]:
                rect = pygame.Rect(
                    (position[0]+1, position[1]+1), (GRID_SIZE-2, GRID_SIZE-2))
                pygame.draw.rect(surface, self.color, rect)
            else:
                rect = pygame.Rect(
                    (position[0]+3, position[1]+3), (GRID_SIZE-6, GRID_SIZE-6))
                pygame.draw.rect(surface, self.color, rect)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


# Class : Food
#
# The food poping randomly on the screen
class Food(object):

    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.random_position([0, 0])

    def random_position(self, positions):
        """ input : snake positions

            Generating a random position not on the snake for the food to pop
        """
        test_potision = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        while test_potision in positions:
            test_potision = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

        self.position = test_potision

    def draw(self, surface):
        """ input : surface to draw on

            Draw the snake based on its positions on given surface
        """
        rect = pygame.Rect(
            (self.position[0]+2, self.position[1]+2), (GRID_SIZE-4, GRID_SIZE-4))
        pygame.draw.rect(surface, self.color, rect)


def drawGrid(surface):
    """ input : surface on which to draw the grid 

        Draws grid on the screen
    """
    for i in range(0, int(GRID_HEIGHT)):
        for j in range(0, int(GRID_WIDTH)):
            rect = pygame.Rect((i*GRID_SIZE, j*GRID_SIZE),
                               (GRID_SIZE, GRID_SIZE))
            if (i+j) % 2 == 0:
                pygame.draw.rect(surface, (23, 141, 19), rect)
            else:
                pygame.draw.rect(surface, (27, 176, 22), rect)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont("monospace", 16)
    pygame.display.set_caption('Snake')

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    drawGrid(surface)

    snake = Snake()
    food = Food()

    while True:
        clock.tick(10)

        end = False

        snake.handle_keys()
        drawGrid(surface)
        if not snake.move():
            pause = False
            text_end = font.render(f'Vous avez perdu, Appuyez sur espace pour rejouer', True, (255, 255, 255), (0, 0, 0))
            screen.blit(text_end, (10, SCREEN_HEIGHT/2 - 10))
            pygame.display.update()
            while not pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            pause = True
            end = True

        if snake.get_head_position() == food.position:
            snake.lenght += 1
            snake.score += 1
            food.random_position(snake.positions)

        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        
        text_score = font.render(f'Score : {snake.score}', 1, (0, 0, 0))
        screen.blit(text_score, (7, SCREEN_WIDTH - 20))
        pygame.display.update()


if __name__ == "__main__":
    main()

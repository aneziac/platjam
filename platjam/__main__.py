import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

import platjam.utils as utils
import platjam.colors as colors
from platjam.world import *
from platjam.player import *
import platjam.obstactles as obstacle


TILE_SIZE = 32
SCREEN_WIDTH = TILE_SIZE * 13
screen = utils.Screen((TILE_SIZE * 13, TILE_SIZE * 19))
running = True

# Class instances
world = World(screen)
# player = Player(screen)
display_obstacles = obstacle.ObstaclesDisplay(screen)

while screen.update():
    # update
    keys = pg.key.get_pressed()

    # player.update(keys, False)
    display_obstacles.update()

    # render
    screen.fill(colors.BLUE)

    world.render()
    # player.render()

    screen.clock.tick(60)
    display_obstacles.render()

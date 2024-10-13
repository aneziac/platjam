import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

import platjam.utils as utils
import platjam.colors as colors
from platjam.world import *


TILE_SIZE = 32
SCREEN_WIDTH = TILE_SIZE * 13
screen = utils.Screen((TILE_SIZE * 13, TILE_SIZE * 19))
running = True

# Class instances
world = World(screen)

while screen.update():
    # update
    keys = pg.key.get_pressed()
    # gameplayer.update(keys)

    # render
    screen.fill(colors.BLUE)

    world.render()

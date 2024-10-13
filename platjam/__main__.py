import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

import platjam.utils as utils
import platjam.colors as colors
from platjam.world import *
from platjam.player import *


TILE_SIZE = 32
SCREEN_WIDTH = TILE_SIZE * 13
screen = utils.Screen((TILE_SIZE * 13, TILE_SIZE * 19))
running = True

# Class instances
world = World(screen)
player = Player(screen)

while screen.update():
    # update
    keys = pg.key.get_pressed()

    player.update(keys, False)

    # render
    screen.fill(colors.BLUE)

    world.render()
    player.render()

    screen.clock.tick(60)

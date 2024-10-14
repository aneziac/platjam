import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

import platjam.utils as utils
from platjam.world import *
from platjam.player import *
from platjam.obstactles import *


TILE_SIZE = 32
PLAYER_Y_OFFSET = 6
screen = utils.Screen((16, 28), TILE_SIZE)

# Class instances
world = World(screen, TILE_SIZE, PLAYER_Y_OFFSET)
player = Player(screen, world, PLAYER_Y_OFFSET)
display_obstacles = ObstaclesDisplay(screen, world)

while screen.update():
    # update
    keys = pg.key.get_pressed()
    dtime = screen.clock.get_time()

    player.update(keys, dtime)
    world.update(dtime)
    display_obstacles.update(dtime)

    display_obstacles.obstactle_hits(player)

    # render
    world.render(player.player_pos.y)
    player.render()
    display_obstacles.render()

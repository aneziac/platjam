import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

import platjam.utils as utils
import platjam.colors as colors
from platjam.world import *
from platjam.player import *
import platjam.obstactles as obstacle


TILE_SIZE = 32
PLAYER_Y_OFFSET = 6
screen = utils.Screen((16, 28), TILE_SIZE)

# Class instances
world = World(screen, TILE_SIZE, PLAYER_Y_OFFSET)
player = Player(screen, world, PLAYER_Y_OFFSET)
display_obstacles = obstacle.ObstaclesDisplay(screen)

while screen.update():
    # update
    keys = pg.key.get_pressed()
    dtime = screen.clock.get_time()

    player.update(keys, dtime)
    display_obstacles.update(dtime)

    # render
    screen.fill(colors.BLUE)

    world.render(player.player_pos.y)
    player.render()
    display_obstacles.render()

    # screen.clock.tick(60)

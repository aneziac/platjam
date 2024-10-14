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

game_over = False
hit = False
while screen.update():
    keys = pg.key.get_pressed()

    if not game_over:
        # update
        dtime = screen.clock.get_time()

        player.update(keys, dtime)
        world.update(dtime)
        display_obstacles.update(dtime)

    else:
        if keys[pg.K_r]:
            player.reset()
            world.reset()
            display_obstacles.reset()
            game_over = False

    # render
    is_collided: bool = display_obstacles.obstactle_hits(player)
    game_over = world.render(player.player_pos, player.screen_top_y, is_collided)
    player.render()
    display_obstacles.render()

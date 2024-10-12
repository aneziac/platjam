import pygame as pg

import platjam.utils as utils
import platjam.colors as colors
import platjam.obstactles as obstacle


screen = utils.Screen((900, 600))
running = True

# Class instances
# world = World()
# player = Player()
display_obstacles = obstacle.ObstaclesDisplay(screen)

while screen.update():
    # update
    keys = pg.key.get_pressed()
    # player.update(keys)

    # render
    screen.fill(colors.BLUE)
    display_obstacles.update()

import pygame as pg

import platjam.utils as utils
import platjam.colors as colors
from platjam.player import *


screen = utils.Screen((900, 600))
running = True

# Class instances
# world = World()
player = Player(screen)

while screen.update():
    # update
    keys = pg.key.get_pressed()
    player.update(keys, False)

    # render
    screen.fill(colors.BLUE)
    
    player.render()
    screen.clock.tick(60)

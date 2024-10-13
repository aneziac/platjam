import pygame as pg
import numpy as np
from platjam.utils import Screen
import platjam.colors as colors


class World:
    def __init__(self, screen: Screen):
        self.screen = screen

        self.TILE_SIZE = 32

        self.SCREEN_TILE_WIDTH = int(screen.WIDTH / self.TILE_SIZE)
        self.SCREEN_TILE_HEIGHT = int(screen.HEIGHT / self.TILE_SIZE)

        self.WIDTH = self.SCREEN_TILE_WIDTH
        self.HEIGHT = 20

        self.create_world_map()

    def create_world_map(self):
        self.MAP = np.zeros((self.HEIGHT, self.WIDTH))
        self.MAP[-1] = 1
        for _ in range(10):
            self.MAP[-np.random.randint(1, 5), np.random.randint(1, 10)] = 1

    def render(self):
        # y_tile_offset = round(player.scroll_y - math.floor(player.scroll_y), 3)
        for y in range(self.SCREEN_TILE_HEIGHT):
            for x in range(self.SCREEN_TILE_WIDTH):
                tile = self.MAP[y + 1, x]
                if tile != 0:
                    location = pg.Vector2((x * self.TILE_SIZE, y * self.TILE_SIZE))
                    self.screen.rect(location, (self.TILE_SIZE, self.TILE_SIZE), colors.BLACK)

import pygame as pg
import numpy as np
import sys
from platjam.utils import Screen
import platjam.colors as colors
np.set_printoptions(threshold=sys.maxsize)


class World:
    def __init__(self, screen: Screen, tile_size: int, player_y_offset: int):
        self.screen = screen

        self.TILE_SIZE = tile_size
        self.PLAYER_Y_OFFSET = player_y_offset

        self.SCREEN_TILE_WIDTH = int(screen.WIDTH / self.TILE_SIZE)
        self.SCREEN_TILE_HEIGHT = int(screen.HEIGHT / self.TILE_SIZE)

        self.WIDTH = self.SCREEN_TILE_WIDTH
        self.HEIGHT = self.SCREEN_TILE_HEIGHT * 2

        self.create_world_map()

    def create_world_map(self):
        self.MAP = np.zeros((self.HEIGHT + 1, self.WIDTH))
        self.MAP[-self.PLAYER_Y_OFFSET + 1:] = 1
        for _ in range(10):
            self.MAP[-np.random.randint(7, 9), np.random.randint(1, 10)] = 1
        print(self.MAP)

    def render(self, player_y: float):
        player_y_block = int(player_y) // self.TILE_SIZE
        # print(player_y)
        y_tile_offset = player_y - player_y_block * self.TILE_SIZE
        for y in range(self.SCREEN_TILE_HEIGHT + 1):
            y_tile = y + player_y_block - self.SCREEN_TILE_HEIGHT + self.PLAYER_Y_OFFSET

            for x in range(self.SCREEN_TILE_WIDTH):
                tile = self.MAP[y_tile, x]
                if tile != 0:
                    location = pg.Vector2((x * self.TILE_SIZE, y * self.TILE_SIZE - y_tile_offset))
                    self.screen.rect(location, (self.TILE_SIZE, self.TILE_SIZE), colors.BLACK)

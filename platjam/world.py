import pygame as pg
import numpy as np
import sys
from typing import Optional
from platjam.utils import Screen, load
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

        self.background = self.get_background()

        self.tilemap = self.get_tilemap(load('plain.png', 'tiles').convert())

        self.create_world_map()

    def get_background(self):
        background = pg.Surface((self.screen.WIDTH, self.screen.HEIGHT))
        image = load('background.png', 'tiles')
        image_x, image_y = image.get_size()
        for i in range(self.screen.WIDTH // image_x + 1):
            for j in range(self.screen.HEIGHT // image_y + 1):
                background.blit(image, (i * image_x, j * image_y))

        return background

    def get_tilemap(self, tilemap: pg.Surface) -> list[Optional[pg.Surface]]:
        result: list[Optional[pg.Surface]] = [None]
        for i in range(9):
            result.append(tilemap.subsurface(((i % 3) * 32, (i // 3) * 32, 32, 32)))
        result.append(tilemap.subsurface((224, 160, 32, 32)))

        return result

    def create_world_map(self):
        self.MAP = np.zeros((self.HEIGHT + 5, self.WIDTH), dtype=int)

        bottom = np.tile(np.arange(4, 10).reshape((2, 3)), (self.PLAYER_Y_OFFSET // 2, self.WIDTH // 3 + 1))
        bottom[0, :] = np.tile(np.arange(1, 4), (self.WIDTH // 3 + 1))

        self.MAP[-self.PLAYER_Y_OFFSET:] = bottom[:, :self.WIDTH]

        for _ in range(50):
            self.MAP[-np.random.randint(7, 30), np.random.randint(0, self.WIDTH)] = 10
        # print(self.MAP.shape)

    def render(self, player_y: float):
        self.screen.blit(self.background, (0, 0))

        player_y_block = int(player_y) // self.TILE_SIZE
        y_tile_offset = player_y - player_y_block * self.TILE_SIZE
        for y in range(self.SCREEN_TILE_HEIGHT + 1):
            y_tile = y + player_y_block - self.SCREEN_TILE_HEIGHT + self.PLAYER_Y_OFFSET

            for x in range(self.SCREEN_TILE_WIDTH):
                tile = self.MAP[y_tile, x]
                if tile != 0:
                    location = pg.Vector2((x * self.TILE_SIZE, y * self.TILE_SIZE - y_tile_offset))
                    self.screen.blit(self.tilemap[tile], location)

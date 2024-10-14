import pygame as pg
import numpy as np
import sys
from dataclasses import dataclass
from typing import Optional
from platjam.utils import Screen, load
np.set_printoptions(threshold=sys.maxsize)


@dataclass
class Wave:
    sample = 512  # screen width
    x = np.arange(sample)

    amplitude: float
    initial_phase: float
    frequency: float
    velocity: float

    def calculate(self):
        self.y = self.amplitude * np.sin(
            2 * np.pi * self.frequency * ((Wave.x / Wave.sample) - self.initial_phase)
        )


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
        self.milk_time = 0
        self.milk_level = (self.HEIGHT - 1) * self.TILE_SIZE

        self.tilemap = self.get_tilemap(load('plain.png', 'tiles').convert())

        self.create_world_map()
        self.create_waves()

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

    def update(self, dtime: int):
        self.milk_time += dtime
        self.milk_level -= 1

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

        if self.milk_level < player_y + self.PLAYER_Y_OFFSET * self.TILE_SIZE

        milk = np.zeros(Wave.sample)
        for wave in self.waves:
            offset = int(self.milk_time * wave.velocity) % Wave.sample
            milk += np.roll(wave.y, offset)

        # screen_height =

        for i in range(self.screen.WIDTH):
            self.screen.vline_to_bottom((i, self.screen.HEIGHT - 70 - int(milk[i])))

    def create_waves(self):
        self.waves: list[Wave] = []

        for i in range(1, 3):
            initial_phase = np.random.rand() * 2 * np.pi
            if i == 1:
                frequency = np.random.randint(4, 6)
            else:
                frequency = frequency * np.random.randint(2, 4) + 1
            amplitude = 10 / i
            velocity = (np.random.rand() / 2 + 0.5) / 5
            self.waves.append(Wave(amplitude, initial_phase, frequency, velocity))

        for wave in self.waves:
            wave.calculate()

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
        self.HEIGHT = self.SCREEN_TILE_HEIGHT * 30
        self.INITIAL_SCREEN_TOP = (self.HEIGHT - self.SCREEN_TILE_HEIGHT) * self.TILE_SIZE

        self.RANDOM_BLOCK_SIZE = self.WIDTH // 4

        self.background = self.get_background()

        self.reset()

        self.tilemap = self.get_tilemap(load('plain.png', 'tiles').convert())

        self.font = pg.font.Font('platjam/fonts/retro.ttf', 50)
        self.create_world_map()
        self.create_waves()

    def reset(self):
        self.milk_time = 0
        self.milk_level = (self.HEIGHT - 1) * self.TILE_SIZE
        self.extra_milk_vel = 0

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
        self.MAP = np.zeros((self.HEIGHT + 1, self.WIDTH), dtype=int)

        bottom = np.tile(np.arange(4, 10).reshape((2, 3)), (self.PLAYER_Y_OFFSET // 2, self.WIDTH // 3 + 1))
        bottom[0, :] = np.tile(np.arange(1, 4), (self.WIDTH // 3 + 1))

        self.MAP[-self.PLAYER_Y_OFFSET:] = bottom[:, :self.WIDTH]

        generated_tileset = {}

        for i in range(12):
            tile = np.zeros((4, 4))

            for _ in range(np.random.randint(1, 3)):
                tile[np.random.randint(0, 4), np.random.randint(0, 4)] = 10

            generated_tileset[i] = tile

        generated_tiles = np.random.randint(0, len(generated_tileset), size=((self.HEIGHT - 5) // self.RANDOM_BLOCK_SIZE) * self.RANDOM_BLOCK_SIZE)

        for i, tile_i in enumerate(generated_tiles):
            top_left_x, top_left_y = ((i % 4) * 4, (i // 4) * 4)
            self.MAP[top_left_y:top_left_y + 4, top_left_x:top_left_x + 4] = generated_tileset[tile_i]

    def update(self, dtime: int):
        self.milk_time += dtime + self.extra_milk_vel
        self.milk_level -= 2
        self.extra_milk_vel += 0.01

    def render(self, player_pos: pg.Vector2, screen_top_y: int, hit: bool) -> bool:
        self.screen.blit(self.background, (0, 0))
        player_x, player_y = player_pos.x, player_pos.y

        player_y_block = int(player_y) // self.TILE_SIZE
        y_tile_offset = player_y - player_y_block * self.TILE_SIZE
        for y in range(self.SCREEN_TILE_HEIGHT + 1):
            y_tile = y + player_y_block - self.SCREEN_TILE_HEIGHT + self.PLAYER_Y_OFFSET

            for x in range(self.SCREEN_TILE_WIDTH):
                tile = self.MAP[y_tile, x]
                if tile != 0:
                    location = pg.Vector2((x * self.TILE_SIZE, y * self.TILE_SIZE - y_tile_offset))
                    self.screen.blit(self.tilemap[tile], location)

        milk = np.zeros(Wave.sample)
        for wave in self.waves:
            offset = int(self.milk_time * wave.velocity) % Wave.sample
            milk += np.roll(wave.y, offset)

        game_over = False
        for i in range(self.screen.WIDTH):
            milk_world_y = self.milk_level + int(milk[i])
            milk_screen_y = milk_world_y - screen_top_y
            if milk_screen_y > 0:
                self.screen.vline_to_bottom((i, milk_screen_y))

            if i == int(player_x):
                if player_y > milk_world_y or hit:
                    self.screen.text('GAME OVER', (30, 144, 255), self.font, center=True)
                    game_over = True

        return game_over

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

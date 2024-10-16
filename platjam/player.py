import pygame as pg
from platjam.utils import Screen, load
from platjam.world import World
import numpy as np


class Player:
    def __init__(self, screen: Screen, world: World, player_y_offset: int):
        self.screen = screen
        self.world = world
        self.screen_y_pos = self.screen.HEIGHT - player_y_offset * self.world.TILE_SIZE
        self.Y_OFFSET = player_y_offset
        self.player_acceleration: float = 0.002
        self.speed = 0.4

        self.reset()
        self.initial_y: int = int(self.player_pos.y)

        self.icon = load('player.png', 'player')

    @property
    def tile_pos(self) -> list[int]:
        return [int(self.player_pos.x) // self.world.TILE_SIZE,
                int(self.player_pos.y) // self.world.TILE_SIZE]

    def update(self, keys: list[bool], dtime: int):
        flags = self.detect_surroundings()
        self.move(keys, dtime, flags)
        self.collide(flags)
        self.dy = self.initial_y - int(self.player_pos.y)
        self.screen_top_y: int = self.world.INITIAL_SCREEN_TOP - self.dy

    def move(self, keys: list[bool], dtime: int, flags: int):
        self.old_pos = self.player_pos.copy()
        if not flags & 8:
            self.player_pos.y += self.player_velocity * dtime
            self.player_velocity += self.player_acceleration * dtime

        if self.grounded and (keys[pg.K_w] or keys[pg.K_UP]):
            self.player_pos.y -= 5
            self.player_velocity = -0.75
            self.grounded = False

        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if self.player_pos.x > -self.world.TILE_SIZE:
                self.player_pos.x -= self.speed * dtime
            else:
                self.player_pos.x = self.screen.WIDTH

        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if self.player_pos.x < self.screen.WIDTH:
                self.player_pos.x += self.speed * dtime
            else:
                self.player_pos.x = 0

    def reset(self):
        self.player_pos = pg.Vector2(
            self.screen.WIDTH / 2,
            (self.world.HEIGHT - self.Y_OFFSET) * self.world.TILE_SIZE
        )
        self.player_velocity: float = 0.
        self.grounded = True
        self.dy: int = 0

    def detect_surroundings(self) -> int:
        #                                                         1 2 4 8
        # store blocks near player location as a bitmask in order W N E S
        wall_flags = 0

        self.tile_pos_before = self.tile_pos
        self.tile_pos_before[0] = self.tile_pos_before[0] % self.world.WIDTH

        for n in range(4):
            wall_flags |= (1 << n) * bool(
                self.world.MAP[self.tile_pos_before[1] - int(np.sin(np.pi / 2 * n)),
                               (self.tile_pos_before[0] - int(np.cos(np.pi / 2 * n)) % self.world.WIDTH)]
            )
            if self.world.TILE_SIZE - 2 > self.player_pos.x % self.world.TILE_SIZE > 2 and n % 2 == 1:
                wall_flags |= (1 << n) * bool(
                    self.world.MAP[self.tile_pos_before[1] - int(np.sin(np.pi / 2 * n)),
                                   (self.tile_pos_before[0] + 1) % self.world.WIDTH]
                )

        return wall_flags

    def collide(self, wall_flags: int) -> None:
        # collision resolution based on bitmask flags set by detect_surroundings
        if wall_flags & 1:
            self.player_pos.x = max(self.player_pos.x, self.tile_pos_before[0] * self.world.TILE_SIZE)
        if wall_flags & 2:
            self.player_pos.y = max(self.player_pos.y, self.tile_pos_before[1] * self.world.TILE_SIZE)
        if wall_flags & 4:
            self.player_pos.x = min(self.player_pos.x, self.tile_pos_before[0] * self.world.TILE_SIZE)
        if wall_flags & 8:
            self.player_pos.y = min(self.player_pos.y, self.tile_pos_before[1] * self.world.TILE_SIZE)
            if not self.grounded:
                self.grounded = True
            if self.player_velocity != 0:
                self.player_velocity = 0

    def render(self):
        self.screen.blit(self.icon, pg.Vector2(self.player_pos.x, self.screen_y_pos))

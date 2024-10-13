import os
import random
import pygame as pg
from platjam.utils import Screen, load


class Obstacle:
    def __init__(self, sprite: pg.Surface, scale_factor: float, max_width: int, max_height: int):
        self.max_x = max_width - 16  # 16 is the image size
        self.max_y = max_height
        x = random.randint(0, max_width)
        self.pos = pg.Vector2([x, 0])
        self.scale_factor = scale_factor  # the sprite gets scaled by this amount
        self.radius = 16 * self.scale_factor  # the actual radius is the sprite size multiplied by scale
        self.sprite = sprite
        self.velocity_y = random.randint(3, 8) / 10

    def update(self, dtime: int) -> None:
        self.pos[1] += self.velocity_y * dtime

    def collides(self, other_pos: pg.Vector2) -> bool:
        intersecting_x: bool = other_pos.x < self.pos.x + 16 * self.scale_factor and other_pos.x > self.pos.x
        intersecting_y: bool = other_pos.y < self.pos.y + 16 * self.scale_factor and other_pos.y > self.pos.y
        return intersecting_x and intersecting_y

    def is_out_of_screen(self) -> bool:
        return self.pos[1] > self.max_y


class ObstaclesDisplay:
    def __init__(self, screen: Screen, max_obstacles: int = 5):
        self.screen = screen
        self.scale_factor = 2.5
        self.max_obstacles = max_obstacles
        self.obstacles: list[Obstacle] = []
        self.load_sprites()
        self.create_obstacle()

    def create_obstacle(self) -> None:
        sprite: pg.Surface = self.get_random_sprite()
        new_obstacle: Obstacle = Obstacle(sprite, self.scale_factor, self.screen.WIDTH, self.screen.HEIGHT)
        self.obstacles.append(new_obstacle)

    def load_sprites(self) -> None:
        path: str = f"{os.getcwd()}/platjam/sprites/food"
        files: list[str] = os.listdir(path)
        self.sprites: list[pg.Surface] = []
        for filename in files:
            self.sprites.append(pg.transform.scale_by(load(file=f"{path}/{filename}"), self.scale_factor))

    def get_random_sprite(self) -> pg.Surface:
        sprite_idx: int = random.randint(0, len(self.sprites) - 1)
        return self.sprites[sprite_idx]

    def obstactle_hits(self, other_pos: pg.Vector2) -> bool:
        for obs in self.obstacles:
            if obs.collides(other_pos):
                return True
        return False

    def update(self, dtime: int) -> None:
        for obs in self.obstacles:
            obs.update(dtime=dtime)
            if obs.is_out_of_screen():
                self.obstacles.remove(obs)
                self.create_obstacle()
                continue

    def render(self) -> None:
        for obs in self.obstacles:
            self.screen.blit(obs.sprite, obs.pos)

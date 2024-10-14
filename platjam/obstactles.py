import random
import pygame as pg
from platjam.utils import Screen, load_folder
from platjam.world import World
from platjam.player import Player

scale_factor = 2.5
obstacle_width: int = int(16 * scale_factor)
obstacle_height: int = int(16 * scale_factor)


class Obstacle:
    def __init__(self, sprite: pg.Surface, world: World, max_width: int, max_height: int):
        self.max_x = max_width - 16  # 16 is the image size
        self.max_y = max_height
        self.world = world
        x = random.randint(0, max_width)
        self.pos = pg.Vector2(x, 0)
        self.sprite = sprite
        self.velocity_y = random.randint(3, 8) / 10  # vertical velocity between 0.3 and 0.8
        self.hitbox = (self.pos.x, self.pos.y, obstacle_width, obstacle_height)

    def update(self, dtime: int) -> None:
        self.pos.y += self.velocity_y * dtime
        self.hitbox = (self.pos.x, self.pos.y, obstacle_width, obstacle_height)

    def collides(self, player: Player) -> bool:
        # intersecting_x: bool = other_pos.x < self.pos.x + obstacle_width and other_pos.x > self.pos.x
        other_height: int = 30  # arbitrary! TODO
        other_y = self.world.TILE_SIZE * \
            (self.world.HEIGHT - (self.world.SCREEN_TILE_HEIGHT + self.world.PLAYER_Y_OFFSET)) - \
            (player.initial_y - player.player_pos.y)
        # print("hitbox", self.pos.y, "player", other_y)
        #intersecting_y: bool = other_pos.y > self.hitbox[1] + \
        #    obstacle_height and (other_pos.y + other_height) < (self.hitbox[1] + obstacle_height)
        #if intersecting_y:
        #    print("intersectng on y?", intersecting_y)
        #    exit(0)
        return False  # intersecting_x and intersecting_y

    def is_out_of_screen(self) -> bool:
        return self.pos.y > self.max_y


class ObstaclesDisplay:
    def __init__(self, screen: Screen, world: World, max_obstacles: int = 5):
        self.screen = screen
        self.world = world
        self.max_obstacles = max_obstacles
        self.obstacles: list[Obstacle] = []
        self.load_sprites()
        self.create_obstacle()

    def create_obstacle(self) -> None:
        sprite: pg.Surface = self.get_random_sprite()
        new_obstacle: Obstacle = Obstacle(sprite, self.world, self.screen.WIDTH, self.screen.HEIGHT)
        self.obstacles.append(new_obstacle)

    def load_sprites(self) -> None:
        folder: str = "food"
        self.sprites: list[pg.Surface] = load_folder(folder, (obstacle_width, obstacle_height))

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
            # pg.draw.rect(self.screen._screen, (255, 0, 0), obs.hitbox, 2)
            # self.screen.circle(obs.pos, obs.hitbox[2], (255, 0, 0))

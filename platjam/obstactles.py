import pygame as pg
import random
from platjam.utils import Screen


class Obstacle:
    def __init__(self, max_width: int, max_height: int):
        self.max_x = max_width
        self.max_y = max_height
        x = random.randint(0, max_width)
        self.pos = [x, 0]
        self.radius = random.randint(5, 15)
        self.color = pg.Color(234, 132, 112)

    def update(self) -> None:
        self.pos[1] += 1
        print(self.pos)

    def is_out_of_screen(self) -> bool:
        return self.pos[1] > self.max_y


class ObstaclesDisplay:
    def __init__(self, screen: Screen, max_obstacles: int = 5):
        self.screen = screen
        self.max_obstacles = max_obstacles
        self.obstacles = [Obstacle(screen.WIDTH, screen.HEIGHT)]

    def update(self) -> None:
        for obs in self.obstacles:
            obs.update()
            if obs.is_out_of_screen():
                self.obstacles.remove(obs)
                self.obstacles.append(Obstacle(self.screen.WIDTH, self.screen.HEIGHT))
                continue
            self.screen.circle(obs.pos, obs.radius, obs.color)
        return True

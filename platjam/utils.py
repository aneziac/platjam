import pygame as pg
import pygame.gfxdraw as gfxdraw
import os
import sys
from typing import Optional


class Screen:
    def __init__(self, dims: pg.Vector2, title: str = '', alpha: bool = False):
        pg.init()
        pg.font.init()
        pg.mixer.init()

        flags = 0
        if len(sys.argv) > 1:
            if 'f' in sys.argv[1]:
                flags |= pg.FULLSCREEN
            if "n" in sys.argv[1]:
                flags |= pg.NOFRAME
            elif "r" in sys.argv[1]:
                flags |= pg.RESIZABLE

        self.WIDTH, self.HEIGHT = dims
        self._canvas = pg.display.set_mode(dims, flags)
        if not alpha:
            self._canvas.set_alpha(None)

        if title:
            pg.display.set_caption(title)

        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()

    def text(self,
             text: str,
             color: pg.Color,
             font: pg.font.Font,
             location: Optional[pg.Vector2] = None,
             center: bool = False) -> None:
        if location is None:
            location = pg.Vector2(self.WIDTH / 2, self.HEIGHT // 2)

        rendered_text = font.render(text, True, color)
        if center:
            text_size = font.size(text)

            location.x += text_size[0] // 2
            location.y += text_size[1] // 2
        self._canvas.blit(rendered_text, Screen.floor_vector(location))

    def circle(self, location: pg.Vector2, radius: int, color: pg.Color):
        if self.is_onscreen(location, radius):
            gfxdraw.aacircle(self._canvas, int(location.x), int(location.y), radius, color)
            gfxdraw.filled_circle(self._canvas, int(location.x), int(location.y), radius, color)

    def rect(self, location: pg.Vector2, dims: pg.Vector2, color: pg.Color):
        gfxdraw.box(self._canvas, (Screen.floor_vector(location), dims), color)

    def blit(self, image: pg.Surface, location: pg.Vector2):
        self._canvas.blit(image, Screen.floor_vector(location))

    def is_onscreen(self, location: pg.Vector2, radius: int = 0) -> bool:
        in_width = location.x - radius > 0 and location.x + radius < self.WIDTH
        in_height = location.y - radius > 0 and location.y + radius < self.HEIGHT
        return in_width and in_height

    def fill(self, color: pg.Color) -> None:
        self._canvas.fill(color)

    def update(self) -> bool:
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return False

        self.clock.tick()
        pg.display.flip()
        return True

    @staticmethod
    def floor_vector(vec: pg.Vector2) -> tuple[int, int]:
        return (int(vec.x), int(vec.y))


# Load functions
def load(file: str, extra_path: str = '', scale: Optional[pg.Vector2] = None) -> pg.Surface:
    path = os.path.join(f'./platjam/assets/image/{extra_path}', file)
    image = pg.image.load(path)
    if scale is None:
        return image
    else:
        return pg.transform.scale(image, scale)


# add mirror image argument
def load_folder(folder_path: str, scale: Optional[pg.Vector2] = None):
    textures: list[pg.Surface] = []
    for name in sorted(os.listdir(f'./platjam/assets/image/{folder_path}')):
        if not name.startswith('.'):
            textures.append(load(name, folder_path, scale))
    return textures


def play_music(file_path: str):
    pg.mixer.music.load(file_path)
    pg.mixer.music.play()


def num_files(directory: str):
    return len([name for name in os.listdir(f'./platjam/assets/{directory}')])

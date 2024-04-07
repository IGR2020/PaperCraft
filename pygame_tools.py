import pygame
from os import listdir
from os.path import join, isfile

pygame.font.init()


def blit_text(
    win, text, pos, colour=(0, 0, 0), size=30, font="arialblack", blit=True
):
    font_style = pygame.font.SysFont(font, size)
    text_surface = font_style.render(text, False, colour)
    if blit:
        win.blit(text_surface, pos)
    return text_surface


class Button:
    def __init__(self, pos, image, scale=1):
        x, y = pos
        width, height = image.get_width() * scale, image.get_height() * scale
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False

    def display(self, win):
        win.blit(self.image, self.rect)


def load_assets(path, size: int = None):
    sprites = {}
    for file in listdir(path):
        if not isfile(join(path, file)):
            continue
        if size is None:
            sprites[file.replace(".png", "")] = pygame.image.load(join(path, file))
        else:
            sprites[file.replace(".png", "")] = pygame.transform.scale(
                pygame.image.load(join(path, file)), size
            )
    return sprites

import pygame
from os import listdir
from os.path import isfile, join

pygame.font.init()


def blit_text(
    win, text, pos=(0, 0), colour=(0, 0, 0), size=30, font="arialblack", blit=True
):
    font_style = pygame.font.SysFont(font, size)
    text_surface = font_style.render(text, False, colour)
    if blit:
        win.blit(text_surface, pos)
    return text_surface


class Button:
    def __init__(self, pos, text, scale=1):
        self.x, self.y = pos
        self.width, self.height = text.get_width() * scale, text.get_height() * scale
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.transform.scale(text, (self.width, self.height))

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def display(self, win):
        win.blit(self.image, self.rect)

def load_assets(path, size: int = None):
    sprites = {}
    for file in listdir(path):
        if isfile(file):
            if size is None:
                sprites[file.replace(".png", "")] = pygame.image.load(join(path, file))
            else:
                sprites[file.replace(".png", "")] = pygame.transform.scale(pygame.image.load(join(path, file)), size)
    return sprites


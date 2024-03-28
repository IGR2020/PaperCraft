import pygame
from pygame_tools import blit_text, Button
from constants import inv_slot_img


class Object(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.img = image
        self.name = name

    def render(self, screen, x_offset, y_offset):
        screen.blit(self.img, (self.rect.x - x_offset, self.rect.y - y_offset))


class Block(Object):
    def __init__(self, image, x, y, size, name=None):
        super().__init__(image, x, y, size, size, name)
        self.name = name


class Item:
    def __init__(self, image, name, count=1) -> None:
        self.image = image
        self.name = name
        self.count = count

    def display(self, rect, window):
        window.blit(self.image, (rect.x + 10, rect.y + 10))
        blit_text(
                window,
                str(self.count),
                (rect.x, rect.y),
                size=20,
            )

class EntityItem:
    def __init__(self, img, size, pos):
        self.img = pygame.transform.scale(img, size)
        self.rect = self.img.get_rect(topleft=pos)
        self.y_vel = 0
        self.fall_speed = 0.2

    def display(self, screen, x_offset, y_offset):
        screen.blit(self.img, (self.rect.x - x_offset, self.rect.y - y_offset))

    def loop(self, objects):
        self.y_vel += self.fall_speed
        self.rect.y += self.y_vel
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.y_vel > 0:
                    self.y_vel = 0
                    self.rect.bottom = obj.rect.top
                elif self.y_vel < 0:
                    self.rect.top = obj.rect.bottom

class Slot(Button):
    def __init__(self, pos, item: Item, scale=1):
        super().__init__(pos, inv_slot_img, scale)
        self.item = item
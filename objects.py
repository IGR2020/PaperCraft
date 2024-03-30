import pygame
from pygame_tools import blit_text
from constants import inv_slot_img, slot_size, arrow_img, block_images


class Object():
    def __init__(self, x, y, width, height, name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name

    def render(self, screen, x_offset, y_offset):
        screen.blit(block_images[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))


class Block(Object):
    def __init__(self, x, y, size, name):
        super().__init__(x, y, size, size, name)


class Item:
    def __init__(self, name, count=1) -> None:
        self.name = name
        self.count = count

    def display(self, rect, window):
        window.blit(block_images[self.name], (rect.x + 8, rect.y + 8))
        blit_text(
            window,
            str(self.count),
            (rect.x + 9, rect.y + 9),
            size=15,
        )


class CraftingTable(Block):
    def __init__(self, name, x, y, size):
        super().__init__(name, x, y, size)
        self.inventory = []
        for j in range(9, 6, -1):
            for i in range(13, 16):
                self.inventory.append(Slot((i * slot_size, j * slot_size), None))
        self.result_inventory = [
            Slot((14 * slot_size, 5 * slot_size), None),
            Slot((14 * slot_size, 6 * slot_size), None, 1, arrow_img),
        ]

class Chest(Block):
    def __init__(self, name, x, y, size):
        super().__init__(name, x, y, size)
        self.inventory = []
        for j in range(9, 3, -1):
            for i in range(13, 17):
                self.inventory.append(Slot((i * slot_size, j * slot_size), None))
        self.result_inventory = None

# update display func to refrence image from constants
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

class Button:
    def __init__(self, pos, image, scale=1):
        x, y = pos
        width, height = image.get_width() * scale, image.get_height() * scale
        self.rect = pygame.Rect(x, y, width, height)

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False

    def display(self, win):
        win.blit(inv_slot_img, self.rect)


class Slot(Button):
    def __init__(self, pos, item: Item, scale=1, image=None):
        if image is None:
            super().__init__(pos, inv_slot_img, scale)
        else:
            super().__init__(pos, image, scale)
        self.item = item

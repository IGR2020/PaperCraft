import pygame
from pygame_tools import blit_text
from constants import slot_size, assets, item_fall_speed


def get_break_time(category):
    if category == "wood":
        return 3
    elif category == "soil":
        return 0.75
    elif category == "rock":
        return 10
    elif category == "plant":
        return 0.3
    else:
        return 0


def get_break_bonus(tool_name, category):
    if tool_name == "Wood Pickaxe" and category == "rock":
        return -8
    elif tool_name == "Stone Pickaxe" and category == "rock":
        return -9
    elif tool_name == "Iron Pickaxe" and category == "rock":
        return -9.5
    elif tool_name == "Diamond Pickaxe" and category == "rock":
        return -9.7
    else:
        return 0
    
def get_fuel(fuel_name):
    if fuel_name == "Oak Planks":
        return 1
    if fuel_name == "Oak Wood":
        return 4.5
    if fuel_name == "Coal":
        return 8
    else:
        return 1


class Object:
    def __init__(self, x, y, width, height, name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name

    def render(self, screen, x_offset, y_offset):
        screen.blit(assets[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))


class Block(Object):
    def __init__(self, x, y, size, name, category=None, break_time=None):
        super().__init__(x, y, size, size, name)
        if break_time is not None:
            self.break_time = break_time
        else:
            self.break_time = get_break_time(category)
        self.category = category


class Item:
    def __init__(self, name, type, category=None, break_time=None, count=1, durability=100) -> None:
        self.name = name
        self.count = count
        self.type = type
        if category is None:
            self.break_time = break_time
        else:
            self.break_time = get_break_time(category)
        self.category = category
        self.durability = durability

    def display(self, rect, window):
        window.blit(assets[self.name], (rect.x + 8, rect.y + 8))
        blit_text(
            window,
            str(self.count),
            (rect.x + 9, rect.y + 9),
            size=15,
        )


class CraftingTable(Block):
    def __init__(self, x, y, size, name, category=None, break_time=None):
        super().__init__(x, y, size, name, category, break_time)
        self.inventory = []
        for j in range(9, 6, -1):
            for i in range(13, 16):
                self.inventory.append(
                    Slot((i * slot_size, j * slot_size), None, "Slot")
                )
        self.result_inventory = [
            Slot((14 * slot_size, 5 * slot_size), None, "Slot"),
            Slot((14 * slot_size, 6 * slot_size), None, "Arrow"),
        ]


class Furnace(Block):
    def __init__(self, x, y, size, name, category=None, break_time=None):
        super().__init__(x, y, size, name, category, break_time)
        self.inventory = [
            Slot((14 * slot_size, 7 * slot_size), None, "Slot"),
            Slot((14 * slot_size, 9 * slot_size), None, "Slot"),
        ]
        self.result_inventory = [
            Slot((14 * slot_size, 5 * slot_size), None, "Slot"),
            Slot((14 * slot_size, 6 * slot_size), None, "Arrow"),
        ]
        # items the block can smelt
        self.fuel = 0


class Chest(Block):
    def __init__(self, x, y, size, name, category=None, break_time=None):
        super().__init__(x, y, size, name, category, break_time)
        self.inventory = []
        for j in range(9, 3, -1):
            for i in range(13, 17):
                self.inventory.append(
                    Slot((i * slot_size, j * slot_size), None, "Slot")
                )
        self.result_inventory = None


class EntityItem:
    def __init__(self, name, pos, type, category=None, break_time=None, count=1):
        self.name = name
        self.rect = assets[name].get_rect(topleft=pos)
        self.y_vel = 0
        self.count = count
        self.type = type
        if category is None:
            self.break_time = break_time
        else:
            self.break_time = get_break_time(category)
        self.category = category

    def display(self, screen: pygame.Surface, x_offset, y_offset):
        screen.blit(assets[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))

    def script(self):
        self.y_vel += item_fall_speed
        self.rect.y += self.y_vel

    def solve_collision(self, obj):
        if self.rect.colliderect(obj.rect):
            if self.y_vel > 0:
                self.y_vel = 0
                self.rect.bottom = obj.rect.top
            elif self.y_vel < 0:
                self.rect.top = obj.rect.bottom


class Button:
    def __init__(self, pos, name):
        x, y = pos
        width, height = assets[name].get_width(), assets[name].get_height()
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False

    def display(self, win):
        win.blit(assets[self.name], self.rect)


class Slot(Button):
    def __init__(self, pos, item: Item, name):
        super().__init__(pos, name)
        self.item = item

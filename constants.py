import os
import pygame
from pygame_tools import load_assets

WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper craft")

FPS = 60
run = True
CLOCK = pygame.time.Clock()

item_fall_speed = 0.2

block_size = 32
item_size = 24

terrain_smoothness = 0.03
terrain_variation = 30
cave_size = 24
cave_variation = 0.16
ore_generation = 0.04
ore_vein_size = 7

stack_size = 64
slot_size = 48

scroll_area = 100

chunck_size = 64

world_height = -64
world_depth = 64

VERSION = "0.7.1.4b"

# loading all assets and merging into a single dict
assets = load_assets("assets\\Blocks", (block_size, block_size))
other_assets = load_assets("assets")
items = load_assets("assets\\Blocks", (item_size, item_size))
for i in items:
    assets[f"Item {i}"] = items[i]
assets.update(other_assets)
overlays = load_assets("assets\\Overlay")
for i in overlays:
    overlays[i].set_colorkey((255, 255, 255))
    assets[i] = overlays[i]
del other_assets
del overlays
del items


# horror assets
assets["Light"] = pygame.transform.scale(assets["Light"], (300, 300))
horror_bg_color = (0, 0, 0)
filter = pygame.Surface((WIDTH, HEIGHT))
filter.fill(pygame.color.Color("Grey"))

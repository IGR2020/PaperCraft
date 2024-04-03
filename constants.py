import os
import pygame
from pygame_tools import load_assets

WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper craft")

FPS = 60
RUN = True
CLOCK = pygame.time.Clock()

block_size = 32

terrain_smoothness = 0.03
terrain_variation = 30
cave_size = 24
cave_variation = 0.2
ore_generation = 0.8
ore_vein_size = 7

stack_size = 64
slot_size = 48

scroll_area = 100

chunck_size = 64

world_height = -64
world_depth = 64

assets = load_assets("assets\\Blocks", (block_size, block_size))
other_assets = load_assets("assets")
assets.update(other_assets)
del other_assets
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

terrain_smoothness = 0.02
terrain_variation = 30

stack_size = 64
slot_size = 48

scroll_area = 100

block_images = load_assets("assets\Blocks", (block_size, block_size))

player_img = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "player.jpeg")), (28, 56)
)
inv_slot_img = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "slot.jpeg")), (slot_size, slot_size)
)

arrow_img = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "arrow.png")), (slot_size, slot_size)
)
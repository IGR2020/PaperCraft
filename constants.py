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
slot_size = 70

block_images = load_assets("assets\Blocks", (block_size, block_size))

grass = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "grass.jpeg")), (50, 50)
)
dirt = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "dirt.jpeg")), (50, 50)
)
stone = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "stone.jpeg")), (50, 50)
)
wood = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "wood.jpeg")), (50, 50)
)
leaf = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "leaf.jpeg")), (50, 50)
)
player_img = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "player.jpeg")), (28, 56)
)
inv_slot_img = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "slot.jpeg")), (70, 70)
)
arrow = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "arrow.jpeg")), (70, 70)
)
craft = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "craft.jpeg")), (50, 50)
)
planks = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "planks.jpeg")), (50, 50)
)
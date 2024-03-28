import os
import pygame

WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper craft")

FPS = 60
RUN = True
CLOCK = pygame.time.Clock()

block_size = 50

terrain_smoothness = 0.03
terrain_variation = 30

stack_size = 64
slot_size = 70

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
    pygame.image.load(os.path.join("assets", "player.jpeg")), (45, 95)
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
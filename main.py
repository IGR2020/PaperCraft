from random import randint

import pygame

from pygame_tools import blit_text, Button

from player import Player
from objects import Block, Item, Slot, CraftingTable

from perlin_noise import PerlinNoise
from constants import *

from ui import render_ui, find_slot, manage_inventory, maintain_inventory


def generate_world():
    objects = []
    noise = PerlinNoise()
    for x in range(-WIDTH * 8 // block_size, WIDTH * 8 // block_size):
        current_height = round(noise((x * terrain_smoothness, 0)) * terrain_variation)
        for y in range(current_height, 30):
            objects.append(
                Block(
                    block_images["Stone"],
                    x * block_size,
                    y * block_size,
                    block_size,
                    "Stone",
                )
            )
        objects.append(
            Block(
                block_images["Dirt"],
                x * block_size,
                (current_height - 1) * block_size,
                block_size,
                "Dirt",
            )
        )
        objects.append(
            Block(
                block_images["Grass"],
                x * block_size,
                (current_height - 2) * block_size,
                block_size,
                "Grass",
            )
        )
        if randint(1, 20) == 1:
            for i in range(current_height - 5, current_height - 2):
                objects.append(
                    Block(block_images["Oak Wood"], x * block_size, i * block_size, block_size, "Wood")
                )
            for i in range(current_height - 8, current_height - 5):
                objects.append(
                    Block(block_images["Oak Leaves"], x * block_size, i * block_size, block_size, "Leaf")
                )
                objects.append(
                    Block(
                        block_images["Oak Leaves"], (x - 1) * block_size, i * block_size, block_size, "Leaf"
                    )
                )
                objects.append(
                    Block(
                        block_images["Oak Leaves"], (x + 1) * block_size, i * block_size, block_size, "Leaf"
                    )
                )
    return objects


def crafting():
    recipe_components = []
    for slot in external_inventory:
        if slot.item is not None:
            recipe_components.append(slot.item.name)
    if recipe_components[0] == "Oak Wood" and len(recipe_components) == 1:
        return


# noinspection PyShadowingNames
def setpos(pos):
    x, y = pos
    x -= x % block_size
    y -= y % block_size
    pos = x, y
    return pos


def delete_block():
    x, y = pygame.mouse.get_pos()
    x += x_offset
    y += y_offset
    for obj in blocks_loaded:
        if obj.rect.collidepoint((x, y)):
            slot = find_slot(obj.name, inventory)
            if slot is None:
                return
            if inventory[slot].item is None:
                inventory[slot].item = Item(obj.img, obj.name, 1)
            else:
                inventory[slot].item.count += 1
            blocks_loaded.remove(obj)
    for item in blocks:
        if item.rect.collidepoint((x, y)):
            blocks.remove(item)
            return


# activated opon request to place block
def right_click():
    x, y = pygame.mouse.get_pos()
    x += x_offset
    y += y_offset
    # check for interation
    for obj in blocks_loaded:
        if obj.rect.collidepoint((x, y)):
            interact(obj)
            return
    # checking for illegal placement
    if inventory[selection].item is None:
        return
    if player.rect.collidepoint((x, y)):
        return
    # placing block
    x, y = setpos((x, y))
    if  inventory[selection].item.name == "Crafting Table":
        blocks_loaded.append(
        CraftingTable(
            inventory[selection].item.image,
            x,
            y,
            block_size,
            )
        )
        blocks.append(
            CraftingTable(
                inventory[selection].item.image,
                x,
                y,
                block_size,
            )
        )
        return
    inventory[selection].item.count -= 1
    blocks_loaded.append(
        Block(
            inventory[selection].item.image,
            x,
            y,
            block_size,
            inventory[selection].item.name,
        )
    )
    blocks.append(
        Block(
            inventory[selection].item.image,
            x,
            y,
            block_size,
            inventory[selection].item.name,
        )
    )
    inventory[selection].item.count -= 1

def interact(obj):
    global external_inventory, inv_view, external_inventory_type
    if obj.name == "Crafting Table":
        external_inventory = obj.inventory
        inv_view = True
        external_inventory_type = "Crafting"


def display():
    window.fill((150, 150, 255))
    for obj in blocks_loaded:
        obj.render(window, x_offset, y_offset)
    player.render(window, x_offset, y_offset)
    render_ui(window, inventory, held, external_inventory, inv_view, inv_view, selection)
    pygame.display.update()


if __name__ == "__main__":
    blocks = generate_world()
    blocks_loaded = []
    player = Player(player_img, 28, 56)
    y_offset = 0
    x_offset = 0

    # inventory creation
    inventory = []
    for j in range(9, 4, -1):
        for i in range(6, 12):
            inventory.append(Slot((i * slot_size, j * slot_size), None))
    held = Slot((200, 200), None)
    external_inventory = None
    external_inventory_type = None

    # temporary testing
    inventory[0].item = Item(block_images["Crafting Table"], "Crafting Table", 10)

    selection = 0
    inv_view = False
    for block in blocks:
        if (
            0 - block_size < block.rect.x - x_offset < WIDTH + block_size
            and 0 - block_size < block.rect.y - y_offset < HEIGHT + block_size
        ):
            blocks_loaded.append(block)

    while RUN:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not inv_view:
                    if event.button == 1:
                        delete_block()
                    if event.button == 3:
                        right_click()
                    if event.button == 4:
                        selection += 1
                        if selection >= 6:
                            selection = 0
                    if event.button == 5:
                        selection -= 1
                        if selection < 0:
                            selection = 4
                    if event.button == 2:
                        selection += 1
                        if selection >= 6:
                            selection = 0
                else:
                    manage_inventory(event, inventory, held)
                    if external_inventory is not None:
                        manage_inventory(event, external_inventory, held)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_e:
                    inv_view = not inv_view
                    external_inventory = None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.move_left()
        if keys[pygame.K_a]:
            player.move_right()

        if (
            player.rect.right - x_offset >= WIDTH - scroll_area and player.x_vel > 0
        ) or (player.rect.left - x_offset <= scroll_area and player.x_vel < 0):
            x_offset += player.x_vel
            blocks_loaded = []
            for block in blocks:
                if (
                    0 - block_size * 3
                    < block.rect.x - x_offset
                    < WIDTH + block_size * 3
                    and 0 - block_size * 3
                    < block.rect.y - y_offset
                    < HEIGHT + block_size * 3
                ):
                    blocks_loaded.append(block)

        if (
            player.rect.bottom - y_offset >= HEIGHT - scroll_area and player.y_vel > 0
        ) or (player.rect.top - y_offset <= scroll_area and player.y_vel < 0):
            y_offset += player.y_vel
            blocks_loaded = []
            for block in blocks:
                if (
                    0 - block_size * 3
                    < block.rect.x - x_offset
                    < WIDTH + block_size * 3
                    and 0 - block_size * 3
                    < block.rect.y - y_offset
                    < HEIGHT + block_size * 3
                ):
                    blocks_loaded.append(block)

        maintain_inventory(inventory, held, external_inventory)
        player.loop(blocks_loaded)
        display()

    pygame.quit()

from random import randint

import pygame

from player import Player
from objects import Block, Item, Slot, CraftingTable, Chest

from perlin_noise import PerlinNoise
from constants import *

from world import load_data, save_data, read_pair, write_pair

from os.path import join, isfile

from math import floor, ceil

from ui import (
    render_ui,
    find_slot,
    maintain_inventory,
    manage_all_inventories,
)

def generate_world(
    starting_x=-WIDTH * 2 // block_size, ending_x=WIDTH * 2 // block_size
):
    global noise
    objects = []
    for x in range(starting_x, ending_x):
        current_height = round(noise((x * terrain_smoothness, 0)) * terrain_variation)
        for y in range(current_height, 30):
            objects.append(
                Block(
                    x * block_size,
                    y * block_size,
                    block_size,
                    "Stone",
                )
            )
        objects.append(
            Block(
                x * block_size,
                (current_height - 1) * block_size,
                block_size,
                "Dirt",
            ) 
        )
        objects.append(
            Block(
                x * block_size,
                (current_height - 2) * block_size,
                block_size,
                "Grass",
            )
        )
        if randint(1, 7) == 1:
            for i in range(current_height - 5, current_height - 2):
                objects.append(
                    Block(
                        x * block_size,
                        i * block_size,
                        block_size,
                        "Oak Wood",
                    )
                )
            for i in range(current_height - 8, current_height - 5):
                objects.append(
                    Block(
                        x * block_size,
                        i * block_size,
                        block_size,
                        "Oak Leaves",
                    )
                )
                objects.append(
                    Block(
                        (x - 1) * block_size,
                        i * block_size,
                        block_size,
                        "Oak Leaves",
                    )
                )
                objects.append(
                    Block(
                        (x + 1) * block_size,
                        i * block_size,
                        block_size,
                        "Oak Leaves",
                    )
                )
    return objects


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
    for obj in blocks:
        if obj.rect.collidepoint((x, y)):
            slot = find_slot(obj.name, inventory)
            if slot is None:
                return
            if inventory[slot].item is None:
                inventory[slot].item = Item(obj.name, 1)
            else:
                inventory[slot].item.count += 1
            blocks.remove(obj)


# activated opon request to place block
def right_click():
    x, y = pygame.mouse.get_pos()
    x += x_offset
    y += y_offset
    # check for interation
    for obj in blocks:
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
    normal_args = [
        x,
        y,
        block_size,
        inventory[selection].item.name,
    ]
    # adding correct block type into block data
    if inventory[selection].item.name == "Crafting Table":
        blocks.append(CraftingTable(*normal_args))
    elif inventory[selection].item.name == "Chest":
        blocks.append(Chest(*normal_args))
    else:
        blocks.append(Block(*normal_args))
    inventory[selection].item.count -= 1


def interact(obj):
    global external_inventory, inv_view, external_inventory_type, result_inventory
    if obj.name == "Crafting Table":
        external_inventory = obj.inventory
        inv_view = True
        external_inventory_type = "Crafting"
        result_inventory = obj.result_inventory
    if obj.name == "Chest":
        external_inventory = obj.inventory
        inv_view = True
        external_inventory_type = "Chest"
        result_inventory = obj.result_inventory


def display():
    window.fill((150, 150, 255))
    for obj in blocks:
        obj.render(window, x_offset, y_offset)
    player.render(window, x_offset, y_offset)
    render_ui(
        window,
        inventory,
        held,
        external_inventory,
        result_inventory,
        inv_view,
        inv_view,
        selection,
    )
    pygame.display.update()


if __name__ == "__main__":
    # getting noise
    if isfile("world data\\world1\\noise.pkl"):
        noise = load_data("world data\\world1\\noise.pkl")
    else:
        noise = PerlinNoise()

    # checking if a world exists and reading from it
    if isfile("world data\\world1\\0.pkl"):
        blocks = load_data("world data\\world1\\0.pkl")
    else:
        blocks = generate_world()
    if isfile("world data\\world1\\player data.pkl"):
        player = load_data("world data\\world1\\player data.pkl")
    else:
        player = Player(28, 56)
    x_offset, y_offset = read_pair("world data\\world1\\offsets.txt")
    block_x = 0
    current_chunk = 0
    chunck_changed = False

    # inventory creation
    inventory = []
    for j in range(9, 4, -1):
        for i in range(6, 12):
            inventory.append(Slot((i * slot_size, j * slot_size), None))
    held = Slot((200, 200), None)
    external_inventory = None
    external_inventory_type = None
    result_inventory = None

    selection = 0
    inv_view = False

    while RUN:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # saving all data
                save_data(blocks, join("world data", "world1", f"{current_chunk}.pkl"))
                save_data(player, join("world data", "world1", "player data.pkl"))
                save_data(noise, join("world data", "world1", "noise.pkl"))
                write_pair("world data\\world1\\offsets.txt", round(x_offset), round(y_offset))
                RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not inv_view:
                    if event.button == 1:
                        delete_block()
                    if event.button == 3  :
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
                    manage_all_inventories(
                        event,
                        held,
                        result_inventory,
                        external_inventory_type,
                        inventory,
                        external_inventory,
                    )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_e:
                    inv_view = not inv_view
                    external_inventory = None
                    result_inventory = None
                    external_inventory_type = None
                if event.key == pygame.K_F3:
                    print("Current fps = ", CLOCK.get_fps())
                    print("Current x = ", block_x)
                    print("Current chunk x = ", current_chunk)
                    print("Current y = ", player.rect.y)
                    

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.move_left()
        if keys[pygame.K_a]:
            player.move_right()

        if (
            player.rect.right - x_offset >= WIDTH - scroll_area and player.x_vel > 0
        ) or (player.rect.left - x_offset <= scroll_area and player.x_vel < 0):
            x_offset += player.x_vel
            block_x = player.rect.x // block_size
            temp = current_chunk
            if block_x < 0:
                current_chunk = ceil((block_x - 56) / 113)
            elif block_x > 0:
                current_chunk = floor((block_x + 57) / 113)
            else:
                current_chunk = 0
            chunck_changed = temp != chunck_changed


        if (
            player.rect.bottom - y_offset >= HEIGHT - scroll_area and player.y_vel > 0
        ) or (player.rect.top - y_offset <= scroll_area and player.y_vel < 0):
            y_offset += player.y_vel

        if chunck_changed:
            # saving all data
            save_data(blocks, join("world data", "world1", f"{temp}.pkl"))
            save_data(player, join("world data", "world1", "player data.pkl"))
            save_data(noise, join("world data", "world1", "noise.pkl"))
            write_pair("world data\\world1\\offsets.txt", round(x_offset), round(y_offset))
            if isfile(f"world data\\world1\\{current_chunk}.pkl"):
                blocks = load_data(f"world data\\world1\\{current_chunk}.pkl")
            else:
                if current_chunk < 0:
                    blocks = generate_world(current_chunk*113+56-113, current_chunk*113+56)
                if current_chunk > 0:
                    blocks = generate_world(current_chunk*113-57, current_chunk*113-57+113)
                else:
                    blocks = generate_world()
        # checks if a new chunk has to be generated
        

        maintain_inventory(inventory, held, external_inventory, result_inventory)
        player.loop(blocks)
        display()

    pygame.quit()

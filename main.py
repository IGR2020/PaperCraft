from random import randint

import pygame

from player import Player
from objects import Block, Item, CraftingTable, Chest

from perlin_noise import PerlinNoise
from constants import *

from world import load_data, save_data, read_pair, write_pair

from os.path import join, isfile

from math import floor

from time import perf_counter

from ui import (
    render_ui,
    find_slot,
    maintain_inventory,
    manage_all_inventories,
)

def generate_world(starting_x, ending_x):
    global noise
    objects = []
    for x in range(starting_x, ending_x):
        current_height = round(noise((x * terrain_smoothness, 0)) * terrain_variation)
        for y in range(current_height, current_height+4):
            objects.append(
                    Block(
                        x * block_size,
                        y * block_size,
                        block_size,
                        "Stone",
                    )
                )
        for y in range(current_height+4, world_depth):
            if noise((x*cave_variation, y*cave_variation)) * cave_size < 0.5:
                if abs(noise((x*ore_generation, y*ore_generation)) * ore_vein_size) < 0.022 and y < 32:
                    objects.append(
                    Block(
                        x * block_size,
                        y * block_size,
                        block_size,
                        "Coal Ore",
                    )
                )
                elif 0.02 < abs(noise((x*ore_generation, y*ore_generation)) * ore_vein_size) < 0.04 and y < 38:
                    objects.append(
                    Block(
                        x * block_size,
                        y * block_size,
                        block_size,
                        "Copper Ore",
                    )
                )
                elif 0.04 < abs(noise((x*ore_generation, y*ore_generation)) * ore_vein_size) < 0.06 and 26 < y < 54:
                    objects.append(
                    Block(
                        x * block_size,
                        y * block_size,
                        block_size,
                        "Iron Ore",
                    )
                )
                elif 0.059 < abs(noise((x*ore_generation, y*ore_generation)) * ore_vein_size) < 0.0607 and y > 52:
                    objects.append(
                    Block(
                        x * block_size,
                        y * block_size,
                        block_size,
                        "Diamond Ore",
                    )
                )
                elif 0.0607 < abs(noise((x*ore_generation, y*ore_generation)) * ore_vein_size) < 0.07 and y > 48:
                    objects.append(
                    Block(
                        x * block_size,
                        y * block_size,
                        block_size,
                        "Redstone Ore",
                    )
                )
                elif 0.07 < abs(noise((x*ore_generation, y*ore_generation)) * ore_vein_size) < 0.085 and y > 44:
                    objects.append(
                    Block(
                        x * block_size,
                        y * block_size,
                        block_size,
                        "Lapis Ore",
                    )
                )
                elif 0.07 < abs(noise((x*ore_generation, y*ore_generation)) * ore_vein_size) < 0.074 and y > 58:
                    print("eme")
                    objects.append(
                    Block(
                        x * block_size,
                        y * block_size,
                        block_size,
                        "Emerald Ore",
                    )
                )
                else:
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
                        64 * block_size,
                        block_size,
                        "Bedrock",
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
    for obj in chunk1:
        if obj.rect.collidepoint((x, y)):
            if obj.name == "Bedrock":
                return
            slot = find_slot(obj.name, player.inventory)
            if slot is None:
                return
            if player.inventory[slot].item is None:
                player.inventory[slot].item = Item(obj.name, 1)
            else:
                player.inventory[slot].item.count += 1
            chunk1.remove(obj)
    for obj in chunk2:
        if obj.rect.collidepoint((x, y)):
            if obj.name == "Bedrock":
                return
            slot = find_slot(obj.name, player.inventory)
            if slot is None:
                return
            if player.inventory[slot].item is None:
                player.inventory[slot].item = Item(obj.name, 1)
            else:
                player.inventory[slot].item.count += 1
            chunk2.remove(obj)


# activated opon request to place block
def right_click():
    x, y = pygame.mouse.get_pos()
    x += x_offset
    y += y_offset
    # check for interation
    for obj in chunk1:
        if obj.rect.collidepoint((x, y)):
            interact(obj)
            return
    for obj in chunk2:
        if obj.rect.collidepoint((x, y)):
            interact(obj)
            return
    # checking for illegal placement
    if player.inventory[selection].item is None:
        return
    if player.rect.collidepoint((x, y)):
        return
    # placing block
    x, y = setpos((x, y))
    normal_args = [
        x,
        y,
        block_size,
        player.inventory[selection].item.name,
    ]
    # placing block into correct chunk
    if floor((x//block_size)/chunck_size) != current_chunk:
        # adding correct block type into block data
        if player.inventory[selection].item.name == "Crafting Table":
            chunk2.append(CraftingTable(*normal_args))
        elif player.inventory[selection].item.name == "Chest":
            chunk2.append(Chest(*normal_args))
        else:
            chunk2.append(Block(*normal_args))
    else:
        # adding correct block type into block data
        if player.inventory[selection].item.name == "Crafting Table":
            chunk1.append(CraftingTable(*normal_args))
        elif player.inventory[selection].item.name == "Chest":
            chunk1.append(Chest(*normal_args))
        else:
            chunk1.append(Block(*normal_args))
    player.inventory[selection].item.count -= 1


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

def save_chunk(chunk, chunk_data):
    save_data(chunk_data, join("world data", "world1", f"{chunk}.pkl"))


def display():
    window.fill((150, 150, 255))
    for obj in chunk1:
        obj.render(window, x_offset, y_offset)
    for obj in chunk2:
        obj.render(window, x_offset, y_offset)
    player.render(window, x_offset, y_offset)
    render_ui(
        window,
        player.inventory,
        player.held,
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
        save_data(noise, "world data\\world1\\noise.pkl")

    # getting the loaded chunks
    current_chunk, closest_chunk = read_pair("world data\\world1\\loaded chunks.txt")

    # checking if a world exists and reading from it
    if isfile(f"world data\\world1\\{current_chunk}.pkl"):
        chunk1 = load_data(f"world data\\world1\\{current_chunk}.pkl")
    else:
        chunk1 = generate_world(0, chunck_size)
    if isfile(f"world data\\world1\\{closest_chunk}.pkl"):
        chunk2 = load_data(f"world data\\world1\\{closest_chunk}.pkl")
    else:
        chunk2 = generate_world(-chunck_size, 0)
    if isfile("world data\\world1\\player data.pkl"):
        player = load_data("world data\\world1\\player data.pkl")
    else:
        player = Player(28, 56)
        player.inventory[0].item = Item("Crafting Table")
    x_offset, y_offset = read_pair("world data\\world1\\offsets.txt")
    current_chunk = 0
    closest_chunk = -1
    swap = False

    external_inventory = None
    external_inventory_type = None
    result_inventory = None

    selection = 0
    inv_view = False

    while RUN:
        CLOCK.tick(FPS)

        # getting chunk data
        prev_chunk = current_chunk
        precise_chunk = (player.rect.x // block_size)/chunck_size
        current_chunk = floor(precise_chunk)
        prev_closest_chunk = closest_chunk
        if round(precise_chunk) == current_chunk:
            closest_chunk = current_chunk - 1 
        else:
            closest_chunk = current_chunk + 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # saving all data
                save_chunk(current_chunk, chunk1)
                save_chunk(closest_chunk, chunk2)
                save_data(player, join("world data", "world1", "player data.pkl"))
                write_pair("world data\\world1\\offsets.txt", round(x_offset), round(y_offset))
                write_pair("world data\\world1\\loaded chunks.txt", current_chunk, closest_chunk)
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
                        player.held,
                        result_inventory,
                        external_inventory_type,
                        player.inventory,
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
                    print("Current chunk x = ", current_chunk)
                    print("Previous chunk x = ", prev_chunk)
                    print("Current y = ", player.rect.y)
                    print("Closest chunk = ", closest_chunk)
                    print("Current x = ", player.rect.x // block_size, "\n")
                
                if event.key == pygame.K_TAB:
                    player.rect.x = 450
                    player.rect.y = -1500
                    x_offset = 0
                    y_offset = -1500
                    

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            player.move_left()
        if keys[pygame.K_a]:
            player.move_right()

        if (
            player.rect.right - x_offset >= WIDTH - scroll_area and player.x_vel > 0
        ) or (player.rect.left - x_offset <= scroll_area and player.x_vel < 0):
            x_offset += player.x_vel


        if (
            player.rect.bottom - y_offset >= HEIGHT - scroll_area and player.y_vel > 0
        ) or (player.rect.top - y_offset <= scroll_area and player.y_vel < 0):
            y_offset += player.y_vel

        # managing chunk generation
        if prev_chunk != current_chunk:
            # swaping chunks
            chunk1, chunk2 = chunk2, chunk1
            swap = True
        else:
            swap = False

        if prev_closest_chunk != closest_chunk and not swap:
            # saving all data
            save_chunk(prev_closest_chunk, chunk2)
            if isfile(f"world data\\world1\\{closest_chunk}.pkl"):
                chunk2 = load_data(f"world data\\world1\\{closest_chunk}.pkl")
            else:
                chunk2 = generate_world(closest_chunk*chunck_size, closest_chunk*chunck_size+chunck_size)

        maintain_inventory(player.inventory, player.held, external_inventory, result_inventory)
        player.loop([*chunk1, *chunk2])
        display()

    pygame.quit()

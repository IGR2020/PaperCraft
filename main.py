import pygame

from threading import Thread

from random import randint

from player import Player
from objects import Block, Item, CraftingTable, Chest, EntityItem

from perlin_noise import PerlinNoise
from constants import *

from world import load_data, save_data, read_pair, write_pair, write_string

from os.path import join, isfile

from math import floor

from menu import main_menu

from time import time

from ui import (
    render_ui,
    find_slot,
    maintain_inventory,
    manage_all_inventories,
)

from pygame_tools import remove_prefix

def loop(func, fps: int):
    def loop_func():
        clock = pygame.time.Clock()
        while run:
            clock.tick(fps)
            func()
    return loop_func


def generate_world(starting_x, ending_x):
    global noise
    objects = []
    for x in range(starting_x, ending_x):
        current_height = round(noise((x * terrain_smoothness, 0)) * terrain_variation)
        for y in range(current_height, current_height + 4):
            objects.append(
                Block(
                    x * block_size,
                    y * block_size,
                    block_size,
                    "Stone",
                    "rock"
                )
            )
        for y in range(current_height + 4, world_depth):
            if noise((x * cave_variation, y * cave_variation)) * cave_size < 0.5:
                if abs(
                    noise((x * ore_generation, y * ore_generation)) * ore_vein_size
                ) < 0.07 and y < randint(28, 38):
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Coal Ore",
                            "rock"
                        )
                    )
                elif 0.04 < abs(
                    noise((x * ore_generation, y * ore_generation)) * ore_vein_size
                ) < 0.12 and y < randint(30, 44):
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Copper Ore",
                            "rock"
                        )
                    )
                elif 0.09 < abs(
                    noise((x * ore_generation, y * ore_generation)) * ore_vein_size
                ) < 0.13 and randint(22, 28) < y < randint(48, 60):
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Iron Ore",
                            "rock"
                        )
                    )
                elif 0.11 < abs(
                    noise((x * ore_generation, y * ore_generation)) * ore_vein_size
                ) < 0.12 and y > randint(46, 60):
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Diamond Ore",
                            "rock"
                        )
                    )
                elif 0.12 < abs(
                    noise((x * ore_generation, y * ore_generation)) * ore_vein_size
                ) < 0.17 and y > randint(40, 54):
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Redstone Ore",
                            "rock"
                        )
                    )
                elif 0.15 < abs(
                    noise((x * ore_generation, y * ore_generation)) * ore_vein_size
                ) < 0.2 and y > randint(38, 52):
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Lapis Ore",
                            "rock"
                        )
                    )
                elif 0.21 < abs(
                    noise((x * ore_generation, y * ore_generation)) * ore_vein_size
                ) < 0.24 and y > randint(38, 52):
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Gold Ore",
                            "rock"
                        )
                    )
                elif 0.2 < abs(
                    noise((x * ore_generation, y * ore_generation)) * ore_vein_size
                ) < 0.21 and y > randint(54, 62):
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Emerald Ore",
                            "rock"
                        )
                    )
                else:
                    objects.append(
                        Block(
                            x * block_size,
                            y * block_size,
                            block_size,
                            "Stone",
                            "rock"
                        )
                    )
        objects.append(
            Block(
                x * block_size,
                64 * block_size,
                block_size,
                "Bedrock",
                "rock"
            )
        )
        objects.append(
            Block(
                x * block_size,
                (current_height - 1) * block_size,
                block_size,
                "Dirt",
                "soil"
            )
        )
        objects.append(
            Block(
                x * block_size,
                (current_height - 2) * block_size,
                block_size,
                "Grass",
                "soil"
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
                        "wood"
                    )
                )
            for i in range(current_height - 8, current_height - 5):
                objects.append(
                    Block(
                        x * block_size,
                        i * block_size,
                        block_size,
                        "Oak Leaves",
                        "plant"

                    )
                )
                objects.append(
                    Block(
                        (x - 1) * block_size,
                        i * block_size,
                        block_size,
                        "Oak Leaves",
                        "plant"
                    )
                )
                objects.append(
                    Block(
                        (x + 1) * block_size,
                        i * block_size,
                        block_size,
                        "Oak Leaves",
                        "plant"
                    )
                )
    return objects


def setpos(pos):
    x, y = pos
    x -= x % block_size
    y -= y % block_size
    pos = x, y
    return pos

def add_obj_as_entity(obj):
    entity_pos = (obj.rect.x + 4, obj.rect.y + 4)
    if obj.name == "Bedrock":
        return
    elif obj.name == "Stone":
        entities.append(EntityItem("Item Cobblestone", entity_pos, "Block", "rock", None, 1))
    elif obj.name == "Diamond Ore":
        entities.append(EntityItem("Item Diamond", entity_pos, "Item"))
    elif obj.name == "Iron Ore":
        entities.append(EntityItem("Item Raw Iron", entity_pos, "Item"))
    elif obj.name == "Redstone Ore":
        entities.append(EntityItem("Item Redstone", entity_pos, "Item" ))
    elif obj.name == "Lapis Ore":
        entities.append(EntityItem("Item Lapis", entity_pos, "Item"))
    elif obj.name == "Emerald Ore":
        entities.append(EntityItem("Item Emerald", entity_pos, "Item"))
    elif obj.name == "Gold Ore":
        entities.append(EntityItem("Item Raw Gold", entity_pos, "Item"))
    elif obj.name == "Copper Ore":
        entities.append(EntityItem("Item Raw Copper", entity_pos, "Item"))
    elif obj.name == "Coal Ore":
        entities.append(EntityItem("Item Coal", entity_pos, "Item"))
    else:
        entities.append(EntityItem(f"Item {obj.name}", entity_pos, "Block", break_time=obj.break_time))


def delete_block():
    global target_obj
    if target_obj is None:
        return
    current_time = time()
    if not (current_time > start_time + target_obj.break_time and mouse_down):
        return
    x, y = pygame.mouse.get_pos()
    x += x_offset
    y += y_offset
    for obj in chunk1:
        if obj.rect.collidepoint((x, y)):
            add_obj_as_entity(obj)
            chunk1.remove(obj)
    for obj in chunk2:
        if obj.rect.collidepoint((x, y)):
            add_obj_as_entity(obj)
            chunk2.remove(obj)
    target_obj = None


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
    if player.inventory[selection].item.type == "Item":
        return
    # placing block
    x, y = setpos((x, y))
    normal_args = [
        x,
        y,
        block_size,
        player.inventory[selection].item.name,
        player.inventory[selection].item.break_time
    ]
    # placing block into correct chunk
    if floor((x // block_size) / chunck_size) != current_chunk:
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
    save_data(chunk_data, join("worlds", world_name, f"{chunk}.pkl"))


def manage_collisions():
    for obj in chunk1:
        for entity in entities:
            entity.solve_collision(obj)
    for obj in chunk2:
        for entity in entities:
            entity.solve_collision(obj)


def display():
    if world_type == "Horror":
        window.fill(horror_bg_color)
    elif world_type == "Normal":
        window.fill((150, 150, 255))
    for entity in entities:
        entity.display(window, x_offset, y_offset)
    for obj in chunk1:
        obj.render(window, x_offset, y_offset)
    for obj in chunk2:
        obj.render(window, x_offset, y_offset)
    player.render(window, x_offset, y_offset)
    if world_type == "Horror":
        filter.fill(pygame.color.Color("Grey"))
        y = player.rect.y + 28 - y_offset
        x = player.rect.x + 14 - x_offset
        x -= 150
        y -= 150
        filter.blit(assets["Light"], (x, y))
        window.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
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
    # main menu and getting information
    world_name, world_type = main_menu()

    # getting noise
    if isfile(f"worlds\\{world_name}\\noise.pkl"):
        noise = load_data(f"worlds\\{world_name}\\noise.pkl")
    else:
        noise = PerlinNoise()
        save_data(noise, f"worlds\\{world_name}\\noise.pkl")

    # getting the loaded chunks
    current_chunk, closest_chunk = read_pair(f"worlds\\{world_name}\\loaded chunks.txt")

    # checking if a world exists and reading from it
    if isfile(f"worlds\\{world_name}\\{current_chunk}.pkl"):
        chunk1 = load_data(f"worlds\\{world_name}\\{current_chunk}.pkl")
    else:
        chunk1 = generate_world(0, chunck_size)
    if isfile(f"worlds\\{world_name}\\{closest_chunk}.pkl"):
        chunk2 = load_data(f"worlds\\{world_name}\\{closest_chunk}.pkl")
    else:
        chunk2 = generate_world(-chunck_size, 0)
    if isfile(f"worlds\\{world_name}\\player data.pkl"):
        player = load_data(f"worlds\\{world_name}\\player data.pkl")
    else:
        player = Player(28, 56)
        player.inventory[0].item = Item("Crafting Table", "Block", "wood")
    x_offset, y_offset = read_pair(f"worlds\\{world_name}\\offsets.txt")
    current_chunk = 0
    closest_chunk = -1
    swap = False

    external_inventory = None
    external_inventory_type = None
    result_inventory = None

    # entities
    entities = []

    selection = 0
    inv_view = False

    mouse_down = False

    while run:

        # getting delta time
        CLOCK.tick(FPS)

        # getting chunk data
        prev_chunk = current_chunk
        precise_chunk = (player.rect.x // block_size) / chunck_size
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
                save_data(player, join("worlds", world_name, "player data.pkl"))
                write_pair(
                    f"worlds\\{world_name}\\offsets.txt",
                    round(x_offset),
                    round(y_offset),
                )
                write_pair(
                    f"worlds\\{world_name}\\loaded chunks.txt",
                    current_chunk,
                    closest_chunk,
                )
                write_string(VERSION, f"worlds\\{world_name}\\version.txt")

                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                if not inv_view:
                    if event.button == 1:
                        start_time = time()
                        x, y = pygame.mouse.get_pos()
                        x += x_offset
                        y += y_offset
                        for obj in chunk1:
                            if obj.rect.collidepoint((x, y)):
                                target_obj = obj
                                break
                        else:
                            for obj in chunk2:
                                if obj.rect.collidepoint((x, y)):
                                    target_obj = obj
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
                    manage_all_inventories(
                        event,
                        player.held,
                        result_inventory,
                        external_inventory_type,
                        player.inventory,
                        external_inventory,
                    )
                    
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

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
                    current_chunk = 0
                    closest_chunk = -1
                    prev_chunk = 0
                    prev_closest_chunk = -1
                    chunk1 = load_data(f"worlds\\{world_name}\\{current_chunk}.pkl")
                    chunk2 = load_data(f"worlds\\{world_name}\\{closest_chunk}.pkl")

                if event.key == pygame.K_q:
                    x, y = pygame.mouse.get_pos()
                    x += x_offset
                    y += y_offset
                    if player.inventory[selection].item is not None:
                        entities.append(
                            EntityItem(f"Item {player.inventory[selection].item.name}", (x, y), player.inventory[selection].item.type, break_time=player.inventory[selection].item.break_time)
                        )
                        player.inventory[selection].item.count -= 1

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
        if prev_chunk != current_chunk and not swap:
            # swaping chunks
            chunk1, chunk2 = chunk2, chunk1
            swap = True
        else:
            swap = False

        if prev_closest_chunk != closest_chunk and not swap:
            # saving all data
            save_chunk(prev_closest_chunk, chunk2)
            if isfile(f"worlds\\{world_name}\\{closest_chunk}.pkl"):
                chunk2 = load_data(f"worlds\\{world_name}\\{closest_chunk}.pkl")
            else:
                chunk2 = generate_world(
                    closest_chunk * chunck_size,
                    closest_chunk * chunck_size + chunck_size,
                )
            if isfile(f"worlds\\{world_name}\\{current_chunk}.pkl"):
                save_data(chunk1, f"worlds\\{world_name}\\{current_chunk}.pkl")
            swap = True

        # checking for entity collision
        for entity in entities:
            entity.script()
            if player.rect.colliderect(entity.rect):
                entity.name = remove_prefix(entity.name, "Item ")
                slot = find_slot(entity.name, player.inventory)
                if slot is None:
                    pass
                elif player.inventory[slot].item is None:
                    player.inventory[slot].item = Item(entity.name, entity.type, None, entity.break_time, entity.count)
                else:
                    player.inventory[slot].item.count += entity.count
                entities.remove(entity)
            for ent in entities:
                if (
                    ent.rect.colliderect(entity)
                    and ent.name == entity.name
                    and id(ent) != id(entity)
                ):
                    entity.count += ent.count
                    entities.remove(ent)

        if mouse_down:
            delete_block()

        manage_collisions()
        maintain_inventory(
            player.inventory, player.held, external_inventory, result_inventory
        )
        player.script([*chunk1, *chunk2])
        display()

    pygame.quit()
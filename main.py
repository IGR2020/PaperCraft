from random import randint
from math import floor

import pygame

from pygame_tools import blit_text, Button

from player import Player
from objects import Block, Item, Slot

from perlin_noise import PerlinNoise
from constants import *

from ui import render_ui, maintain_slots, find_slot

def generate_world():
    objects = []
    noise = PerlinNoise()
    for x in range(-WIDTH * 8 // block_size, WIDTH * 8 // block_size):
        current_height = round(noise((x*terrain_smoothness, 0))*terrain_variation)
        for y in range(current_height, 30):
            objects.append(Block(stone, x * block_size, y * block_size, block_size, "Stone"))
        objects.append(
            Block(
                dirt, x * block_size, (current_height - 1) * block_size, block_size, "Dirt"
            )
        )
        objects.append(
            Block(
                grass,
                x * block_size,
                (current_height - 2) * block_size,
                block_size,
                "Grass"
            )
        )
        if  randint(1, 20) == 1:
            for i in range(current_height - 5, current_height - 2):
                objects.append(
                    Block(wood, x * block_size, i * block_size, block_size, "Wood")
                )
            for i in range(current_height - 8, current_height - 5):
                objects.append(
                    Block(leaf, x * block_size, i * block_size, block_size, "Leaf")
                )
                objects.append(
                    Block(leaf, (x - 1) * block_size, i * block_size, block_size, "Leaf")
                )
                objects.append(
                    Block(leaf, (x + 1) * block_size, i * block_size, block_size, "Leaf")
                )
    return objects


def check_slots(image, amount=999):
    avl_pos = []
    for item in inventory:
        if item is not None:
            if image == item[0]:
                if item[1] <= amount:
                    return inventory.index(item)
        if item is None:
            avl_pos.append(item)
    try:
        return inventory.index(avl_pos[0])
    except IndexError:
        return None


def check_stack():
    global held
    for item in [*inventory, *craft_inv]:
        if item is not None:
            if item[1] > stack_size:
                overflow = item[1] - stack_size
                index = check_slots(item[0], stack_size)
                if index is None:
                    item[1] - overflow
                    return None
                if inventory[index] is not None:
                    inventory[index][1] += overflow
                    item[1] -= overflow
                if inventory[index] is None:
                    inventory.pop(index)
                    inventory.insert(index, [item[0], overflow])
                    item[1] -= overflow
    for item in inventory:
        if item is not None:
            if item[1] <= 0:
                index = inventory.index(item)
                inventory.pop(index)
                inventory.insert(index, None)
    for item in craft_inv:
        if item is not None:
            if item[1] <= 0:
                index = craft_inv.index(item)
                craft_inv.pop(index)
                craft_inv.insert(index, None)
    if held is not None:
        if held[1] <= 0:
            held = None


def ui_render():
    blit_text(window, str(floor(CLOCK.get_fps())), size=50)
    for slot in scroll_bar:
        window.blit(inv_slot_img, slot)
    if inv_view:
        for slot in inv_slots:
            window.blit(inv_slot_img, slot)
    pygame.draw.rect(window, (0, 0, 0), scroll_bar[selection])
    if craft_view:
        for slot in craft_slot:
            window.blit(inv_slot_img, slot)
        craft_button.display(window)
    for item in range(len(inventory)):
        if inventory[item] is not None and (len(scroll_bar) > item or inv_view):
            window.blit(
                inventory[item][0],
                (all_slots[item].x + 10, all_slots[item].y + 10),
            )
            blit_text(
                window,
                str(inventory[item][1]),
                (all_slots[item].x + 10, all_slots[item].y + 10),
                size=20,
            )
    for item in range(len(craft_inv)):
        if craft_inv[item] is not None and craft_view:
            window.blit(
                craft_inv[item][0],
                (craft_slot[item].x + 10, craft_slot[item].y + 10),
            )
            blit_text(
                window,
                str(craft_inv[item][1]),
                (craft_slot[item].x + 10, craft_slot[item].y + 10),
                size=20,
            )
    if held is not None:
        pos = pygame.mouse.get_pos()
        pos = [pos[0] - block_size / 2, pos[1] - block_size / 2]
        window.blit(held[0], pos)
        blit_text(window, str(held[1]), pos=pos, size=20)


# noinspection PyShadowingNames
def right_inv(slots, inventory):
    if held is not None:
        pos = pygame.mouse.get_pos()
        for slot in slots:
            if slot.collidepoint(pos):
                index_num = slots.index(slot)
                if inventory[index_num] is not None:
                    if inventory[index_num][0] == held[0]:
                        held[1] -= 1
                        inventory[index_num][1] += 1
                        break
                if inventory[index_num] is None:
                    held[1] -= 1
                    inventory.pop(index_num)
                    inventory.insert(index_num, [held[0], 1])
                    break


# noinspection PyShadowingNames
def left_inv(slots, inventory):
    global held
    pos = pygame.mouse.get_pos()
    for slot in slots:
        if slot.collidepoint(pos):
            index_num = slots.index(slot)
            place = held
            try:
                if inventory[index_num] is not None:
                    if held is None:
                        held = inventory[index_num]
                    elif held[0] == inventory[index_num][0]:
                        place[1] += inventory[index_num][1]
                        held = None
                    else:
                        held = inventory[index_num]
                else:
                    held = None
            except IndexError:
                held = None
            inventory.pop(index_num)
            inventory.insert(index_num, place)


def crafting():
    recipe = []
    for item in range(9):
        if craft_inv[item] is not None:
            recipe.append([craft_inv[item][0], item])
    # planks
    if len(recipe) == 1 and recipe[0][0] == wood:
        if craft_inv[9] is None:
            craft_inv.pop(9)
            craft_inv.append([planks, 4])
        elif craft_inv[9][0] == planks:
            craft_inv[9][1] += 4
        else:
            return
        craft_inv[recipe[0][1]][1] -= 1
    # craft table
    cft = 0
    for item in recipe:
        if item[0] == planks:
            cft += 1
    if cft == 4:
        if (
            recipe[1][1] == recipe[0][1] + 1
            and recipe[2][1] == recipe[0][1] + 3
            and recipe[3][1] == recipe[0][1] + 4
        ):
            if craft_inv[9] is None:
                craft_inv.pop(9)
                craft_inv.append([craft, 1])
            elif craft_inv[9][0] == craft:
                craft_inv[9][1] += 1
            else:
                return
            for item in recipe:
                craft_inv[item[1]][1] -= 1


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


# noinspection PyShadowingNames
def place_block():
    if inventory[selection].item is None:
        return
    x, y = pygame.mouse.get_pos()
    x += x_offset
    y += y_offset
    if player.rect.collidepoint((x, y)):
        return
    for obj in blocks_loaded:
        if obj.rect.collidepoint((x, y)):
            return
    x, y = setpos((x, y))
    blocks_loaded.append(Block(inventory[selection].item.image, x, y, block_size, inventory[selection].item.name))
    blocks.append(Block(inventory[selection].item.image, x, y, block_size, inventory[selection].item.name))
    inventory[selection].item.count -= 1


def display():
    window.fill((150, 150, 255))
    for obj in blocks_loaded:
        obj.render(window, x_offset, y_offset)
    player.render(window, x_offset, y_offset)
    render_ui(window, inventory, held, None, inv_view, False, selection)
    pygame.display.update()


if __name__ == "__main__":
    blocks = generate_world()
    blocks_loaded = []
    player = Player(player_img, 40, 95)
    y_offset = 0
    x_offset = 0
    scroll_area = 100

    # inventory creation
    inventory = []
    for j in range(6, 1, -1):
        for i in range(3, 9):
            inventory.append(Slot((i*slot_size,j*slot_size),None))
    held = Slot((200, 200), None)
    craft_inv = []
    selection = 0
    inv_view = False
    craft_view = False
    craft_slot = []
    craft_button = Button([10 * slot_size + 5, 2 * slot_size - 5], arrow)
    for i in range(9, 12):
        for j in range(3, 6):
            craft_slot.append(
                pygame.Rect(i * slot_size + 5, j * slot_size, slot_size, slot_size)
            )
    craft_slot.append(
        pygame.Rect(10 * slot_size + 5, 1 * slot_size - 10, slot_size, slot_size)
    )
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
                        if place_block() == craft:
                            craft_view = True
                            inv_view = True
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
                if inv_view:
                    if event.button == 1:
                        pass
                    if event.button == 3:
                        pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_e:
                    inv_view = not inv_view
                    if craft_view:
                        for item in craft_inv:
                            if item is not None:
                                pass
                        craft_view = False

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
                    0 - block_size < block.rect.x - x_offset < WIDTH + block_size
                    and 0 - block_size < block.rect.y - y_offset < HEIGHT + block_size
                ):
                    blocks_loaded.append(block)

        if (
            player.rect.bottom - y_offset >= HEIGHT - scroll_area and player.y_vel > 0
        ) or (player.rect.top - y_offset <= scroll_area and player.y_vel < 0):
            y_offset += player.y_vel
            blocks_loaded = []
            for block in blocks:
                if (
                    0 - block_size < block.rect.x - x_offset < WIDTH + block_size
                    and 0 - block_size < block.rect.y - y_offset < HEIGHT + block_size
                ):
                    blocks_loaded.append(block)

        maintain_slots(inventory)
        player.loop(blocks_loaded)
        display()

    pygame.quit()

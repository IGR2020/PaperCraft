import pygame
from objects import Item
from pygame_tools import blit_text
from constants import inv_slot_img


# finds available or matching slots for an item
def find_slot(item, inventory, max_stack_count=64):
    for i, button in enumerate(inventory):
        if button.item is None:
            return i
        elif button.item < max_stack_count and button.item.name == item.name:
            return i
    else:
        return None


def maintain_slots(inventory, max_stack_size=64):
    for button in inventory:
        # checking if the item is illegal
        if button.item is None:
            continue
        if not button.item.count > max_stack_size:
            continue
        if button.item.count > 0:
            continue
        # quick treatment
        else:
            button.item = None
        # illegal item treatment
        overflow = button.item.count - max_stack_size
        button.item.count - overflow
        # finding available position and depositing item if found
        index = find_slot(button.item, inventory, max_stack_size)
        if index is None:
            return
        if inventory[index].item is not None:
            inventory[index].item.count += overflow
        if inventory[index].item is None:
            button.item = Item(button.item.image, button.item.name, overflow)


def ui_render(
    window,
    inventory,
    inv_view,
    selection,
    scroll_bar=[0, 1, 2, 3, 4, 5],
):
    # drawing inventory slots
    if inv_view:
        for slot in inventory:
            window.blit(inv_slot_img, slot.rect)
            slot.item.display(slot.rect, window)
    else:
        for slot_num in scroll_bar:
            window.blit(inv_slot_img, inventory[slot_num].rect)
            inventory[slot].item.display(inventory[slot_num].rect, window)
    pygame.draw.rect(window, (0, 0, 0), inventory[selection])
    # to implement
    if held is not None:
        pos = pygame.mouse.get_pos()
        pos = [pos[0] - block_size / 2, pos[1] - block_size / 2]
        win.blit(held[0], pos)
        blit_text(win, str(held[1]), pos=pos, size=20)

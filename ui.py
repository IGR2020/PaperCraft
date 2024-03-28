import pygame
from objects import Item
from pygame_tools import blit_text
from constants import inv_slot_img, block_size


# finds available or matching slots for an item
def find_slot(item_name, inventory, max_stack_count=64):
    for i, button in enumerate(inventory):
        if button.item is None:
            return i
        elif button.item.count < max_stack_count and button.item.name == item_name:
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
        index = find_slot(button.item.name, inventory, max_stack_size)
        if index is None:
            return
        if inventory[index].item is not None:
            inventory[index].item.count += overflow
        if inventory[index].item is None:
            button.item = Item(button.item.image, button.item.name, overflow)


def render_ui(
    window,
    inventory,
    held,
    external_interface,
    inv_view,
    interface_view,
    selection,
    scroll_bar=[0, 1, 2, 3, 4, 5],
):
    # drawing inventory slots
    if inv_view:
        for slot in inventory:
            window.blit(inv_slot_img, slot.rect)
            if slot.item is not None:
                slot.item.display(slot.rect, window)
    else:
        for slot_num in scroll_bar:
            window.blit(inv_slot_img, inventory[slot_num].rect)
            if inventory[slot_num].item is not None:
                inventory[slot_num].item.display(inventory[slot_num].rect, window)
    pygame.draw.rect(window, (0, 0, 0), inventory[selection])
    if interface_view:
        for slot in external_interface:
            window.blit(inv_slot_img, slot.rect)
            slot.item.display(slot.rect, window)
    # checks for held item
    if held.item is not None:
        x, y = pygame.mouse.get_pos()
        pos = (x - block_size / 2, y - block_size / 2)
        window.blit(held.item, pos)
        blit_text(window, str(held.item.name), pos=pos, size=20)

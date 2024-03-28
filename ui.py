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

# checking for proper inventory
def maintain_slots(inventory, max_stack_size=64):
    for i, button in enumerate(inventory):
        # checking if the item is illegal
        if button.item is None:
            continue
        if not button.item.count > max_stack_size and button.item.count > 0:
            continue
        # quick treatment
        elif button.item.count < 1:
            inventory[i].item = None
            continue
        # illegal item treatment
        overflow = button.item.count - max_stack_size
        button.item.count - overflow
        # finding available position and depositing item if found
        index = find_slot(button.item.name, inventory, max_stack_size)
        if index is None:
            continue
        if inventory[index].item is not None:
            inventory[index].item.count += overflow
        if inventory[index].item is None:
            button.item = Item(button.item.image, button.item.name, overflow)
    return

def maintain_inventory(inventory, held, external_inventroy, max_stack_size=64):
    maintain_slots(inventory, max_stack_size)
    maintain_slots([held], max_stack_size)
    maintain_slots(external_inventroy, max_stack_size)


# rendering ui (inventory + held item + external inventory if there is one)
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
    if inventory[selection].item is not None:
        inventory[selection].item.display(inventory[selection].rect, window)
    if interface_view:
        for slot in external_interface:
            window.blit(inv_slot_img, slot.rect)
            slot.item.display(slot.rect, window)
    # checks for held item
    if held.item is not None:
        x, y = pygame.mouse.get_pos()
        pos = (x - block_size / 2, y - block_size / 2)
        window.blit(held.item.image, pos)
        blit_text(window, str(held.item.count), pos=pos, size=20)


# inventory manegment
def manage_inventory(event, inventory, held):
    x, y = pygame.mouse.get_pos()

    # finding slot
    for slot in inventory:
        if slot.rect.collidepoint((x, y)):
            # checking for left mouse button
            if event.button == 1:
                if held.item is None or slot.item is None:
                    held.item, slot.item = slot.item, held.item
                elif held.item.name == slot.item.name:
                    slot.item.count += held.item.count
                    held.item = None
                else:
                    held.item, slot.item = slot.item, held.item
                return
            # checking for right mouse button
            if event.button == 3:
                if held.item is None and slot.item is None:
                    return
                elif held.item is None and slot.item is not None:
                    held.item = Item(slot.item.image, slot.item.name, 0)
                    held.item.count += slot.item.count // 2
                    slot.item.count -= slot.item.count // 2
                elif held.item is not None and slot.item is None:
                    slot.item = Item(held.item.image, held.item.name, 0)
                    held.item.count -= 1
                    slot.item.count += 1
                elif held.item.name == slot.item.name:
                    held.item.count -= 1
                    slot.item.count += 1
                else:
                    held.item, slot.item = slot.item, held.item
                return

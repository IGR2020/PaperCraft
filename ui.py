import pygame
from objects import Item
from pygame_tools import blit_text
from constants import block_size, assets


# finds available or matching slots for an item
def find_slot(item_name, inventory, max_stack_count=64, avail_count_needed=1):
    for i, button in enumerate(inventory):
        if button.item is None:
            return i
        elif (
            button.item.count <= max_stack_count - avail_count_needed
            and button.item.name == item_name
        ):
            return i
    return None


# checking for proper inventory
def maintain_slots(inventory, max_stack_size=64):
    for i, button in enumerate(inventory):
        # checking if the item is illegal
        if button.item is None:
            continue
        elif button.item.count <= max_stack_size and button.item.count > 0:
            continue
        # quick treatment
        elif button.item.count < 1:
            inventory[i].item = None
            continue

        # finding available position and depositing item if found
        index = find_slot(button.item.name, inventory, max_stack_size)
        if index is None:
            continue
        elif inventory[index].item is None:
            inventory[index].item = Item(
                button.item.name,
                button.item.type,
                None,
                button.item.break_time,
                button.item.count,
            )
            inventory[index].item.count -= max_stack_size
        else:
            inventory[index].item.count += button.item.count - max_stack_size
        button.item.count -= button.item.count - max_stack_size
    return


def maintain_inventory(
    inventory, held, external_inventory, result_inventory, max_stack_size=64
):
    maintain_slots(inventory, max_stack_size)
    maintain_slots([held], max_stack_size)
    if external_inventory is not None:
        maintain_slots(external_inventory, max_stack_size)
    if result_inventory is not None:
        maintain_slots(result_inventory, max_stack_size)


# rendering ui (inventory + held item + external inventory if there is one)
def render_ui(
    window,
    inventory,
    held,
    external_interface,
    result_inventory,
    inv_view,
    interface_view,
    selection,
    scroll_bar=[0, 1, 2, 3, 4, 5],
):
    # drawing inventory slots
    if inv_view:
        for slot in inventory:
            slot.display(window)
            if slot.item is not None:
                slot.item.display(slot.rect, window)
    else:
        for slot_num in scroll_bar:
            inventory[slot_num].display(window)
            if inventory[slot_num].item is not None:
                inventory[slot_num].item.display(inventory[slot_num].rect, window)
    pygame.draw.rect(window, (0, 0, 0), inventory[selection])
    if inventory[selection].item is not None:
        inventory[selection].item.display(inventory[selection].rect, window)
    if interface_view and external_interface is not None:
        for slot in external_interface:
            slot.display(window)
            if slot.item is None:
                continue
            slot.item.display(slot.rect, window)
    if interface_view and result_inventory is not None:
        for slot in result_inventory:
            slot.display(window)
            if slot.item is None:
                continue
            slot.item.display(slot.rect, window)
    # checks for held item
    if held.item is not None:
        x, y = pygame.mouse.get_pos()
        pos = (x - block_size / 2, y - block_size / 2)
        window.blit(assets[held.item.name], pos)
        blit_text(window, str(held.item.count), pos=pos, size=20)


# inventory manegment
def manage_inventory(
    event,
    inventory,
    held,
):
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
                    held.item = Item(
                        slot.item.name, slot.item.type, None, slot.item.break_time, 0
                    )
                    held.item.count += slot.item.count // 2
                    slot.item.count -= slot.item.count // 2
                elif held.item is not None and slot.item is None:
                    slot.item = Item(
                        held.item.name, held.item.type, None, held.item.break_time, 0
                    )
                    held.item.count -= 1
                    slot.item.count += 1
                elif held.item.name == slot.item.name:
                    held.item.count -= 1
                    slot.item.count += 1
                else:
                    held.item, slot.item = slot.item, held.item
                return


def craft(external_inventory):
    recipe_components = []
    # recipe component index corredponding to "wood",recipe components
    rci = []
    for i, slot in enumerate(external_inventory):
        if slot.item is not None:
            recipe_components.append(slot.item.name)
            rci.append(i)
    if len(recipe_components) < 1:
        return (None, None)
    elif recipe_components[0] == "Oak Wood" and len(recipe_components) == 1:
        return (Item("Oak Planks", "Block", "wood", None, 4), recipe_components)
    elif (
        recipe_components == ["Oak Planks", "Oak Planks", "Oak Planks", "Oak Planks"]
        and rci[0] + 4 == rci[1] + 3 == rci[2] + 1 == rci[3]
    ):
        return (Item("Crafting Table", "Block", "wood", None, 1), recipe_components)
    elif (
        recipe_components == ["Stone", "Stone", "Stone", "Stone"]
        and rci[0] + 4 == rci[1] + 3 == rci[2] + 1 == rci[3]
    ):
        return (Item("Stone Brick", "Block", "rock", None, 4), recipe_components)
    elif (
        len(recipe_components) == 8
        and rci == [0, 1, 2, 3, 5, 6, 7, 8]
        and "Oak Planks" in recipe_components
        and len(set(recipe_components)) == 1
    ):
        return (Item("Chest", "Block", "wood", None, 1), recipe_components)
    elif (
        len(set(recipe_components)) == 1
        and "Oak Planks" in recipe_components
        and len(recipe_components) == 2
        and rci[0] + 3 == rci[1]
    ):
        return (Item("Stick", "Item", count=4), recipe_components)
    elif rci == [1, 4, 6, 7, 8] and recipe_components == [
        "Stick",
        "Stick",
        "Oak Planks",
        "Oak Planks",
        "Oak Planks",
    ]:
        return (Item("Wood Pickaxe", "Tool", count=1), recipe_components)
    else:
        return (None, None)


def manage_all_inventories(
    event,
    held,
    result_inventory,
    external_inventory_type,
    inventory,
    external_inventory,
):
    # allows manegment of inventories
    manage_inventory(event, inventory, held)
    if external_inventory is not None:
        manage_inventory(event, external_inventory, held)
    x, y = pygame.mouse.get_pos()
    if external_inventory_type == "Crafting":
        result_inventory[0].item, items_used = craft(external_inventory)
        if result_inventory[0].rect.collidepoint((x, y)):
            if result_inventory[0].item is None:
                return
            # removes used items
            for item_used in items_used:
                for slot in external_inventory:
                    if slot.item is None:
                        continue
                    if slot.item.name == item_used:
                        slot.item.count -= 1
                        maintain_slots(external_inventory)
                        break
            if event.button == 1:
                if held.item is None:
                    held.item = result_inventory[0].item
                elif result_inventory[0].item is not None:
                    if held.item.name == result_inventory[0].item.name:
                        held.item.count += result_inventory[0].item.count
            elif event.button == 3:
                slot_index = find_slot(result_inventory[0].item.name, inventory)
                if (
                    inventory[slot_index].item is not None
                    and result_inventory[0].item is not None
                ):
                    inventory[slot_index].item.count += result_inventory[0].item.count
                if inventory[slot_index].item is None:
                    inventory[slot_index].item = result_inventory[0].item
                result_inventory[1].item = None
    elif external_inventory_type == "Chest":
        return

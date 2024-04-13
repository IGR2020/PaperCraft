import pygame as pg
from objects import Item, get_fuel
from time import time

def craft(external_inventory):
    recipe_components = []
    # recipe component index corredponding to recipe components
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
        return (Item("Chest", "Block", "rock", None, 1), recipe_components)
    elif (
        len(recipe_components) == 8
        and rci == [0, 1, 2, 3, 5, 6, 7, 8]
        and "Cobblestone" in recipe_components
        and len(set(recipe_components)) == 1
    ):
        return (Item("Furnace", "Block", "wood", None, 1), recipe_components)
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
        return (Item("Wood Pickaxe", "Tool", count=1, durability=32), recipe_components)
    elif rci == [1, 4, 6, 7, 8] and recipe_components == [
        "Stick",
        "Stick",
        "Cobblestone",
        "Cobblestone",
        "Cobblestone",
    ]:
        return (Item("Stone Pickaxe", "Tool", count=1, durability=96), recipe_components)
    elif rci == [1, 4, 6, 7, 8] and recipe_components == [
        "Stick",
        "Stick",
        "Iron Ingot",
        "Iron Ingot",
        "Iron Ingot",
    ]:
        return (Item("Iron Pickaxe", "Tool", count=1, durability=182), recipe_components)
    elif rci == [1, 4, 6, 7, 8] and recipe_components == [
        "Stick",
        "Stick",
        "Diamond",
        "Diamond",
        "Diamond",
    ]:
        return (Item("Diamond Pickaxe", "Tool", count=1, durability=320), recipe_components)
    elif rci == [1, 4, 6, 7, 8] and recipe_components == [
        "Stick",
        "Stick",
        "Gold Ingot",
        "Gold Ingot",
        "Gold Ingot",
    ]:
        return (Item("Gold Pickaxe", "Tool", count=1, durability=320), recipe_components)
    elif rci == [1, 3, 4, 6, 7] and recipe_components == [
        "Stick",
        "Diamond",
        "Stick",
        "Diamond",
        "Diamond",
    ]:
        return (Item("Diamond Axe", "Tool", count=1, durability=320), recipe_components)
    elif rci == [1, 3, 4, 6, 7] and recipe_components == [
        "Stick",
        "Iron Ingot",
        "Stick",
        "Iron Ingot",
        "Iron Ingot",
    ]:
        return (Item("Iron Axe", "Tool", count=1, durability=320), recipe_components)
    elif rci == [1, 3, 4, 6, 7] and recipe_components == [
        "Stick",
        "Oak Planks",
        "Stick",
        "Oak Planks",
        "Oak Planks",
    ]:
        return (Item("Wood Axe", "Tool", count=1, durability=320), recipe_components)
    elif rci == [1, 3, 4, 6, 7] and recipe_components == [
        "Stick",
        "Stone",
        "Stick",
        "Stone",
        "Stone",
    ]:
        return (Item("Stone Axe", "Tool", count=1, durability=320), recipe_components)
    elif rci == [1, 3, 4, 6, 7] and recipe_components == [
        "Stick",
        "Gold Ingot",
        "Stick",
        "Gold Ingot",
        "Gold Ingot",
    ]:
        return (Item("Diamond Axe", "Tool", count=1, durability=320), recipe_components)
    else:
        return (None, None)

def smelt(inventory):
    if inventory[0].item is None: return None, None
    if inventory[1].item is None: return None, None
    fuel = get_fuel(inventory[1].item.name)
    if inventory[0].item.name == "Raw Iron":
        return Item("Iron Ingot", "Item"), fuel # returns fuel use ex. if fuel = 8 then item duarability * 1/8
    elif inventory[0].item.name == "Raw Gold":
        return Item("Gold Ingot", "Item"), fuel
    else:
        return None, None

from constants import *
import pygame as pg
from os import listdir, makedirs
from pygame_tools import Button, blit_text
from world import write_pair, write_string, read_string

def main_menu():
    world_name = ""
    all_worlds = [f for f in listdir("worlds")]
    run = True
    mode = "Menu"
    select = False

    play_button = Button((206, 320), assets["Play"])

    horror = False
    horror_button = Button((220, 50), assets["Horror"])

    world_type = "Normal"
    
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONUP:
                if play_button.clicked() and mode == "Menu":
                    mode = "Create"
                    select = True
                if horror_button.clicked() and mode == "Create":
                    horror = not horror
                    if horror:
                        world_type = "Horror"
                        horror_button.image = assets["Horror Clicked"]
                    else:
                        world_type = "Normal"
                        horror_button.image = assets["Horror"]
            if event.type == pg.KEYDOWN and select:
                if event.key == pg.K_RETURN:
                    world_exists = False
                    for file in all_worlds:
                        if file == world_name:
                            world_exists = True
                            world_version = read_string(f"worlds\\{world_name}\\version.txt")
                            if world_version != VERSION:
                                if version_warning():
                                    return world_name, world_type
                            else:
                                return world_name, world_type
                    if not world_exists:
                        makedirs(f"worlds\\{world_name}")
                        write_pair(f"worlds\\{world_name}\\offsets.txt", 0, -1500)
                        write_pair(f"worlds\\{world_name}\\loaded chunks.txt", 0, -1)
                        write_string(VERSION, f"worlds\\{world_name}\\version.txt")
                        return world_name, world_type
                if event.key == pg.K_BACKSPACE:
                    world_name = world_name[:-1]
                else:
                    world_name += event.unicode
        if play_button.clicked():
            play_button.image = assets["Play Hover"]
        else:
            play_button.image = assets["Play"]
        window.fill((0, 0, 0))
        if mode == "Menu":
            window.blit(assets["Title"], (186.5, 50))
            play_button.display(window)
        elif mode == "Create":
            horror_button.display(window)
            blit_text(window, "Enter World Name", (322, 280), (255, 255, 255), 25)
            window.blit(assets["Text Box"], (322, 320))
            blit_text(window, world_name, (340, 340), (255, 255, 255), 15)
        pg.display.update()

    pg.quit()
    quit()

def version_warning():
    run = True
    procced_button = Button((322, 320), blit_text(None, "Procced", None, (255, 255, 255), size=30, blit=False))
    return_button = Button((322, 200), blit_text(None, "Return", None, (255, 255, 255), size=30, blit=False))
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if procced_button.clicked():
                    return True
                if return_button.clicked():
                    return False
        window.fill((0, 0, 0))
        blit_text(window, "World Version does not", (322, 50), (255, 255, 255), size=30)
        blit_text(window, "match current game version", (322, 90), (255, 255, 255), size=30)
        procced_button.display(window)
        return_button.display(window)
        pg.display.update()
    pg.quit()
    quit()
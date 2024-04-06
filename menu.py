from constants import *
import pygame as pg
from os import listdir, makedirs
from pygame_tools import Button, blit_text
from world import write_pair

def main_menu():
    world_name = ""
    all_worlds = [f for f in listdir("worlds")]
    run = True
    mode = "menu"
    select = False

    play_button = Button((206, 320), assets["Play"])
    
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONUP:
                if play_button.clicked():
                    mode = "Create"
                    select = True
            if event.type == pg.KEYDOWN and select:
                if event.key == pg.K_RETURN:
                    for file in all_worlds:
                        if file == world_name:
                            return world_name
                    else:
                        makedirs(f"worlds\\{world_name}")
                        write_pair(f"worlds\\{world_name}\\offsets.txt", 0, -1500)
                        write_pair(f"worlds\\{world_name}\\loaded chunks.txt", 0, -1)
                        return world_name
                if event.key == pg.K_BACKSPACE:
                    world_name = world_name[:-1]
                else:
                    world_name += event.unicode
        if play_button.clicked():
            play_button.image = assets["Play Hover"]
        else:
            play_button.image = assets["Play"]
        window.fill((0, 0, 0))
        if mode == "menu":
            window.blit(assets["Title"], (186.5, 50))
            play_button.display(window)
        elif mode == "Create":
            blit_text(window, "Enter World Name", (322, 280), (255, 255, 255), 25)
            window.blit(assets["Text Box"], (322, 320))
            blit_text(window, world_name, (340, 340), (255, 255, 255), 15)
        pg.display.update()

    pg.quit()
    quit()
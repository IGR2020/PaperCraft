from constants import *
import pygame as pg
from os import listdir, makedirs
from pygame_tools import *
from world import write_pair, write_string, read_string
from world import load_data

def main_menu():
    world_name = ""
    all_worlds = [f for f in listdir("worlds")]
    run = True
    mode = "Menu"
    select = False

    play_button = Button((206, 320), assets["Play"])

    horror = False
    horror_button = Button((220, 50), assets["Horror"])

    chunkViewButton = Button((0, HEIGHT-slot_size), assets["Chunk View"])

    world_type = "Normal"
    
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if chunkViewButton.clicked():
                    chunkViewButton.image = assets["Chunk View Pressed"]
            if event.type == pg.MOUSEBUTTONUP:
                chunkViewButton.image = assets["Chunk View"]
                if chunkViewButton.clicked():
                    viewChunks()
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
            chunkViewButton.display(window)
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

def viewChunks():
    run = True
    renderChunk = False
    x_offset, y_offset = 0, 0
    chunks = []
    caption = Text("Enter World Name", WIDTH/2, HEIGHT/2 - 80, (255, 255, 255), 40, "ArialBlack", center=True)
    enterName = TextBox(assets["Text Box Clean"], assets["Text Box Clean"], 4, WIDTH/2, HEIGHT/2, (0, 0, 0), 30, "ArialBlack", center=True)
    while run:
        for event in pg.event.get():
            enterName.update_text(event)
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE and not enterName.selected:
                    return
                
                if event.key == pg.K_RETURN:
                    try:
                        for file in listdir(f"worlds/{enterName.text}"):
                            if file[0] in "-1234567890":
                                chunks.append(load_data(f"worlds/{enterName.text}/{file}"))
                        renderChunk = True
                    except:
                        continue
        enterName.select()
        if renderChunk:
            window.fill((150, 150, 255))
            rel_x, rel_y = pg.mouse.get_rel()
            if True in pg.mouse.get_pressed():
                x_offset -= rel_x
                y_offset -= rel_y
            for chunk in chunks:
                for block in chunk:
                    block.render(window, x_offset, y_offset)
        else:
            window.fill((30, 30, 30))
            enterName.display(window)
            caption.display(window)
        pg.display.update()
import pygame
from os import listdir
from os.path import join, isfile
import pygame as pg

class Text():
    def __init__(self, text, x, y, color, size, font,  center=False, centerx=False, centery=False) -> None:

        # saving reconstruction data
        self.text = text
        self.color = color
        self.size = size
        self.font = font

        # creating text surface
        font_style = pg.font.SysFont(self.font, self.size)
        text_surface = font_style.render(self.text, True, self.color)
        if center:
            x -= text_surface.get_width() // 2
            y -= text_surface.get_height() // 2
        else:
            if centerx:
                x -= text_surface.get_width() // 2
            if centery:
                y -= text_surface.get_height() // 2

        self.image = text_surface
        self.rect = text_surface.get_rect(topleft=(x, y))
        
        self.type = "Text"

    def reload(self, reloadRect=True):
        font_style = pg.font.SysFont(self.font, self.size)
        text_surface = font_style.render(self.text, True, self.color)

        self.image = text_surface

        if reloadRect:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)        

    def display(self, window):
        window.blit(self.image, self.rect)

class TextBox():
    def __init__(self,  imageName, selectedImageName, border: tuple[int, int] | int, x, y, color, size, font, text="", center=False) -> None:
        
        # saving reconstruction data
        self.text = text
        self.color = color
        self.size = size
        self.font = font


        self.boxImage = imageName
        self.selectedBoxName = selectedImageName

        if isinstance(border, int):
            self.border = (border, border)   
        else:         
            self.border = border

        if center:
            self.rect = self.boxImage.get_rect(center=(x, y))
        else:            
            self.rect = self.boxImage.get_rect(topleft=(x, y))

        self.image = None
        Text.reload(self, False)

        self.selected = False
        self.type = "TextBox"

    def reload(self):
        Text.reload(self, False)

    def display(self, window):
        if self.selected:
            window.blit(self.selectedBoxName, self.rect)
        else:            
            window.blit(self.boxImage, self.rect)
        window.blit(self.image, (self.rect.x + self.border[0], self.rect.y + self.border[1]))

    def select(self, pos=None, clicked_button=None) -> bool:
        if pos is None:
            pos = pg.mouse.get_pos()
        x, y = pos
        mouseDown = pg.mouse.get_pressed()
        if clicked_button is None:
            if True in mouseDown:
                mouseDown = True
            else:
                mouseDown = False
        else:
            mouseDown = mouseDown[clicked_button]

        if self.rect.collidepoint((x, y)) and mouseDown:
            self.selected = True
        elif not self.rect.collidepoint((x, y)) and mouseDown:
            self.selected = False

        return self.selected
    
    def update_text(self, event):
        """Call inside event loop"""
        if event.type != pg.KEYDOWN or not self.selected:
            return
        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
            self.text += "|"
        elif event.unicode == "\r":
            self.selected = False
            self.text += "|"
        else:
            self.text += event.unicode
            self.text += "|"
        self.reload()
        self.text = self.text[:-1]



class Button:
    def __init__(self, pos, image, scale=1):
        x, y = pos
        width, height = image.get_width() * scale, image.get_height() * scale
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        return False

    def display(self, win):
        win.blit(self.image, self.rect)


def load_assets(path, size: int = None):
    sprites = {}
    for file in listdir(path):
        if not isfile(join(path, file)):
            continue
        if size is None:
            sprites[file.replace(".png", "")] = pygame.image.load(join(path, file))
        else:
            sprites[file.replace(".png", "")] = pygame.transform.scale(
                pygame.image.load(join(path, file)), size
            )
    return sprites

def remove_prefix(str: str, prefix: str):
    return str[len(prefix):] if str.startswith(prefix) else str


pygame.font.init()


def blit_text(
    win,
    text,
    pos,
    colour=(0, 0, 0),
    size=30,
    font="arialblack",
    blit=True,
    centerx=False,
    centery=False,
    center=False,
):
    text = str(text)
    x, y = pos
    font_style = pygame.font.SysFont(font, size)
    text_surface = font_style.render(text, True, colour)
    if center:
        x -= text_surface.get_width() // 2
        y -= text_surface.get_height() // 2
    else:
        if centerx:
            x -= text_surface.get_width() // 2
        if centery:
            y -= text_surface.get_height() // 2
    if blit:
        win.blit(text_surface, (x, y))
    return text_surface

import pygame
from constants import assets, slot_size
from objects import Slot
from time import time


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.rect = pygame.Rect(450, -1500, width, height)
        self.y_vel = 0
        self.x_vel = 0
        self.fall_speed = 0.2
        self.jump_count = 0
        self.direction = "left"
        self.speed = 5
        self.inventory = []
        for j in range(9, 4, -1):
            for i in range(6, 12):
                self.inventory.append(
                    Slot((i * slot_size, j * slot_size), None, "Slot")
                )
        self.held = Slot((200, 200), None, "Slot")
        self.is_sprinting = False
        self.default_speed = 3

    def render(self, screen, x_offset, y_offset):
        screen.blit(assets["Player"], (self.rect.x - x_offset, self.rect.y - y_offset))

    def script(self, objects):
        self.y_vel += self.fall_speed
        self.y_vel = min(16, self.y_vel)
        self.rect.y += self.y_vel
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.y_vel > 0:
                    self.y_vel = 0
                    self.rect.bottom = obj.rect.top
                    self.jump_count = 0
                elif self.y_vel < 0:
                    self.rect.top = obj.rect.bottom
                self.default_speed = 3
                break
        else:
            self.default_speed = 2
        self.move(objects)

    def move(self, objects):
        self.rect.x += self.x_vel
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.x_vel > 0:
                    self.rect.right = obj.rect.left
                elif self.x_vel < 0:
                    self.rect.left = obj.rect.right
                self.jump()
        self.x_vel = 0

    def move_left(self):
        if self.default_speed == 2 and self.is_sprinting:
            self.speed = self.default_speed + 1.5
        elif self.is_sprinting:
            self.speed = 5
        else:
            self.speed = self.default_speed
        self.x_vel += self.speed
        self.direction = "left"

    def move_right(self):
        if self.default_speed == 2 and self.is_sprinting:
            self.speed = self.default_speed + 1.5
        elif self.is_sprinting:
            self.speed = 5
        else:
            self.speed = self.default_speed
        self.x_vel -= self.speed
        self.direction = "right"

    def jump(self):
        if self.jump_count == 0:
            self.jump_count += 1
            self.y_vel = -4

import pygame
from constants import assets, slot_size
from objects import Slot


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.rect = pygame.Rect(450, -1500, width, height)
        self.y_vel = 0
        self.x_vel = 0
        self.fall_speed = 0.2
        self.jump_count = 0
        self.direction = "left"
        self.inventory = []
        for j in range(9, 4, -1):
            for i in range(6, 12):
                self.inventory.append(
                    Slot((i * slot_size, j * slot_size), None, "Slot")
                )
        self.held = Slot((200, 200), None, "Slot")

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
        self.x_vel += 5
        self.direction = "left"

    def move_right(self):
        self.x_vel -= 5
        self.direction = "right"

    def jump(self):
        if self.jump_count == 0:
            self.jump_count += 1
            self.y_vel = -4

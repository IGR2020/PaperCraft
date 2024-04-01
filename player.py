import pygame
from constants import player_img


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.rect = pygame.Rect(450, -1500, width, height)
        self.y_vel = 0
        self.x_vel = 0
        self.fall_speed = 0.2
        self.jump_count = 0

    def render(self, screen, x_offset, y_offset):
        screen.blit(player_img, (self.rect.x - x_offset, self.rect.y - y_offset))

    def loop(self, objects):
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
        self.x_vel = 0

    def move_left(self):
        self.x_vel += 5

    def move_right(self):
        self.x_vel -= 5

    def jump(self):
        if self.jump_count == 0:
            self.jump_count += 1
            self.y_vel = -5
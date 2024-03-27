import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, width, height):
        super().__init__()
        self.rect = pygame.Rect(450, -2000, width, height)
        self.img = image
        self.y_vel = 0
        self.x_vel = 0
        self.fall_speed = 0.2
        self.jump_count = 0
        self.inventory = []
        for i in range(30):
            self.inventory.append(None)
        self.selection = 0

    def render(self, screen, x_offset, y_offset):
        screen.blit(self.img, (self.rect.x - x_offset, self.rect.y - y_offset))

    def loop(self, objects):
        self.y_vel += self.fall_speed
        self.y_vel = min(10, self.y_vel)
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
        self.x_vel += 4

    def move_right(self):
        self.x_vel -= 4

    def jump(self):
        if self.jump_count == 0:
            self.jump_count += 1
            self.y_vel = -5

import pygame
from tool import Tool
from keylistener import *
from screen import *

class Entity(pygame.sprite.Sprite) :

    def __init__(self, keylistener : Keylistener, screen : Screen) -> None:
        super().__init__()
        self.screen = screen
        self.spritesheet = pygame.image.load("assets/caracters/main_caracter.png")
        self.image = Tool.split_image(self.spritesheet, 0, 0, 64, 64)
        self.position_x = 10 
        self.position_y = 10
        self.rect = pygame.Rect(0, 0, 192, 192)
        self.keylistener = keylistener
        self.all_images = self.get_all_images()
        self.index_image = 0
        self.animation_step_time = 0.0
        self.action_animation = 60
    
    def update(self):
        self.rect.topleft = [self.position_x, self.position_y]

    def move_left(self):
        self.position_x -= 4
        self.image = self.all_images["left"][self.index_image]

    def move_right(self):
        self.position_x += 4
        self.image = self.all_images["right"][self.index_image]

    def move_up(self):
        self.position_y -= 4
        self.image = self.all_images["up"][self.index_image]

    def move_down(self):
        self.position_y += 4
        self.image = self.all_images["down"][self.index_image]

    def get_all_images(self):
        all_images = {
            "up": [],
            "left": [],
            "down": [],
            "right": []
        }
        for i in range(10):
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(self.spritesheet, i * 64, j*64, 64, 64))
        return all_images
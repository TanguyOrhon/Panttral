import pygame
import json
import base64
import io

from .keylistener import *
from .screen import *

class Entity(pygame.sprite.Sprite) :

    def __init__(self, data_received, keylistener : Keylistener) -> None:
        super().__init__()
        self.spritesheet = pygame.image.load("assets/caracters/main_caracter.png")
        self.image = self.get_sprite_surface
        self.position_x = data_received[0]["content"]["position_x"]
        self.position_y = data_received[0]["content"]["position_y"]
        self.rect = pygame.Rect(0, 0, 192, 192)
        self.keylistener = keylistener
        self.all_images = self.get_all_images()
        self.index_image = 0
        self.animation_step_time = 0.0
        self.action_animation = 60
    
    def update(self):
        self.image = self.get_sprite_surface()
        self.rect.topleft = [self.position_x, self.position_y]

    def get_sprite_surface(self) -> pygame.surface:
        # Lire le fichier JSON
        with open('game/data_json/data_received.json', 'r') as json_file:
            json_data = json.load(json_file)
            json_file.close()

        # Décoder les données base64
        data_base64 = json_data[0]["content"]["surface"]
        data = base64.b64decode(data_base64)

        # Reconstruction de la surface
        buffer = io.BytesIO(data)
        buffer.seek(0)
        sprite_surface = pygame.image.load(buffer)
        return sprite_surface
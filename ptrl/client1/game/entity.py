import pygame
import json
import base64

from .keylistener import *
from .screen import *
from .settings import *

class Entity(pygame.sprite.Sprite) :

    def __init__(self, keylistener : Keylistener) -> None:
        super().__init__()
        self.json_data_get = JSON_DATA_GET
        self.json_data_set = JSON_DATA_SET
        self.name = self.json_data_get[PLAYER]["content"]["name"]
        self.position_x = self.json_data_get[PLAYER]["content"]["position_x"]
        self.position_y = self.json_data_get[PLAYER]["content"]["position_y"]
        self.image = self.get_sprite_surface
        self.rect = pygame.Rect(0, 0, 192, 192)
        self.keylistener = keylistener
        self.index_image = 0
        self.animation_step_time = 0.0
        self.action_animation = 60
    
    def update(self):
        self.rect.topleft = [self.position_x, self.position_y]
        self.keylistener.update()
        self.update_data()

    def get_json_data(self):
        # Lire le fichier JSON
        try:
            with open('game/data_json/data_get.json', 'r') as f:
                self.json_data_get = json.load(f)
        except:
            pass

    
    def get_sprite_surface(self):
        # Décoder les données base64
        data_base64 = self.json_data_get[PLAYER]["content"]["surface"].encode('utf-8')
        data = base64.b64decode(data_base64)
        self.image = pygame.image.frombytes(data, (64,64), 'RGBA')

    def get_position(self):
        # Décoder les données base64
        self.position_x = self.json_data_get[PLAYER]["content"]["position_x"]
        self.position_y = self.json_data_get[PLAYER]["content"]["position_y"]

    def update_data(self):
         self.get_json_data()
         self.get_sprite_surface()
         self.get_position()
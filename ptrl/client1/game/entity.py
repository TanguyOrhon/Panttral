import pygame
import json
import base64

from .keylistener import *
from .screen import *
from .settings import *

class Entity(pygame.sprite.Sprite) :

    def __init__(self, id_ : int, getted, setted, ent_type) -> None:
        super().__init__()
        self.json_data_get = None
        self.json_data_set = None
        self.ent_type = ent_type  
        self.id = id_
        self.get_json_data(getted, setted)

        # self.name = self.json_data_get[f"player_{self.id}"]["content"]["name"]
        self.position_x = self.json_data_get["content"]["position_x"]
        self.position_y = self.json_data_get["content"]["position_y"]
        self.image = self.get_sprite_surface
        self.rect = pygame.Rect(0, 0, 192, 192)
        self.index_image = 0
        self.animation_step_time = 0.0
        self.action_animation = 60
    
    
    def get_json_data(self, getted, setted):
        self.json_data_get = getted[self.ent_type][f"player_{self.id}"]
        self.json_data_set = setted
    
    def get_position(self):
        # Décoder les données base64
        self.position_x = self.json_data_get["content"]["position_x"]
        self.position_y = self.json_data_get["content"]["position_y"]

    def get_sprite_surface(self):
        # Décoder les données base64
        data_base64 = self.json_data_get["content"]["surface"].encode('utf-8')
        data = base64.b64decode(data_base64)
        self.image = pygame.image.frombytes(data, (64,64), 'RGBA')

    def update(self):
        self.rect.topleft = [self.position_x, self.position_y]
        self.update_data()

    def update_data(self):
         self.get_sprite_surface()
         self.get_position()
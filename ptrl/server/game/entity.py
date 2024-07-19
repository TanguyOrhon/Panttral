import pygame
import base64
import json
import io

from .tool import *
from .keylistener import *
import json


class Entity(pygame.sprite.Sprite) :

    def __init__(self, keylistener : Keylistener) -> None:
        super().__init__()
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
        self.filepath = "game/data_json/data_serv.json"
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data_received = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erreur de décodage JSON dans le fichier {self.filepath}: {e}")
        except IOError as e:
            raise IOError(f"Erreur de lecture du fichier {self.filepath}: {e}")
    
    def update(self):
        self.rect.topleft = [self.position_x, self.position_y]
        self.update_json()

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
    
    def update_json(self):
        self.data_received[0]["content"]["position_x"] = self.position_x
        self.data_received[0]["content"]["position_x"] = self.position_y
        self.data_received[0]["content"]["surface"] = self.save_sprite_surface()
        with open(self.filepath, 'w', encoding='utf-8') as data_player:
            json.dump(self.data_received, data_player, ensure_ascii=False, indent=4)

    def save_sprite_surface(self) -> str:
        buffer = io.BytesIO()
        pygame.image.save(self.image, buffer)
        buffer.seek(0)
        data = buffer.read()

        # Encoder les données en base64
        data_base64 = base64.b64encode(data).decode('utf-8')
        return data_base64
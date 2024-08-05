import pygame
import json
import base64
import time

from .tool import *
from .keylistener import *
from .settings import *

# Assuming JSON_DATA_SET is a global dictionary containing player data
JSON_DATA_SET = {
    "Players": {}
}

class Entity(pygame.sprite.Sprite):

    def __init__(self, id_: int) -> None:
        super().__init__()
        self.json_data_get = None
        self.json_data_set = JSON_DATA_SET["Players"]
        self.id = id_
        self.spritesheet = pygame.image.load("assets/caracters/main_caracter.png")
        self.position_x = 10 
        self.position_y = 10
        self.rect = pygame.Rect(0, 0, 192, 192)
        self.all_images = self.get_all_images()
        self.index_image = 0
        self.image = self.all_images["right"][self.index_image]
        self.animation_step_time = 0.0
        self.action_animation = 60
        # Ensure JSON data is created during initialization
        self.create_json_data()
    
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
                all_images[key].append(Tool.split_image(self.spritesheet, i * 64, j * 64, 64, 64))
        return all_images

    def save_sprite_surface(self) -> str:
        image_string = pygame.image.tostring(self.image, 'RGBA')
        image_base64 = base64.b64encode(image_string).decode('utf-8')
        return image_base64

    def update_json(self):
        # Update JSON data with current entity state
        self.json_data_set["content"]["position_x"] = self.position_x
        self.json_data_set["content"]["position_y"] = self.position_y
        self.json_data_set["content"]["surface"] = self.save_sprite_surface()

    def create_json_data(self):
        # Ensure the player data structure is initialized correctly
        player_key = f"player_{self.id}"

        # Check if the player is already in the JSON_DATA_SET
        if player_key not in self.json_data_set:
            # Initialize player data with default values
            self.json_data_set[player_key] = {
                "content": {
                    "position_x": self.position_x,
                    "position_y": self.position_y,
                    "surface": self.save_sprite_surface()
                }
            }
            # Write the updated JSON_DATA_SET to the file
            try:
                with open('game/data_json/data_set.json', 'r+', encoding='utf-8') as f:
                    # Load existing data from the file
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        print("zeiuhf")
                        existing_data = {"Players": {}}

                    # Update existing data with new player data
                    existing_data["Players"].update(self.json_data_set)

                    # Move the file cursor to the start and write the updated data
                    f.seek(0)
                    json.dump(existing_data, f, indent=4)
                    f.truncate()
            except Exception as e:
                print(f"An error occurred while updating the JSON file: {e}")

        # Set self.json_data_set to reference the specific player's data
        self.json_data_set = self.json_data_set[player_key]

    def get_json_data(self, data):
        player_key = f"player_{self.id}"

        # Wait until the player data is available in the JSON structure
        while player_key not in data["Players"]:
            time.sleep(0.1)

        self.json_data_get = data["Players"][player_key]


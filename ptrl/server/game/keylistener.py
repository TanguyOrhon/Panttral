import json
from typing import List
import pygame

class Keylistener:
    def __init__(self) -> None:
        self.keys = self.get_keys()

    def key_pressed(self, key):
        return key in self.keys
    
    def get_keys(self) -> List[int]:
        keys = self.get_keys()
        try:
            with open('game/data_json/data_get.json', 'r') as json_file:
                json_data = json.load(json_file)
                keys = json_data["Player_1"]["content"]["keys"]
        except:
            pass
        
        return keys
    
    def update(self):
        self.keys = self.get_keys()
    
    def clear(self) -> None:
        self.keys.clear()
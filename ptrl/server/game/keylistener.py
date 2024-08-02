import json
from typing import List
import pygame
from .settings import *

class Keylistener:
    def __init__(self) -> None:
        self.keys = self.get_keys()

    def key_pressed(self, key):
        return key in self.keys
    
    def get_keys(self) -> List[int]:

        keys = JSON_DATA_GET["Player_2"]["content"]["keys"]
        return keys
    
    def update(self):
        self.keys = self.get_keys()
    
    def clear(self) -> None:
        self.keys.clear()
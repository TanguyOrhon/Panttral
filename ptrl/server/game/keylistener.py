import json
from typing import List
import pygame
from .settings import *

class Keylistener:
    def __init__(self) -> None:
        self.keys = []

    def key_pressed(self, key):
        return key in self.keys
    
    def get_keys(self, data_get):
        self.keys = data_get["content"]["keys"]
        print(self.keys)
    
    def clear(self) -> None:
        self.keys.clear()
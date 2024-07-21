import pygame
import json
from .settings import *
from .entity import *
from .switch import *
from .keylistener import *
from .screen import *


class Player(Entity):
    def __init__(self, keylistener: Keylistener, screen: Screen) -> None:
        super().__init__(keylistener)
        self.switch = [Switch]
        self.screen = screen
    
    def update(self):
        super().update()
        
    def add_switch(self, switches : list[Switch]):
        self.switch = switches
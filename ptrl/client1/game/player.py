import pygame
import json
from .settings import *
from .entity import *
from .switch import *
from .keylistener import *
from .screen import *


class Player(Entity):
    def __init__(self, screen: Screen, id_, getted, setted) -> None:
        super().__init__(id_, getted, setted, "Players")
        self.switch = [Switch]
        self.screen = screen
    
    def update(self):
        super().update()
        
    def add_switch(self, switches : list[Switch]):
        self.switch = switches
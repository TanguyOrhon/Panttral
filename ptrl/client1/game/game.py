import pygame
import json
from .settings import *
from .player import *
from .screen import *
from .maps import *
from .entity import *
from .keylistener import *

class Game:
    def __init__(self) -> None:
        self.running = True
        self.screen = Screen()
        self.map = Maps(self.screen)
        self.keylistener = Keylistener()
        self.player : Player = Player(self.keylistener, self.screen)
        self.map.add_player(self.player)


    def run(self) -> None:
        while self.running :
            self.handle_input()
            self.map.update()
            self.screen.udpdate()

    def handle_input(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    self.keylistener.add_key(event.key)
                case pygame.KEYUP:
                    self.keylistener.remove_key(event.key)
                case _:
                    pass
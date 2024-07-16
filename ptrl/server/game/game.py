import pygame

from .settings import *
from .player import *
from .maps import *
from .entity import *
from .keylistener import *

class Game:
    def __init__(self) -> None:
        self.running = True
        # self.map = Maps()
        # self.keylistener = Keylistener()
        # self.player : Player = Player(self.keylistener, self.screen)
        # self.map.add_player(self.player)


    def run(self) -> None:
        while self.running :
            self.handle_input()
            self.map.update()
            self.screen.udpdate()
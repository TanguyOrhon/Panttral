import pygame


from .player import *
from .entity import *
from .keylistener import *

class Game:
    def __init__(self) -> None:
        self.running = True
        self.keylistener = Keylistener()
        self.player : Player = Player(self.keylistener)

    def run(self) -> None:
        while self.running :
            self.keylistener.update()
            self.player.update()


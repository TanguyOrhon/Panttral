import pygame
from settings import *
from screen import *
from map import *

class Game:
    def __init__(self) -> None:
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)

    def run(self) -> None:
        while self.running :
            self.map.update()
            self.screen.udpdate()
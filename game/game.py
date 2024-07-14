import pygame
from settings import *
from screen import *
from map import *
from entity import *
from keylistener import *
import player

class Game:
    def __init__(self) -> None:
        self.running = True
        self.screen = Screen()
        self.map = Map(self.screen)
        self.keylistener = Keylistener()
        self.player : player.Player = player.Player(self.keylistener, self.screen)
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
                    pygame.quit()
                case pygame.KEYDOWN:
                    self.keylistener.add_key(event.key)
                case pygame.KEYUP:
                    self.keylistener.remove_key(event.key)
                case _:
                    pass
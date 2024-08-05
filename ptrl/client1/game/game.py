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
        self.json_data_get = JSON_DATA_GET
        self.json_data_set = JSON_DATA_SET
        self.screen = Screen()
        self.map = Maps(self.screen)
        self.keylistener = Keylistener()
        self.player : Player = Player(self.screen, 1, self.json_data_get, self.json_data_set)
        self.map.add_player(self.player)


    def run(self) -> None:
        while self.running :
            self.handle_input()
            self.player.get_json_data(self.json_data_get, self.json_data_set)
            self.map.update()
            self.screen.udpdate()
            self.update_json()

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

    def update_json(self):
        self.json_data_set["content"]["keys"] = self.keylistener.keys
        try :
            with open('game/data_json/data_set.json', 'r+', encoding='utf-8') as f:
                f.seek(0)
                json.dump(self.json_data_set, f, indent=4)
                f.truncate()
        except:
            pass
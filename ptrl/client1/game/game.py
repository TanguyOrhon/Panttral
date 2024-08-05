import pygame
import json
from threading import Lock
from .settings import JSON_DATA_SET
from .player import Player
from .screen import Screen
from .maps import Maps
from .entity import Entity
from .keylistener import Keylistener

class Game:
    def __init__(self) -> None:
        """
        Initialize the game components and data.
        """
        self.running = True
        self.json_data_get = {}
        self.json_data_set = JSON_DATA_SET
        self.file_lock = Lock()  # Lock for thread-safe file access
        self.update_data_get()

        # Initialize game components
        self.screen = Screen()
        self.map = Maps(self.screen)
        self.keylistener = Keylistener()
        self.player: Player = Player(self.screen, 1, self.json_data_get, self.json_data_set)
        self.map.add_player(self.player)

    def run(self) -> None:
        """
        Main game loop to handle input, update game state, and render the screen.
        """
        while self.running:
            self.handle_input()
            self.player.get_json_data(self.json_data_get, self.json_data_set)
            self.map.update()
            self.screen.update()
            self.update_json()

    def handle_input(self) -> None:
        """
        Process input events from the user.
        """
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

    def update_json(self) -> None:
        """
        Update the JSON data set with the current game state and save it to a file.
        """
        self.json_data_set["content"]["keys"] = self.keylistener.keys
        try:
            with self.file_lock:
                with open('game/data_json/data_set.json', 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    json.dump(self.json_data_set, f, indent=4)
                    f.truncate()
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error updating JSON data set: {e}")

    def update_data_get(self) -> None:
        """
        Load the latest game state from the JSON data get file.
        """
        try:
            with self.file_lock:
                with open('game/data_json/data_get.json', 'r', encoding='utf-8') as f:
                    self.json_data_get = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading data get: {e}")

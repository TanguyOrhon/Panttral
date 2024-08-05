import pygame
import json
from .player import Player
from .entity import Entity
from .keylistener import Keylistener
from threading import Lock


class Game:
    def __init__(self) -> None:
        """
        Initialize the game with necessary components and data structures.
        """
        self.running = True
        self.json_data_get = {}  # Initialize as an empty dictionary
        self.json_data_set = {}  # Initialize as an empty dictionary
        self.keylistener = Keylistener()
        self.players = {}
        self.file_lock = Lock()  # Lock for thread-safe file access

    def run(self) -> None:
        """
        Main game loop that updates game state and player data.
        """
        while self.running:
            self.update_data_get()
            self.update_nb_players()
            for player in self.players.values():
                player.get_json_data(self.json_data_get)
                player.update()
            self.update_data_set()

    def update_data_set(self) -> None:
        """
        Update the JSON data set file with the current state of the game.
        """
        self.update_json_data_set()
        try:
            with self.file_lock:
                with open('game/data_json/data_set.json', 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    json.dump(self.json_data_set, f, indent=4)
                    f.truncate()
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error updating data set: {e}")

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

    def update_nb_players(self) -> None:
        """
        Update the number of active players based on the settings file.
        """
        try:
            with self.file_lock:
                with open('game/data_json/settings.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    active_players = data.get("active_players", [])

                    # Add new players
                    print(len(self.json_data_get["Players"]))
                    if len(active_players) != len(self.json_data_get["Players"]):
                        for player_id in active_players:
                            if f"player_{player_id}" not in self.players:
                                self.players[f"player_{player_id}"] = Player(self.keylistener, id_=player_id)
                                print(f"New connection : player_{player_id}")

                        # Remove inactive players
                        self.players = {key: p for key, p in self.players.items() if p.id in active_players}
                        self.json_data_get["Players"] = self.players
                        print(self.json_data_get["Players"])

        except (IOError, json.JSONDecodeError) as e:
            print(f"Error updating number of players: {e}")

    def update_json_data_set(self) -> None:
        """
        Compile and update the JSON data set with current player data.
        """
        data_players = {}
        for p in self.players.values():
            data_players[f"player_{p.id}"] = p.json_data_set
        self.json_data_set["Players"] = data_players

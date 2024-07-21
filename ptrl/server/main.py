import threading
import pygame
from communication.server import Server
from game.game import Game
import time

def start_game():
    pygame.init()
    main_game = Game()
    main_game.run()

def start_server():
    main_server = Server()
    main_server.start()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Wait for a short while to ensure the server has time to start
    time.sleep(2)

    game_thread = threading.Thread(target=start_game)
    game_thread.start()

    game_thread.join()
    server_thread.join()

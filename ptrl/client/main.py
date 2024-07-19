import threading
import pygame
from communication.client import Client
from game.game import Game
import time

# def start_game():
#     pygame.init()
#     main_game = Game()
#     main_game.run()

def connect_client():
    main_client = Client()
    connected = False
    while not connected:
        try:
            main_client.connection()
            connected = True
        except ConnectionError:
            print("Retrying connection...")
            time.sleep(1)

if __name__ == "__main__":

    client_thread = threading.Thread(target=connect_client)
    client_thread.start()

    # Wait for a short while to ensure the client has time to start
    time.sleep(2)

    # game_thread = threading.Thread(target=start_game)
    # game_thread.start()

    # game_thread.join()
    client_thread.join()
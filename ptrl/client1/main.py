import threading
import pygame
import time
from communication.client import Client
from game.game import Game
from game import settings

def main():
    
    name = input("Player : ")
    settings.PLAYER = name
    main_client = Client()

    client_thread = threading.Thread(target=connect_client, args=(main_client,))
    client_thread.start()

    # Wait for a short while to ensure the client has time to start
    time.sleep(2)
    game_thread = threading.Thread(target=start_game, args=(main_client,))
    game_thread.start()

    game_thread.join()
    client_thread.join()
    
    print("All threads have been closed.")

def start_game(main_client):
    pygame.init()
    main_game = Game()
    main_game.run()
    main_client.stop_connection = True


def connect_client(main_client):
    connected = False
    while not connected:
        try:
            main_client.connection()
            connected = True
        except ConnectionError:
            print("Retrying connection...")
            time.sleep(1)
    

if __name__ == "__main__":
    main()
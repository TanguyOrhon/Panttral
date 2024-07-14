import threading
import pygame
import server.server as server
import client.client as client
import game
import time

def start_game():
    pygame.init()
    main_game = game.Game()
    main_game.run()

def start_server():
    main_server = server.Server()
    main_server.start()
    main_client = client.Client()
    main_client.connection()

def connect_client():
    main_client = client.Client()
    connected = False
    while not connected:
        try:
            main_client.connection()
            connected = True
            print("Client connected")
        except ConnectionError:
            print("Retrying connection...")
            time.sleep(1)

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Wait for a short while to ensure the server has time to start
    time.sleep(2)

    client_thread = threading.Thread(target=connect_client)
    client_thread.start()

    game_thread = threading.Thread(target=start_game)
    game_thread.start()
    
    game_thread.join()
    client_thread.join()
    server_thread.join()

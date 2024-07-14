import threading
import pygame
import server.server as server
import game

def start_game():
    pygame.init()
    main_game = game.Game()
    main_game.run()

def start_server():
    main_server = server.Server()
    main_server.start()

if __name__ == "__main__":
    game_thread = threading.Thread(target=start_game)
    server_thread = threading.Thread(target=start_server)

    game_thread.start()
    server_thread.start()

    game_thread.join()
    server_thread.join()

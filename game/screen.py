import pygame
from settings import *

class Screen:

    def __init__(self) -> None:
        self.display = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.framerate = FPS


    def udpdate(self) -> None:
        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.framerate)
        self.display.fill((0,0,0))

    def get_size(self):
        return self.display.get_size()
    
    def get_display(self):
        return self.display
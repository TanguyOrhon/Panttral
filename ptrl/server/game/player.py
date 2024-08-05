import pygame
import json

from .entity import *
from .keylistener import *


class Player(Entity):
    def __init__(self, keylistener : Keylistener, id_ : int) -> None:
        super().__init__(id_)
        self.keylistener = keylistener
    
    def update(self):
        print("test")
        self.keylistener.get_keys(self.json_data_get)
        self.check_move()
        super().update()

    def check_move(self):
        # self.animation_step_time += self.screen.get_delta_time()
        # if self.animation_step_time >= self.action_animation:
        if self.keylistener.key_pressed(pygame.K_z):
            self.move_up()
        if self.keylistener.key_pressed(pygame.K_s):
            self.move_down()
        if self.keylistener.key_pressed(pygame.K_q):
            self.move_left()
        if self.keylistener.key_pressed(pygame.K_d):
            self.move_right()
        if self.index_image < 8 :
            self.index_image += 1
        else :
            self.index_image = 0
        self.animation_step_time = 0.0
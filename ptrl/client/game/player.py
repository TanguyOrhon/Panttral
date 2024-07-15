import pygame
import json
from .settings import *
from .entity import *
from .switch import *
from .keylistener import *
from .screen import *


class Player(Entity):
    def __init__(self, data_received, keylistener: Keylistener, screen: Screen) -> None:
        super().__init__(data_received, keylistener)
        self.name = data_received[0]["content"]["name"]
        self.switch = [Switch]
        self.screen = screen
    
    def update(self):
        self.check_move()
        super().update()

    def check_move(self):
        self.animation_step_time += self.screen.get_delta_time()
        if self.animation_step_time >= self.action_animation:
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
        
    def add_switch(self, switches : list[Switch]):
        self.switch = switches
import pygame
import pyscroll
import pytmx

from .screen import *
from .switch import *
from .player import *

class Maps :
    def __init__(self, screen : Screen) -> None:
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.player = None
        self.switchs = [Switch]
        self.switch_map("Test_map")

    def switch_map(self, map : str) -> None:
        self.tmx_data = pytmx.load_pygame(f"assets/map/{map}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        # self.map_layer.zoom = 2
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=5)
        self.switchs = []

        for obj in self.tmx_data.objects:
            if obj.properties["Type"] == "switch":
                self.switchs.append(Switch(obj.properties["Type"], obj.name, pygame.Rect(obj.x, obj.y, obj.width, obj.height), obj.properties["Port"]))



    def update(self):
        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

    def add_player(self, player : Player):
        self.group.add(player)
        self.player = player
        self.player.add_switch(self.switchs)

import pygame
import pyscroll
import pytmx

from screen import *

class Map :
    def __init__(self, screen : Screen) -> None:
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None

        self.switch_map("Test_map")

    def switch_map(self, map : str) -> None:
        self.tmx_data = pytmx.load_pygame(f"assets/map/{map}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

    def update(self):
        self.group.draw(self.screen.get_display())

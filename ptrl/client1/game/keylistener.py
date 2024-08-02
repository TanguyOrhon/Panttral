import json
from .settings import *
class Keylistener:
    def __init__(self) -> None:
        self.keys = []
        self.json_data_get = JSON_DATA_GET
        self.json_data_set = JSON_DATA_SET

    def add_key(self, key):
        if key not in self.keys:
            self.keys.append(key)
    
    def remove_key(self, key):
        if key in self.keys:
            self.keys.remove(key)

    def key_pressed(self, key):
        return key in self.keys
    
    def clear(self) -> None:
        self.keys.clear()
    
    def update(self):
        self.json_data_set["Player"]["content"]["keys"] = self.keys
        try :
            with open('game/data_json/data_set.json', 'r+', encoding='utf-8') as f:
                f.seek(0)
                json.dump(self.json_data_set, f, indent=4)
                f.truncate()
        except:
            pass

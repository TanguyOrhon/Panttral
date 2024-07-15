class Keylistener:
    def __init__(self) -> None:
        self.keys = []

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
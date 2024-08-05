import json
TITLE = "Panttral"
PLAYER = "player_1"
WIDTH = 1280
HEIGHT = 720
FPS = 60
JSON_DATA_GET = None
JSON_DATA_SET = None
try:
    with open("game/data_json/data_get.json", 'r', encoding='utf-8') as f:
        JSON_DATA_GET = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError(f"Erreur de décodage JSON dans le fichier {"game/data_json/data_get.json"}: {e}")
except IOError as e:
    raise IOError(f"Erreur de lecture du fichier {"game/data_json/data_get.json"}: {e}")

try:
    with open("game/data_json/data_set.json", 'r', encoding='utf-8') as f:
        JSON_DATA_SET = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError(f"Erreur de décodage JSON dans le fichier {"game/data_json/data_set.json"}: {e}")
except IOError as e:
    raise IOError(f"Erreur de lecture du fichier {"game/data_json/data_set.json"}: {e}")
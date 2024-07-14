import sqlite3
from entity import *
from map import Map
from keylistener import *
from screen import *

def create_table_player(entity : Entity):
    conn = sqlite3.connect("Pantral.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Player (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
                )""")
    # cur.execute("""INSERT INTO Player (name)
    #             VALUES (?) """, entity.name)
    cur.execute("""INSERT INTO Player (name)
                VALUES (?) """, (entity.name,))
    conn.commit()
    conn.close()

screen = Screen()
map = Map(screen)
keylistener = Keylistener()
entity = Entity(keylistener, screen)
create_table_player(entity)
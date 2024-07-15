import sqlite3
from entity import *
from .maps import *
from .keylistener import *


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

keylistener = Keylistener()
entity = Entity(keylistener)
create_table_player(entity)
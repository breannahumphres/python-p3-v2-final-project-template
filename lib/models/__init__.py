import sqlite3
from models.characters import Character
from models.items import Item

CONN = sqlite3.connect('game.db')
CURSOR = CONN.cursor()


CURSOR.execute('''CREATE TABLE IF NOT EXISTS characters (
               id INTEGER PRIMARY KEY, 
               name TEXT,
               health_points INTEGER DEFAULT 100,
               gold_coins INTEGER DEFAULT 100)''');

CONN.commit()

CURSOR.execute('''CREATE TABLE IF NOT EXISTS items (
               id INTEGER PRIMARY KEY,
               item_name TEXT NOT NULL,
               item_type TEXT NOT NULL,
               value INTEGER NOT NULL,
               character_id INTEGER, 
               FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE )''')
CONN.commit()


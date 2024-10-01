import sqlite3

CONN=sqlite3.connect('game.db')
CURSOR = CONN.cursor()

class Item():

    def __init__(self, item_name, item_type, value, id=None):
        self.id = id
        self.item_name = item_name
        self.item_type = item_type
        self.value = value

    def __repr__(self): 
        return f"{self.item_name} ({self.item_type})"
    
    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM items')
        items_rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[3], row[0]) for row in items_rows]
    
    @classmethod
    def find_by_id(cls, item_id):
        CURSOR.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item_row = CURSOR.fetchone()
        if item_row:
            return cls(item_row[1], item_row[2], item_row[3], item_row[0])
        return None
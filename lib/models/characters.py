from .items import Item
import sqlite3

CONN = sqlite3.connect('game.db')
CURSOR = CONN.cursor()


class Character():


    def __init__(self, name, health_points = 100, gold_coins = 100, id=None):
        self.id = id
        self.name = name
        self.health_points = health_points
        self.gold_coins = gold_coins
        self.inventory = []
        self.current_weapon = Item("Stick", "Weapon", 5)
    
    def save(self):
        if self.id is None:
            CURSOR.execute('''INSERT INTO characters (name, health_points, gold_coins)
                            VALUES (?, ?, ?)''', (self.name, self.health_points, self.gold_coins))
            CONN.commit()
            self.id = CURSOR.lastrowid
            self.gain_item(self.current_weapon)
        else: 
            CURSOR.execute('''UPDATE characters SET health_points = ?, gold_coins = ? WHERE id = ?''', (self.health_points, self.gold_coins, self.id))
            CONN.commit()
    
    def load_inventory(self):
        CURSOR.execute('''SELECT * FROM items WHERE character_id = ?''', (self.id,))
        items_data = CURSOR.fetchall()
        self.inventory = [Item(row[1], row[2], row[3], row[0]) for row in items_data]


    def lose_health(self, amount):
        self.health_points -= amount
        if self.health_points <0:
            self.health_points = 0
        print(f"{self.name} has lost {amount} health points. Current HP: {self.health_points}")

    def gain_health(self,amount):
        self.health_points += amount
        print(f"{self.name} has gained {amount} health points. Current HP: {self.health_points}")
    
    def lose_coins(self,amount): 
        self.gold_coins -= amount
        if self.gold_coins < 0:
            self.gold_coins = 0
        print(f"{self.name} has lost {amount} gold coins. Current gold coins: {self.gold_coins}")
    
    def gain_coins(self,amount):
        self.gold_coins += amount
        print(f"{self.name} has gained {amount} gold coins. Current gold coins: {self.gold_coins}")

    def gain_item(self,item):
        self.inventory.append(item)
        CURSOR.execute('''INSERT INTO items (item_name, item_type, value, character_id)
                           VALUES (?,?,?,?)''', (item.item_name, item.item_type, item.value, self.id))
        CONN.commit()
    def lose_item(self, item_name):
        item = next((i for i in self.inventory if i.item_name == item_name), None)
        if item:
           self.inventory.remove(item)
           CURSOR.execute('DELETE FROM items WHERE item_name = ? AND character_id = ?', (item_name, self.id))
           CONN.commit()
           print(f"{item_name} removed from inventory.")
        else: 
            print(f"{item_name} removed from inventory")
    def use_food(self, food_name):
        food_item = next((i for i in self.inventory if i.item_name == food_name and i.item_type == "Food"), None)
        if food_item:
            self.health_points += food_item.value
            self.inventory.remove(food_item)
            CURSOR.execute('DELETE FROM items WHERE item_name = ? AND character_id = ?', (food_item.item_name, self.id))
            CONN.commit()
            print(f"Used {food_item.item_name}, restored {food_item.value} health points. Current HP: {self.health_points}")
        else:
            print(f"{food_name} not found in inventory")
    def check_inventory(self):
        print(f"{self.name}'s Stats:")
        print(f"Health Points: {self.health_points}")
        print(f"Gold Coins: {self.gold_coins}")
        print(f"{self.name}'s Inventory:")
        food_items = [item for item in self.inventory if item.item_type == "Food"]
        for index, item in enumerate(self.inventory):
            print(f"{index + 1}. {item.item_name} ({item.item_type}), Value: {item.value}")
        if food_items:
            print("Would you like to eat some food to restore health?")
            choice = input("Enter the number of the food to ear, or press Enter to skip: ")

            if choice.isdigit():
                item_index = int(choice) - 1
                if 0 <= item_index < len(self.inventory) and self.inventory[item_index].item_type == "Food":
                   food_item = self.inventory[item_index]
                   self.use_food(food_item.item_name)
                else:
                    print("Invalid choice or the selected item is not food.")

    def equip_best_weapon(self):
        weapons = [item for item in self.inventory if item.item_type == "Weapon"]

        if weapons:
            best_weapon = max(weapons, key=lambda weapon: weapon.value)
            self.current_weapon = best_weapon
            
class Item():

    def __init__(self, item_name, item_type, value):
        self.item_name = item_name
        self.item_type = item_type
        self.value = value

    def __repr__(self): 
        return f"{self.item_name} ({self.item_type})"
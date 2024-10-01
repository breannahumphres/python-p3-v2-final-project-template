# lib/cli.py
from models.characters import Character
from models.items import Item
import sqlite3

CONN = sqlite3.connect('game.db')
CURSOR = CONN.cursor()

from helpers import (
    exit_program
)
story_progress = 0
player = None

def main():
    global player
    print("~Welcome to The Journey Never Ends Adventure Game!~")
    print("\n------------------------------")
    print("You have just awoken in a foggy, mystical forest. You see that your health is at 100, you have 100 gold coins in your pocket, and a sturdy-looking stick beside you that would make a pitiful, but semi-useful weapon. You must have hit your head because you cannot remember much. But you do remember your name. ")

    player_name = input("What is your name?: ")
    player = Character(player_name)
    player.save()
    

    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            check_player_stats()
        elif choice == "2":
            continue_story()
        elif choice == "3":
            restart_game()
        elif choice == "4":
            admin_menu()
        else: 
            print("Invalid Choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Check Player Stats")
    print("2. Continue Story")
    print("3. Restart Game")
    print("4. Admin Menu")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Clear Past Games")
        print("2. List All Characters")
        print("3. Find Character by ID")
        print("4. List All Items")
        print("5. Find Items by ID")
        print("6. go back to menu")

        choice = input(" >")
        if choice == "1":
            clear_past_games()
        elif choice == "2":
            list_all_characters()
        elif choice == "3":
            find_character_by_id()
        elif choice == "4":
            list_all_items()
        elif choice == "5":
            find_item_by_id()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def list_all_characters():
    characters = Character.get_all()
    if characters:
        for character in characters:
            print(f"ID: {character.id}, Name: {character.name}, HP: {character.health_points}, Gold: {character.gold_coins} ")
    else: 
        print("No characters found")
def find_character_by_id():
    character_id = input("Enter character ID: ")
    if character_id.isdigit():
        character = Character.find_by_id(int(character_id))
        if character: 
            print(f"Found: ID: {character_id}, Name: {character.name}, HP: {character.health_points}, Gold, {character.gold_coins}")
        else: 
            print("Character not found.")
    else:
        print("Invalid Input. Please enter a numeric ID")

def list_all_items():
    items = Item.get_all()
    if items:
        for item in items:
            print(f"ID: {item.id}, Name: {item.item_name}, Type: {item.item_type}, Value: {item.value} ")
    else: 
            print("No items found")

def find_item_by_id():
    item_id = input("Enter item ID: ")
    if item_id.isdigit():
        item = Item.find_by_id(int(item_id))
        if item: 
            print(f"Found: ID: {item_id}, Name: {item.item_name}, Type: {item.item_type}, Value, {item.value}")
        else: 
            print("Item not found.")
    else: 
        print("Invalid Input. Expected an integer")

def check_player_stats():
    global player 
    if player:
        player.check_inventory()
        player.health_points
        player.gold_coins
    else:
        print("No player created yet.")
def restart_game():
    global player, story_progress
    player.health_points = 100
    player.gold_coins = 100
    player.inventory = []
    player.current_weapon = Item("Stick", "Weapon", 5)
    print("The game has been restarted!")

def clear_past_games():
    try:
        CURSOR.execute('DELETE FROM characters')
        CURSOR.execute('DELETE FROM items')
        CONN.commit()
        print("Tables cleared successfully.")
    except sqlite3.Error as e:
        print(f"Error clearing tables: {e}")

def continue_story():
    global story_progress
    if story_progress == 0:
        print(f"Well, {player.name}, you are in for a bit of a surprise. There is a human-sized dung beetle heading right towards you. What do you do?")
        print("1. Fight")
        print("2. Flee")
        print("3. Menu")
        choice = input("> ")
        if choice == "1":
            story_progress = 2
            print("You grab your sturdy stick and take a fighting stance against the beetle. It stops and observes you. It starts barreling forward, but you dodge. You turn and start beating the dung beetle to a pulp. It collapses to the ground, dead.")
        elif choice == "2":
            story_progress = 1
            print("You gather yourself and run away. You trip and hit your head, losing 10 HP. The dung beetle is closing in.")
            player.lose_health(10)
            player.save()
        elif choice == "3":
            menu()
            return
        else: print("Invalid Choice")

    elif story_progress == 1:
        print("\n You run away again and have a really bad headache. The dung beetle is closing in on you. It does not seem to be too intelligent. Why not try fighting?")
        print("1. Attempt to flee again")
        print("2. Menu")

        choice = input(" >")
        if choice == "1":
            print("You keep running but fall again. You're really clumsy huh? You lost 10 more health points!")
            player.lose_health(10)
            print("Maybe it's time to fight. Yes, you will fight now! You grab your sturdy stick and take a fighting stance against the beetle. It stops and observes you. It starts barreling forward, but you dodge. You turn and start beating the dung beetle to a pulp. It collapses to the ground, dead.")
            story_progress = 2
            player.save()
        elif choice == "2":
            menu()
            return
        else: print("Invalid Choice")

    elif story_progress == 2:
        print("\nYou have the option to place 10 gold coins on the dung beetle as a tribute to the poor beast or pick up a Loaf of Bread that it dropped worth 10HP.")
        print("1. Place 10 gold coins as a tribute")
        print("2. Take the Loaf of Bread that it dropped")
        print("3. Menu")

        choice = input(" >")
        if choice == "1":
            print("\nYou place 10 gold coins upon the corpse of the beast and it glows. A gold dagger appears. You have appeased the Gods. What Gods? You are not sure, but the gold dagger has been added to your inventory.")
            player.lose_coins(10)
            gold_dagger = Item("Gold Dagger", "Weapon", 20)
            player.gain_item(gold_dagger)
            story_progress = 3
            player.save()
        elif choice == "2":
            print("\n You take the Loaf of Bread worth 10 health points. It has been added to your inventory")
            loaf_of_bread = Item("Loaf of Bread", "Food", 10)
            player.gain_item(loaf_of_bread)
            story_progress = 3
            player.save()
        elif choice == "3":
            menu()
            return
        else: 
            print("Invalid Choice")
    elif story_progress == 3:
        print("\n You wipe your brow and feel a sense of pride for beating the poor dung beetle. You see a clear path through the forest and trek forward. You walk and walk for miles until you see a clearing ahead. The path ends at a field of florals. In the middle of the flower field is a door. Glowing. A faint humming sound coming from it. You open the door and enter.")
        print(f"Through the door, you find what seems to be the inside of a cottage. A beautiful woman with long hair the color of hay sits at a table with two cups with steam coming off of them. She glances over at you and says, '{player.name}, I have been waiting for you. Please, sit. I have made tea.' What do you do?")
        print("1. Sit with her")
        print("2. Draw your weapon")
        print("3. Menu")

        choice = input(" >")
        if choice == "1":
            print(f"You sit down and she smiles at you. Her face seems so familiar to you. '{player.name}, did you have a hard time finding me? I have been waiting for what seems like forever for you to arrive.' You glance around the room and then meet her eyes. 'I do not know how I wound up in the forest, or how long I have been here.. or who you are Miss… I do not remember anything but my name.” Her eyes seem to turn cold. As a matter of fact… the whole room starts to feel cold. You notice goosebumps start to appear on your arm. She smiles. Her teeth are a bit more sharp than a human. In fact, they are more like fangs.")
            story_progress = 4
        elif choice == "2":
            print(f"You draw your weapon immediately. This all feels off to you. 'Who are you and what do you want with me?' you ask. 'I only wish to help' she tries to assure you. She smiles. Her teeth are a bit more sharp than a human. In fact, they are more like fangs. 'Okay, then why are your teeth like that? Fangs that look like they are ready to sink into my neck'. 'Ah, I see. You do not remember me, do you?' You pause.. 'am I supposed to remember you?' 'The High Wizard has done a number on you, {player.name}. Sit, drink tea with me. It will help. My name, Is Evaline. I am your alchemist. Vampire, alchemist. Hence the fangs that want to sink into your neck' She says as she flashes her teeth. You sit down and drink the tea.")
            story_progress = 5
        elif choice == "3":
            menu()
            return
        else: 
            print("Invalid Choice")
    elif story_progress == 4:
        print(f"You sit and hold the mug, but do not drink. You meet her stare. You still feel the familiarity. It pulls you into her eyes, a cerulean sea. You can almost see the stars in them. You blink. 'Who are you? What are you? How do you know me?' She continues to study you intensely. 'My name is Evaline. I am a vampire and an alchemist. Some say our worlds greatest… but that was a long time ago was it not?' It seems like you are supposed to know the answer to this rhetorical question. 'We knew each other. For a long time. Until.. well until the High Wizard got his hands on you. I guess this is the outcome of that… I hate to say I told you so because you just simply wouldn not get it, but… I told you so, {player.name}.' She clicks her tongue. 'It seems as if he has wiped your memory completely and then left you out in the Dung Forest for dead. Drink the tea. It will help. Then we can have a real conversation.'")
        print("1. Drink the tea")
        print("2. Menu")

        choice = input(" >")
        if choice == "1":
            print("You drink the tea finally")
            story_progress = 5
        elif choice == "2":
            menu()
            return
        else: 
            print("Invalid Choice")
    elif story_progress == 5:
        print("\nYou look deep into Evalines eyes. You do not know why, but you trust and believe her. You take the tea and gulp it down. Sweet and bitter at once. Your cheeks feel flushed. Your vision blurs. The room spins. Evaline tilts her head. 'I suppose I should have mentioned the side effects, but consider this payback for being such an ass to me during our last encounter.' You lose consciousness…")
        print(f"You awaken to the sound of humming. You know that song… Evaline hums it whenever she is trying to get under your skin. A song a bard once wrote about you… except you did not leave him a tip so he added in a line about you slipping in horse shit and eating it. She knows you loathe that song. 'Enough' you yell. You sit up and she is sitting on the counter. Staring. Studying as always. You detest when she attempts to read you like a book. Though you suppose you should be thanking her. The High Wizard wiped your mind and you never would have regained your memory if not for her. 'So you do still care for me after all this time, Evaline. Incredibly touching. But I really should be going. High Wizard to defeat and all, ya know? Thanks again, though!' You head towards the door. 'Do you think you could defeat the High Wizard with just that, {player.current_weapon.item_name}?' You pause. A {player.current_weapon.item_name}? Could I? No. Maybe? Hmm. What do you do?")
        print("1. Continue through the door. She practically drugged you!")
        print("2. Hear her out. You could use a better weapon")
        print("3. Menu")

        choice = input(" >")
        if choice == "1":
            print("\nYou head through the door. You drop into nothingness. A black void. You fall forever and ever. Maybe you should have heard her out? Game Over.")
            restart_game()
        elif choice == "2":
            print("You turn towards her. 'What did you have in mind, my dear friend' She smiles slightly and chuckles. 'Head out that door. It will take you about 2 miles outside the walls of the city of Constania. There you will find a blacksmith merchant stand. The blacksmith is a man named Dylan. Tell him I sent you and he will provide you with a weapon that will destroy the High Wizard. Once and for all. Then, you must head to his Palace in the Cerulean City. You must end him. Once and for all.' You see tears falling down her face. You step forward and hug her. 'Thank you, Evaline. For everything. I will never forget what you have done for me' She does not say anything. She simply spins around and heads into the adjacent room, closing the door.")
            story_progress = 6
        elif choice == "3":
            menu()
            return
        else: 
            print("Invalid Choice")
    elif story_progress == 6:
        print("\n You open the door. It is bright and you cannot see well, so you step through. When you are able to see again, you are on a path leaving the forest and can see the city walls in the distance. You start forward on the path and can not help but feel a bit of excitement. You walk for a few minutes. Alone on the quiet path. You hear a stick break in the forest to the left. You turn your head. You do not see anything. You continue on, but you see a string across the path ahead. A simple trap. You stop in your tracks and look around. 'Ahem' someone says behind you. You turn. There you see three large men dressed in black with dull swords pointing at you. You grin. 'How can I help you, gentleman?' 'You know what we want. Just empty your pockets and we will let you go.' What do you do?")
        print("1. Fight")
        print("2. Empty Your Pockets")
        print("3. Menu")

        choice = input(" >")
        if choice == "1": 

            player.equip_best_weapon()

            if player.current_weapon.item_name == "Stick":
                print(f"You draw your weapon. You only have a {player.current_weapon.item_name}. The men quickly take it out of your hands, snap it in half and laugh. They push you over and your head hits a rock, losing 20 Health Points. They steal 20 gold coins from your pocket. 'At least you are brave enough to fight, kid.' They run away. It is time to head into the city.")
                player.lose_coins(20)
                player.lose_health(20)
                player.lose_item("Stick")
                story_progress = 7
                player.save()
            elif player.current_weapon.item_name == "Gold Dagger":
                print(f"You draw your weapon. Thank god you had the common sense to pay tribute after you killed that beast earlier. You easily unarm the thieves with your {player.current_weapon.item_name} and they scurry off into the forest. How easy. It is time to head into the city finally.")
                story_progress = 7
        elif choice == "2":
            print("You empty your pockets and hand over 50 gold coins and your food item. The thieves look at one another. One takes your money. Another one shoves you hard into the ground and you hit your head on a sharp rock, losing 50 health points. They start laughing and scurry into the woods. At least you are alive? It is time to head into the city.")
            player.lose_coins(50)
            player.lose_health(50)
            player.lose_item("Loaf of Bread")
            story_progress = 7
            player.save()
        elif choice == "3":
            menu()
            return
        else: 
            print("Invalid Choice")
    elif story_progress == 7:
        print("\nYou enter through the golden city gates of Constania. It is a bustling, vibrant city. What do you search for first?")
        print("1. The Blacksmith")
        print("2. An Inn to rest")
        print("3. Menu")

        choice = input(" >")
        if choice == "1":
            print("You ask some people for directions and make your way towards the blacksmith merchant. Dylan appears to be a large elf, with a left ear clipped. You wonder what his story is. You approach the merchant.")
            story_progress = 9
        elif choice == "2": 
            print("You quickly find an inn. It costs 20 gold coins, but you will regain 50 Health Points for resting.")
            story_progress = 8
        elif choice == "3":
            menu()
            return
        else: 
            print("Invalid Choice")
    elif story_progress == 8:
        print("You pay for a single room and meal and head upstairs with your soup. You sip it quietly while you reflect on your day. You wish you would have had more time to pester Evaline. It has been such a long time since you have spoken. And you suppose you were kind of an ass to her. The High Wizard has his way of making his plans seem like your own… How were you to know he would betray you and wipe your memory? He is your brother after all… You lie in bed and rest, earning 50 Health Points. You awake feeling rejuvenated and ready to speak with the Blacksmith.")
        player.gain_health(50)
        player.lose_coins(20)
        story_progress = 9
        player.save()
    elif story_progress == 9:
        print(f"You study the merchant as he works towards the back of the shop. Elves can live for centuries. There is no telling what this Blacksmith has experienced. 'Are you going to keep staring at me, or are you going to ask me for what Evaline sent you for, {player.name}?' You stand there stunned. You wonder how he knew who you were. 'Evaline told me you were coming. You are the only one to ever study me in such a way. I assumed it was you, {player.name}. I am Dylan, but I am sure Eva already made sure you knew that. You are lucky, ya know? She cares for you. That is not common in this world lately.' He picks up an old sheathed sword. 'Here, {player.name}. Take it. I do not want this cursed weapon around anymore.' You reach for the sword and it glows cerulean. Puzzlingly. You take the sword and put it on your back. 'Thank you, Dylan. I hope to meet you again and buy you a drink. Until then, goodbye' 'Goodbye, {player.name}. But do not come back until he is dead.' Dylan turns around and walks back towards the back of the shop and starts working again. ")
        cerulean_sword = Item("Cerulean Sword", "Weapon", 100)
        player.gain_item(cerulean_sword)
        player.current_weapon = cerulean_sword
        story_progress = 10
        player.save()
    else: 
        print("\nYou leave the city of Constania with more questions than ever, but you are for certain what your journeys end will be. A fight to the death between you and your own brother, The High Wizard. The journey continues….")
        print("1. Restart")
        print("2. Menu")
        print("3. Exit")

        choice = input(" >")
        if choice == "1":
            restart_game()

        elif choice == "2":
            menu()
            return
        elif choice == "3":
            exit_program()
        else:
            print("Invalid Choice")
    

    


if __name__ == "__main__":
    main()

from gettext import install
import random

import pip

# --- Pokémon Classes ---
class Pokemon:
    def __init__(self, name, level, hp, attack, defense):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_pokemon(self, other):
        damage = max(1, self.attack - other.defense)
        other.take_damage(damage)
        print(f"{self.name} attacks {other.name} for {damage} damage! ({other.hp}/{other.max_hp} HP left)")

# --- Player Class ---
class Player:
    def __init__(self, name):
        self.name = name
        self.pokemons = []
        self.quest_progress = 0

    def catch_pokemon(self, pokemon):
        self.pokemons.append(pokemon)
        print(f"{self.name} caught {pokemon.name}!")

# --- Game Functions ---
def wild_encounter(player):
    wild_list = [
        Pokemon("Chespin", 5, 20, 7, 5),
        Pokemon("Fennekin", 5, 18, 8, 4),
        Pokemon("Froakie", 5, 16, 9, 3)
    ]
    wild = random.choice(wild_list)
    print(f"A wild {wild.name} appeared!")

    action = input("Do you want to [B]attle or [C]atch? ").lower()
    if action == "b":
        battle(player, wild)
    elif action == "c":
        if random.random() < 0.6:
            player.catch_pokemon(wild)
        else:
            print(f"{wild.name} escaped!")

def battle(player, wild):
    if not player.pokemons:
        print("You have no Pokémon to battle with!")
        return

    pokemon = player.pokemons[0]  # Use first Pokémon
    print(f"You send out {pokemon.name}!")

    while pokemon.is_alive() and wild.is_alive():
        pokemon.attack_pokemon(wild)
        if wild.is_alive():
            wild.attack_pokemon(pokemon)

    if pokemon.is_alive():
        print(f"{wild.name} fainted!")
        player.quest_progress += 1
    else:
        print(f"{pokemon.name} fainted!")

def quest_status(player):
    print(f"Quest progress: {player.quest_progress}/3 wild Pokémon defeated")

# --- Main Game Loop ---
def main():
    player_name = input("Enter your name: ")
    player = Player(player_name)

    # Starter Pokémon
    starter = Pokemon("Chespin", 5, 20, 7, 5)
    player.catch_pokemon(starter)

    print("\n--- Welcome to Pokémon Quest! ---\n")

    while player.quest_progress < 3:
        action = input("Do you want to [E]ncounter a wild Pokémon, [Q]uest status, or [E]xit? ").lower()
        if action == "e":
            wild_encounter(player)
        elif action == "q":
            quest_status(player)
        elif action == "exit":
            print("Goodbye!")
            break

    if player.quest_progress >= 3:
        print("Congratulations! You completed your first quest!")

if __name__ == "__main__":
    main()

import random

# --- Type Effectiveness ---
type_chart = {
    ("Fire", "Grass"): 2,
    ("Water", "Fire"): 2,
    ("Grass", "Water"): 2,
}

def get_multiplier(attacker, defender):
    return type_chart.get((attacker, defender), 1)

# --- Pokémon Class ---
class Pokemon:
    def __init__(self, name, ptype, level):
        self.name = name
        self.type = ptype
        self.level = level
        self.max_hp = 20 + level * 2
        self.hp = self.max_hp
        self.attack = 5 + level
        self.defense = 3 + level
        self.exp = 0

    def is_alive(self):
        return self.hp > 0

    def attack_pokemon(self, other):
        multiplier = get_multiplier(self.type, other.type)
        damage = max(1, int((self.attack - other.defense) * multiplier))
        other.hp -= damage
        if other.hp < 0:
            other.hp = 0

        print(f"{self.name} ({self.type}) hits {other.name} for {damage} damage!")
        if multiplier > 1:
            print("It's super effective!")

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= 10:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.max_hp += 5
        self.attack += 2
        self.defense += 1
        self.hp = self.max_hp
        print(f"{self.name} leveled up to {self.level}!")

# --- Player Class ---
class Player:
    def __init__(self, name):
        self.name = name
        self.party = []
        self.pc = []
        self.quests = {
            "defeat": 0,
            "catch": 0
        }

    def add_pokemon(self, pokemon):
        if len(self.party) < 6:
            self.party.append(pokemon)
            print(f"{pokemon.name} added to party!")
        else:
            self.pc.append(pokemon)
            print(f"{pokemon.name} sent to PC!")

    def show_party(self):
        print("\nYour Party:")
        for p in self.party:
            print(f"- {p.name} Lv{p.level} ({p.hp}/{p.max_hp})")

    def show_pc(self):
        print("\nPC Storage:")
        for p in self.pc:
            print(f"- {p.name} Lv{p.level}")

# --- Battle System ---
def battle(player, wild):
    if not player.party:
        print("No Pokémon available!")
        return

    pokemon = player.party[0]
    print(f"\nGo {pokemon.name}!")

    while pokemon.is_alive() and wild.is_alive():
        pokemon.attack_pokemon(wild)
        if wild.is_alive():
            wild.attack_pokemon(pokemon)

    if pokemon.is_alive():
        print(f"{wild.name} fainted!")
        pokemon.gain_exp(5)
        player.quests["defeat"] += 1
    else:
        print(f"{pokemon.name} fainted!")

# --- Wild Encounter ---
def encounter(player):
    wild_choices = [
        Pokemon("Froakie", "Water", random.randint(3, 6)),
        Pokemon("Fennekin", "Fire", random.randint(3, 6)),
        Pokemon("Chespin", "Grass", random.randint(3, 6)),
    ]

    wild = random.choice(wild_choices)
    print(f"\nA wild {wild.name} appeared!")

    action = input("[B]attle or [C]atch? ").lower()

    if action == "b":
        battle(player, wild)

    elif action == "c":
        if random.random() < 0.7:
            print(f"You caught {wild.name}!")
            player.add_pokemon(wild)
            player.quests["catch"] += 1
        else:
            print("Oh no! It escaped!")

# --- Quest System ---
def check_quests(player):
    print("\n--- Quests ---")
    print(f"Defeat 3 Pokémon: {player.quests['defeat']}/3")
    print(f"Catch 2 Pokémon: {player.quests['catch']}/2")

    if player.quests["defeat"] >= 3:
        print("✅ Defeat quest complete! Reward: +1 level to all party Pokémon")
        for p in player.party:
            p.level_up()
        player.quests["defeat"] = 0

    if player.quests["catch"] >= 2:
        print("✅ Catch quest complete! Reward: Heal all Pokémon")
        for p in player.party:
            p.hp = p.max_hp
        player.quests["catch"] = 0

# --- Main Game Loop ---
def main():
    name = input("Enter your trainer name: ")
    player = Player(name)

    # Starter
    starter = Pokemon("Froakie", "Water", 5)
    player.add_pokemon(starter)

    print("\nWelcome to your Pokémon adventure!\n")

    while True:
        print("\n--- Menu ---")
        print("1. Encounter Pokémon")
        print("2. Show Party")
        print("3. Show PC")
        print("4. Check Quests")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            encounter(player)
        elif choice == "2":
            player.show_party()
        elif choice == "3":
            player.show_pc()
        elif choice == "4":
            check_quests(player)
        elif choice == "5":
            print("Goodbye Trainer!")
            break

if __name__ == "__main__":
    main()

import random

# --- Pokemon Class ---
class Pokemon:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.max_hp = 20 + level * 2
        self.hp = self.max_hp

    def __str__(self):
        return f"{self.name} Lv{self.level} ({self.hp}/{self.max_hp})"

# --- PC STORAGE SYSTEM ---
class PC:
    def __init__(self):
        self.boxes = [[] for _ in range(3)]  # 3 boxes

    def add(self, pokemon):
        for box in self.boxes:
            if len(box) < 10:
                box.append(pokemon)
                print(f"{pokemon.name} sent to PC box!")
                return
        print("All PC boxes are full!")

    def show(self):
        print("\n--- PC Storage ---")
        for i, box in enumerate(self.boxes):
            print(f"\nBox {i+1}:")
            if not box:
                print(" (empty)")
            for idx, p in enumerate(box):
                print(f"{idx+1}. {p}")

    def withdraw(self):
        self.show()
        box_num = int(input("Choose box number: ")) - 1
        if box_num < 0 or box_num >= len(self.boxes):
            return None

        box = self.boxes[box_num]
        if not box:
            print("Box empty!")
            return None

        p_index = int(input("Choose Pokémon #: ")) - 1
        if p_index < 0 or p_index >= len(box):
            return None

        return box.pop(p_index)

# --- PLAYER ---
class Player:
    def __init__(self):
        self.party = []
        self.pc = PC()

    def add_pokemon(self, pokemon):
        if len(self.party) < 6:
            self.party.append(pokemon)
            print(f"{pokemon.name} added to party!")
        else:
            self.pc.add(pokemon)

    def show_party(self):
        print("\n--- Your Party ---")
        for i, p in enumerate(self.party):
            print(f"{i+1}. {p}")

    def deposit(self):
        self.show_party()
        if not self.party:
            return

        choice = int(input("Choose Pokémon to deposit: ")) - 1
        if 0 <= choice < len(self.party):
            poke = self.party.pop(choice)
            self.pc.add(poke)

    def withdraw(self):
        if len(self.party) >= 6:
            print("Party full!")
            return
        poke = self.pc.withdraw()
        if poke:
            self.party.append(poke)
            print(f"{poke.name} added to party!")

# --- ENCOUNTERS ---
def encounter(player):
    wild_names = ["Pikachu", "Eevee", "Bunnelby", "Fletchling"]
    wild = Pokemon(random.choice(wild_names), random.randint(3, 6))

    print(f"\nA wild {wild.name} appeared!")

    action = input("[B]attle, [C]atch, [R]un: ").lower()

    if action == "c":
        if random.random() < 0.75:
            print(f"You caught {wild.name}!")
            player.add_pokemon(wild)
        else:
            print("It escaped!")

    elif action == "b":
        battle(player, wild)

def battle(player, wild):
    if not player.party:
        print("No Pokémon!")
        return

    my_pokemon = player.party[0]
    print(f"Go {my_pokemon.name}!")

    while my_pokemon.hp > 0 and wild.hp > 0:
        wild.hp -= 5
        print(f"{my_pokemon.name} hits {wild.name}!")

        if wild.hp <= 0:
            print(f"{wild.name} fainted!")
            return

        my_pokemon.hp -= 3
        print(f"{wild.name} hits back!")

    print(f"{my_pokemon.name} fainted!")

# --- PC MENU ---
def pc_menu(player):
    while True:
        print("\n--- PC Menu ---")
        print("1. View PC")
        print("2. Deposit Pokémon")
        print("3. Withdraw Pokémon")
        print("4. Exit PC")

        choice = input("Choose: ")

        if choice == "1":
            player.pc.show()
        elif choice == "2":
            player.deposit()
        elif choice == "3":
            player.withdraw()
        elif choice == "4":
            break

# --- MAIN GAME ---
def main():
    player = Player()

    # Starter
    player.add_pokemon(Pokemon("Froakie", 5))

    while True:
        print("\n--- Main Menu ---")
        print("1. Encounter")
        print("2. Party")
        print("3. PC")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            encounter(player)
        elif choice == "2":
            player.show_party()
        elif choice == "3":
            pc_menu(player)
        elif choice == "4":
            break

if __name__ == "__main__":
    main()

import random
import json

# --- Pokemon Class ---
class Pokemon:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.max_hp = 20 + level * 2
        self.hp = self.max_hp

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        p = Pokemon(data["name"], data["level"])
        p.hp = data["hp"]
        return p

    def __str__(self):
        return f"{self.name} Lv{self.level}"

# --- PC SYSTEM ---
class PC:
    def __init__(self):
        self.boxes = [[] for _ in range(20)]
        self.names = [f"Box {i+1}" for i in range(20)]

    def add(self, pokemon):
        for box in self.boxes:
            if len(box) < 30:
                box.append(pokemon)
                print(f"{pokemon.name} sent to PC!")
                return
        print("All boxes full!")

    def show_box(self, index):
        print(f"\n--- {self.names[index]} ---")
        box = self.boxes[index]
        if not box:
            print("Empty")
        for i, p in enumerate(box):
            print(f"{i+1}. {p}")

    def rename_box(self, index):
        new_name = input("New box name: ")
        self.names[index] = new_name

    def move_pokemon(self, from_box, p_index, to_box):
        if p_index < len(self.boxes[from_box]):
            p = self.boxes[from_box].pop(p_index)
            self.boxes[to_box].append(p)
            print(f"Moved {p.name}!")

    def release(self, box, index):
        if index < len(self.boxes[box]):
            p = self.boxes[box].pop(index)
            print(f"{p.name} was released.")

# --- PLAYER ---
class Player:
    def __init__(self):
        self.party = []
        self.pc = PC()

    def add_pokemon(self, pokemon):
        if len(self.party) < 6:
            self.party.append(pokemon)
            print(f"{pokemon.name} added to party!")
        else:
            self.pc.add(pokemon)

    def deposit(self):
        self.show_party()
        if not self.party:
            return

        i = int(input("Deposit which Pokémon: ")) - 1
        if 0 <= i < len(self.party):
            self.pc.add(self.party.pop(i))

    def withdraw(self):
        box = int(input("Box #: ")) - 1
        self.pc.show_box(box)

        i = int(input("Withdraw #: ")) - 1
        if len(self.party) < 6:
            if i < len(self.pc.boxes[box]):
                self.party.append(self.pc.boxes[box].pop(i))
                print("Added to party!")
        else:
            print("Party full!")

    def show_party(self):
        print("\n--- Party ---")
        for i, p in enumerate(self.party):
            print(f"{i+1}. {p}")

# --- SAVE / LOAD ---
def save_game(player):
    data = {
        "party": [p.to_dict() for p in player.party],
        "pc": [[p.to_dict() for p in box] for box in player.pc.boxes],
        "names": player.pc.names
    }
    with open("save.json", "w") as f:
        json.dump(data, f)
    print("Game saved!")

def load_game():
    try:
        with open("save.json", "r") as f:
            data = json.load(f)

        player = Player()
        player.party = [Pokemon.from_dict(p) for p in data["party"]]

        for i, box in enumerate(data["pc"]):
            player.pc.boxes[i] = [Pokemon.from_dict(p) for p in box]

        player.pc.names = data["names"]

        print("Game loaded!")
        return player
    except:
        print("No save found.")
        return Player()

# --- ENCOUNTER SYSTEM ---
def encounter(player):
    names = ["Pikachu", "Eevee", "Fletchling", "Bunnelby"]
    wild = Pokemon(random.choice(names), random.randint(2, 6))

    print(f"\nWild {wild.name} appeared!")

    action = input("[C]atch or [R]un: ").lower()

    if action == "c":
        if random.random() < 0.8:
            print(f"Caught {wild.name}!")
            player.add_pokemon(wild)
        else:
            print("It broke free!")

# --- PC MENU ---
def pc_menu(player):
    while True:
        print("\n--- PC ---")
        print("1. View Box")
        print("2. Rename Box")
        print("3. Move Pokémon")
        print("4. Release Pokémon")
        print("5. Deposit")
        print("6. Withdraw")
        print("7. Exit")

        c = input("Choose: ")

        if c == "1":
            b = int(input("Box #: ")) - 1
            player.pc.show_box(b)

        elif c == "2":
            b = int(input("Box #: ")) - 1
            player.pc.rename_box(b)

        elif c == "3":
            fb = int(input("From box #: ")) - 1
            player.pc.show_box(fb)
            i = int(input("Pokémon #: ")) - 1
            tb = int(input("To box #: ")) - 1
            player.pc.move_pokemon(fb, i, tb)

        elif c == "4":
            b = int(input("Box #: ")) - 1
            player.pc.show_box(b)
            i = int(input("Release #: ")) - 1
            player.pc.release(b, i)

        elif c == "5":
            player.deposit()

        elif c == "6":
            player.withdraw()

        elif c == "7":
            break

# --- MAIN ---
def main():
    player = load_game()

    if not player.party:
        player.add_pokemon(Pokemon("Froakie", 5))

    while True:
        print("\n--- MENU ---")
        print("1. Encounter")
        print("2. Party")
        print("3. PC")
        print("4. Save")
        print("5. Exit")

        c = input("Choose: ")

        if c == "1":
            encounter(player)
        elif c == "2":
            player.show_party()
        elif c == "3":
            pc_menu(player)
        elif c == "4":
            save_game(player)
        elif c == "5":
            break

if __name__ == "__main__":
    main()



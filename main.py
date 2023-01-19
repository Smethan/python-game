import json as js
from art import *
import logging
import os
from time import sleep


def cls():
    os.system("cls" if os.name == "nt" else "clear")


logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


class Game:
    def __init__(self):
        self.gameOver = False
        self.location = "Intro"
        self.prevLoc = ""
        self.HP = 10
        self.inventory = []

    def gameLoop(self):
        mapFile = js.load(open("map.json"))
        logging.info(f"Map loaded, {len(mapFile)} node(s) loaded.")
        while self.gameOver != True:
            self.location = self.step(mapFile[self.location])
            logging.info(f"loading location {self.location}")
        tprint("GG", font="block")
        if input("\nWould you like to restart? (Yes or No): ").lower() == "yes":
            logging.warning("restarting game")
            self.gameOver = False
            self.gameLoop()
        else:
            logging.warning("exiting game")
            return

    def step(self, loc):
        cls()
        if "enemy" not in loc:
            return self.move(loc)
        else:
            result = self.battle(loc["enemy"])
            match result:
                case "victory":
                    del loc["enemy"]
                    return self.move(loc)
                case "run":
                    return self.prevLoc
                case "gg":
                    self.gameOver = True
                    return

    def move(self, loc):
        print("\n", loc["text"], "\n")
        if "gameOver" in loc["choices"].keys():
            self.gameOver = True
            return
        if loc["item"]:
            self.inventory.append(loc["item"])
            print(f"You acquired {loc['item']['name']}!\n")
            del loc["item"]
        for idx, i in enumerate(loc["choices"].keys()):
            print(f"{idx + 1}. {i}")
        value = input("\nEnter your choice: ")
        while value not in loc["choices"].keys():
            value = input("Invalid input, try again: ")
        self.prevLoc = self.location
        return loc["choices"][value]

    def battle(self, enemy):
        health = enemy["health"]
        atk = enemy["atk"]
        name = enemy["name"]
        blocking = False
        options = {
            "atk": "ATTACK (5 DMG)",
            "inv": "INVENTORY",
            "def": "BLOCK (-2 DMG TAKEN)",
            "run": "RUN",
        }
        turn = 0
        tprint("BATTLE START")
        sleep(1)
        print(f"You encounter a {name}!\n")
        sleep(1)
        while health > 0 and self.HP > 0:
            while turn == 0:
                cls()
                print(f"Enemy Health: {health}")
                print(f"Your Health: {self.HP}")
                for idx, i in enumerate(options.values()):
                    print(f"{idx + 1}. {i}")
                value = input("Enter your choice (atk, def, inv, run): ")
                while value not in options.keys():
                    value = input("Invalid option, try again: ")
                if value == "inv" and len(self.inventory) == 0:
                    value = input("You Have nothing in your bag, try something else: ")
                match value:
                    case "atk":
                        print("You attack the enemy, doing 5 damage!")
                        health -= 5
                        turn = 1
                    case "def":
                        blocking = True
                        print("You take a defensive stance...")
                        turn = 1
                    case "inv":
                        cls()
                        for idx, i in enumerate(self.inventory):
                            print(f'{idx + 1}. {i["name"]}: +{i["power"]} HP')
                        ivalue = input(
                            "What item would you like to use (back to return to previous menu): "
                        )
                        if ivalue.lower() == "back":
                            break

                        while not any(
                            i["name"].lower() == ivalue.lower() for i in self.inventory
                        ):
                            ivalue = input("Invalid option, try again: ")
                        item = next(
                            item
                            for item in self.inventory
                            if item["name"].lower() == ivalue.lower()
                        )
                        print(f'You recover {item["power"]} HP!')
                        self.HP += item["power"]
                        turn = 1
                    case "run":
                        print("You run away...")
                        sleep(1)
                        return "run"

            sleep(2)
            if turn == 1 and health > 0:
                if blocking == True:
                    if atk - 2 <= 0:
                        damage = 0
                    else:
                        damage = atk - 2
                    blocking = False
                else:
                    damage = atk

                print(f"You take {damage} points of damage")
                sleep(1)
                self.HP -= damage
                turn = 0
        if self.HP <= 0:
            return "gg"
        elif health <= 0:
            return "victory"


if __name__ == "__main__":
    Game().gameLoop()

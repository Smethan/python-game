import json as js
from art import *
import logging
import os
from time import sleep

# simple function to clear screen
def cls():
    os.system("cls" if os.name == "nt" else "clear")


# logging config
logging.basicConfig(
    filename="log.txt",
    filemode="w",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

# the big class
class Game:
    # initialize required variables
    # gameOver dictates if game has reached a terminal state, be it victory or defeat
    # HP, inventory and speed are all player variables for combat
    # location should be initialized to whatever the first area you want to enter is called

    def __init__(self, fileName):
        self.gameOver = False
        self.location = "Intro"
        self.prevLoc = ""
        self.HP = 10
        self.inventory = []
        self.speed = 2
        self.fileName = fileName

    # main game loop
    def gameLoop(self):
        # load map file, which is just a json with specific keys
        mapFile = js.load(open(self.fileName))
        logging.info(f"Map loaded, {len(mapFile)} node(s) loaded.")

        # the real loop is here, runs while game is not in terminal state
        while self.gameOver != True:

            # recursively use location to update itself via step function
            self.location = self.step(mapFile[self.location])
            logging.info(f"loading location {self.location}")

        # if we break out of the loop, the game should end
        tprint("GG", font="block")

        # ask if player would like to restart
        if input("\nWould you like to restart? (Yes or No): ").lower() == "yes":
            logging.warning("restarting game")
            # create new game object to restart
            Game(self.fileName).gameLoop()
        else:
            logging.warning("exiting game")
            return

    # step function, mostly just a stepping stone to move or battle
    def step(self, loc):
        cls()

        # if there is no enemy, run move function for out of combat actions
        if "enemy" not in loc:
            return self.move(loc)
        else:
            # enemy is in location, do combat and act upon result
            result = self.battle(loc["enemy"])
            match result:
                case "victory":
                    # remove enemy upon victory and "re enter" current room
                    del loc["enemy"]
                    return self.move(loc)
                case "run":
                    # return to previous room if player ran
                    return self.prevLoc
                case "gg":
                    # player died, game over
                    self.gameOver = True
                    return

    # move function, is for all out of combat handling
    def move(self, loc):
        cls()

        # print area text to describe scene
        print("\n", loc["text"], "\n")

        # if gameOver is an option in the area keys, end game. Allows for failure outside of combat, as well as victory conditions
        if "gameOver" in loc["choices"].keys():
            self.gameOver = True
            return

        # if there is an item, add it to the players inventory and remove it from the location to stop item dupes
        if "item" in loc.keys():
            logging.info(f'found {loc["item"]["name"]}, adding to inventory')
            self.inventory.append(loc["item"])
            print(f"You acquired {loc['item']['name']}!\n")
            del loc["item"]

        # enumerate over the choices in a location, print them out with a number next to them
        for idx, i in enumerate(loc["choices"].keys()):
            print(f"{idx + 1}. {i}")

        # input handling
        value = input("\nEnter your choice: ")
        while value not in loc["choices"].keys():
            value = input("Invalid input, try again: ")

        # set prevLoc and return new location
        self.prevLoc = self.location
        return loc["choices"][value]

    # battle function, handles combat
    def battle(self, enemy):

        # fetch enemy variables
        health = enemy["health"]
        atk = enemy["atk"]
        name = enemy["name"]
        speed = enemy["speed"]

        # set some flags
        blocking = False
        options = {
            "atk": "ATTACK (5 DMG)",
            "inv": "INVENTORY",
            "def": "BLOCK (-2 DMG TAKEN)",
            "run": "RUN",
        }

        # set up max turn count, should not be changed
        maxPlayerTurns = 1 if speed > self.speed else 1 + (self.speed - speed)
        maxEnemyTurns = 1 if self.speed > speed else 1 + (speed - self.speed)

        # actual turn counters, can be changed
        ptc = maxPlayerTurns
        etc = maxEnemyTurns
        tprint("BATTLE START")
        sleep(1)
        print(f"You encounter a(n) {name}!\n")
        sleep(1)

        # main combat loop
        while health > 0 and self.HP > 0:

            # player turn loop
            while ptc > 0 and health > 0 and self.HP > 0:
                cls()
                print(f"Enemy Health: {health}")
                print(f"Your Health: {self.HP}")
                print(f"Your Turns: {ptc}")

                # handle input
                for idx, i in enumerate(options.values()):
                    print(f"{idx + 1}. {i}")
                value = input("Enter your choice (atk, def, inv, run): ")
                while value not in options.keys():
                    value = input("Invalid option, try again: ")
                # do not allow inventory usage if no items
                if value == "inv" and len(self.inventory) == 0:
                    value = input("You Have nothing in your bag, try something else: ")
                match value:
                    case "atk":
                        # player attacks enemy, decrement turn counter, do damage
                        print("You attack the enemy, doing 5 damage!")
                        logging.info("player attacked enemy")
                        health -= 5
                        ptc -= 1
                    case "def":
                        # player defends, decrement turn counter, they take less damage
                        # TODO: disallow multi blocking, it just wastes a turn
                        blocking = True
                        print("You take a defensive stance...")
                        logging.info("player defended")
                        ptc -= 1
                    case "inv":
                        # handle inventory usage, only healing items for now
                        # TODO: add buffing and damaging items
                        cls()
                        logging.info("player selected inventory")
                        for idx, i in enumerate(self.inventory):
                            print(f'{idx + 1}. {i["name"]}: +{i["power"]} HP')

                        # more input handling yay
                        ivalue = input(
                            "What item would you like to use (back to return to previous menu): "
                        )
                        if ivalue.lower() == "back":
                            # return player to previous menu without ticking turn counter
                            logging.info("returning to previous menu...")
                            continue

                        while not any(
                            i["name"].lower() == ivalue.lower() for i in self.inventory
                        ):
                            logging.warning(
                                "invalid input recieved, requesting input again..."
                            )
                            ivalue = input("Invalid option, try again: ")

                        # inventory is a list of objects so finding specific object from a key is weird
                        item = next(
                            item
                            for item in self.inventory
                            if item["name"].lower() == ivalue.lower()
                        )
                        logging.info(f'item {item["name"]} found')
                        print(f'You recover {item["power"]} HP!')

                        # heal, decrement turn counter
                        self.HP += item["power"]
                        ptc -= 1
                    case "run":
                        # player runs, return to previous area
                        logging.info(
                            f"player selected run, returning to {self.prevLoc}"
                        )
                        print("You run away...")
                        sleep(1)
                        return "run"

            sleep(2)
            # enemies turn loop
            while etc > 0 and health > 0:
                # if player blocks, do reduced or zero damage
                if blocking == True:
                    if atk - 2 <= 0:
                        damage = 0
                    else:
                        damage = atk - 2
                # otherwise, enemy attack = damage
                # TODO: add equipment and/or passive defense
                else:
                    damage = atk

                print(f"You take {damage} points of damage")
                sleep(1)
                self.HP -= damage
                etc -= 1

            # reset flags
            blocking = False
            ptc = maxPlayerTurns
            etc = maxEnemyTurns

        # player died, end game
        if self.HP <= 0:
            logging.warning("player has died, rip")
            return "gg"
        # enemy died, move forward
        elif health <= 0:
            logging.info("enemy slain, removing from room...")
            return "victory"


# bootstrap game
if __name__ == "__main__":
    Game("map.json").gameLoop()

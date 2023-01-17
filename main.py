import json as js
from art import *
import logging
import os


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

    def step(self, object):
        cls()
        print("\n", object["text"], "\n")
        if object["choices"].count("gameOver") > 0:
            self.gameOver = True
            return
        for idx, i in enumerate(object["choices"]):
            print(f"{idx + 1}. {i}")
        value = input("\nEnter your choice (Case Sensitive): ")
        while object["choices"].count(value) == 0:
            value = input("Invalid input, try again: ")
        return value


if __name__ == "__main__":
    Game().gameLoop()

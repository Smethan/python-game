import json as js
import logging

gameOver = False

logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def gameLoop():
    global gameOver
    mapFile = js.load(open("map.json"))
    logging.info(f"Map loaded, {len(mapFile)} node(s) loaded.")
    location = "Intro"
    while gameOver != True:
        location = step(mapFile[location])
        logging.info(f"loading location {location}")
    if input("Would you like to restart? (Yes or No): ").lower() == "yes":
        logging.warning("restarting game")
        gameOver = False
        gameLoop()
    else:
        logging.warning("exiting game")
        return


def step(object):
    print("\n", object["text"], "\n")
    if object["choices"].count("gameOver") > 0:
        global gameOver
        gameOver = True
        return
    for idx, i in enumerate(object["choices"]):
        print(f"{idx + 1}. {i}")
    value = input("\nEnter your choice (Case Sensitive): ")
    while object["choices"].count(value) == 0:
        value = input("Invalid input, try again: ")
    return value


if __name__ == "__main__":
    gameLoop()

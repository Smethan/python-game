import json as js


def initialize():
    mapFile = js.load(open("map.json"))
    gameLoop()


def gameLoop():
    gameOver = False
    while gameOver != True:
        return


if __name__ == "__main__":
    initialize()

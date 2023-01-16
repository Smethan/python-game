import json as js

gameOver = False


def gameLoop():
    mapFile = js.load(open("map.json"))
    location = "Intro"
    while gameOver != True:
        location = tick(mapFile[location])
    if input("Would you like to restart? (Yes or No): ") == "Yes":
        gameLoop()
    else:
        return


def tick(object):
    print("\n", object["text"], "\n")
    if object["choices"].count("gameOver") > 0:
        global gameOver
        gameOver = True
        return
    for idx, i in enumerate(object["choices"]):
        print(f"{idx + 1}. {i}")
    value = input("\nEnter your choice (case sensitive): ")
    while object["choices"].count(value) == 0:
        value = input("Invalid input, try again: ")
    return value


if __name__ == "__main__":
    gameLoop()

import requests
import io
from tree import *

name = input("Enter lichess username: ")
pgns = io.StringIO(requests.get('https://lichess.org/api/games/user/' + name).text)
history = parse_games(pgns, name)

#Todo add a history explorer that doesn't require knowing chess notation
white = history.children[0]
black = history.children[1]
print("Number of games played as white: " + str(white.weight))
print("Winrate as white:  " + str(100 * white.result / white.weight))
print("")
print("Number of games played as black: " + str(black.weight))
print("Winrate as black:  " + str(100 * black.result / black.weight))
userColor = input("enter \"White\" to inspect games as white or \"Black\" to inspect games as black: ")
if userColor == "White":
    history = white
elif userColor == "Black":
    history = black
else:
    raise Exception("Error: unrecognized color")
while history.children != []:
    for node in history.children:
        print("")
        print(node.color + " plays: " + node.move)
        print("Number of games played:  " + str(node.weight))
        print("Winrate:  " + str(100 * node.result / node.weight))
    nextMove = input("Enter next move: ")
    for node in history.children:
        if node.move == nextMove:
            history = node
print("End of history reached")
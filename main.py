import requests
import io
from tree import *

name = input("Enter lichess username: ")
pgns = io.StringIO(requests.get('https://lichess.org/api/games/user/' + name).text)
history = parse_games(pgns, name)

#Todo add a history explorer that doesn't require knowing chess notation
while history.children != []:
    for node in history.children:
        print("")
        print("Move: " + node.move)
        print("Number of games played:  " + str(node.weight))
        print("Winrate:  " + str(100 * node.result / node.weight))
    nextMove = input("Enter next move: ")
    for node in history.children:
        if node.move == nextMove:
            history = node
print("End of history reached")
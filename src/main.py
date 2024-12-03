import requests
import io
import numpy as np
import os
from tree import *

#Importing games, check saved data first
#Todo download new games of user
history = {}
name = input("Enter lichess username: ")

saved_games = {}
if os.path.isfile('../data/games.npy'):
    saved_games = np.load('../data/games.npy', allow_pickle='true').item()
if name in saved_games.keys():
    history = saved_games[name]
else:
    num_games = requests.get('https://lichess.org/api/user/' + name).json()["count"]["all"]
    
    print("Downloading all " + str(num_games) + " games played by " + name)
    download_time = int(num_games / 20) #lichess's api limits unauthenticated requests to 20 per second
    print("Estimated time to download: " + str(int(download_time / 60)) + " minutes and " + str(download_time % 60)  + " seconds")

    pgns = io.StringIO(requests.get('https://lichess.org/api/games/user/' + name).text)
    history = parse_games(pgns, name)
    
    saved_games[name] = history
    np.save('../data/games.npy', saved_games)

#Exploring results
white = history.children[0]
black = history.children[1]
if white.weight == 0 or black.weight == 0:
    print("This user does not have enough games to analyze")
    exit()
print("")
print("Number of games played as white: " + str(white.weight))
print("Winrate as white:  " + str(int(100 * white.result / white.weight)) + "%")
print("")
print("Number of games played as black: " + str(black.weight))
print("Winrate as black:  " + str(int(100 * black.result / black.weight)) + "%")
user_color = input("enter \"White\" to inspect games as white or \"Black\" to inspect games as black: ")
if user_color == "White" or user_color == "white":
    history = white
elif user_color == "Black" or user_color == "black":
    history = black
else:
    raise Exception("Error: unrecognized color")
while history.children != []:
    print("-----------------------------------------------------")
    history.children.sort(key = lambda x: x.weight, reverse = True)
    for node in history.children:
        print("")
        print(node.color + " plays: " + node.move)
        print(str(int(100 * node.result / node.weight)) + "% winrate after " + str(node.weight) + " games played")
    next_move = input("Enter next move or \"Back\": ")
    if(next_move == "Back"):
        history = history.parent
    for node in history.children:
        if node.move == next_move:
            history = node
print("End of history reached")
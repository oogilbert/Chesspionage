import chess.pgn
from fractions import Fraction

#Todo split nodes between player moves and opponent moves
#Todo combine move transpositions
class ChessNode:
    def __init__(self, move):
        self.weight = 1
        self.move = move
        self.children = []
        self.result = 0
        
    #Increments the weight of a child node if it already exists or creates a new child if it doesnt. Returns the child.
    def add_child(self, newMove):
        for child in self.children:
            if child.move == newMove:
                child.weight += 1
                return child
        newNode = ChessNode(newMove)
        self.children.append(newNode)
        return newNode
        
    def add_result(self, result):
        self.result += result

#Parse a list of a user's pgns into a tree structure
def parse_games(pgns, name):
    treeStart = ChessNode("start")
    while (game := chess.pgn.read_game(pgns)) is not None:
        resultString = game.headers["Result"].split("-")[0]  #Results strings are formatted as "1/2-1/2", "1-0" etc where the white player is listed first
        result = .5 if resultString == "1/2" else int(resultString)
        
        #add a node for all games and two child nodes for games where the player is black or white
        currentNode = treeStart
        if game.headers["White"] == name:
            currentNode = treeStart.add_child("White")
        elif game.headers["Black"] == name:
            currentNode = treeStart.add_child("Black")
            result = 1 - result #invert score when playing as black
        else:
            raise Exception("User was not found in the current game")
        treeStart.add_result(result)
        currentNode.add_result(result)
        
        #Adding the moves from current game to tree
        for move in game.mainline_moves():
            currentNode = currentNode.add_child(move.uci())
            currentNode.add_result(result)
    return treeStart
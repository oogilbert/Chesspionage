import chess.pgn
from fractions import Fraction

#Todo combine move transpositions
class ChessNode:
    def __init__(self, move, color, weight = 1):
        self.weight = weight
        self.move = move
        self.children = []
        self.result = 0
        self.color = color
        
    #Increments the weight of a child node if it already exists or creates a new child if it doesnt. Returns the child.
    def add_child(self, newMove, color):
        for child in self.children:
            if child.move == newMove and child.color == color: #Same color check may be needed for combining transpositions
                child.weight += 1
                return child
        newNode = ChessNode(newMove, color)
        self.children.append(newNode)
        return newNode
        
    def add_result(self, result):
        self.result += result

#Parse a list of a user's pgns into a tree structure
def parse_games(pgns, name):
    #Add nodes for white and black
    treeStart = ChessNode("start", "None", 0)
    treeStart.children.append(ChessNode("White", "None", 0))
    treeStart.children.append(ChessNode("Black", "None", 0))
    while (game := chess.pgn.read_game(pgns)) is not None:
        resultString = game.headers["Result"].split("-")[0]  #Results strings are formatted as "1/2-1/2", "1-0" etc where the white player is listed first
        result = .5 if resultString == "1/2" else int(resultString)
        
        #go back to the start of the tree and invert score if player is playing black
        currentNode = treeStart
        if game.headers["White"] == name:
            currentNode = treeStart.add_child("White", "None")
        elif game.headers["Black"] == name:
            currentNode = treeStart.add_child("Black", "None")
            result = 1 - result #invert score when playing as black
        else:
            raise Exception("User was not found in the current game")
        treeStart.add_result(result)
        currentNode.add_result(result)
        
        #Adding the moves from current game to tree
        color = "White"
        for move in game.mainline_moves():
            currentNode = currentNode.add_child(move.uci(), color)
            currentNode.add_result(result)
            if color == "White":
                color = "Black"
            else:
                color = "White"
    return treeStart
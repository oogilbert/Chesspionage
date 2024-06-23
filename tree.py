import chess.pgn
from fractions import Fraction

class ChessNode:
    def __init__(self, move, color, parent, weight = 1):
        self.weight = weight
        self.move = move
        self.children = []
        self.result = 0
        self.color = color
        self.parent = parent
        
    #Increments the weight of a child node if it already exists or creates a new child if it doesnt. Returns the child.
    def add_child(self, new_move, color):
        for child in self.children:
            if child.move == new_move and child.color == color: #Same color check may be needed for combining transpositions
                child.weight += 1
                return child
        new_node = ChessNode(new_move, color, self)
        self.children.append(new_node)
        return new_node
        
    def add_result(self, result):
        self.result += result

#Parse a list of a user's pgns into a tree structure
def parse_games(pgns, name):
    #Add separate subtrees for games where user plays white and games where user plays black
    tree_start = ChessNode("start", "None", None, 0)
    tree_start.children.append(ChessNode("White", "None", tree_start, 0))
    tree_start.children.append(ChessNode("Black", "None", tree_start, 0))
    
    while (game := chess.pgn.read_game(pgns)) is not None:
        result_string = game.headers["Result"].split("-")[0]  #Results strings are formatted as "1/2-1/2", "1-0" etc where the white player is listed first
        result = .5 if result_string == "1/2" else int(result_string)
        
        #Return to start of tree
        current_node = tree_start
        if game.headers["White"] == name:
            current_node = tree_start.add_child("White", "None")
        elif game.headers["Black"] == name:
            current_node = tree_start.add_child("Black", "None")
            result = 1 - result #invert score when playing as black
        else:
            raise Exception("User was not found in the current game")
        tree_start.add_result(result)
        current_node.add_result(result)
        
        #Add moves from current game to tree
        color = "White"
        for move in game.mainline_moves():
            current_node = current_node.add_child(move.uci(), color)
            current_node.add_result(result)
            if color == "White":
                color = "Black"
            else:
                color = "White"
    return tree_start
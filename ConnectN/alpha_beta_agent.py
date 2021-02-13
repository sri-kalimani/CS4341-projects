import math
import agent
import board
import game


###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth, player):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.move_dictionary = []
        self.player = player

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        best_move_value = self.min(brd)
        moves = self.move_dictionary
        for move in moves:
            if move[1] == best_move_value:
                best_move = move[0]
        return best_move

    def min(self, state):
        """search for the minimum move"""
        if state.get_outcome() != 0:
            return self.utillity(state)
        v = float('inf')
        for a in self.get_successors(state):
            v = min(v, self.max(self.result(state, a)))
        return v

    def max(self, state):
        """search for the maximum move"""
        if state.get_outcome() != 0:
            return self.utillity(state)
        v = float('-inf')
        for a in self.get_successors(state):
            v = max(v, self.min(self.result(state, a)))
            self.move_dictionary.append((a[1], v))
        return v

    def utillity(self, state):
        """get the utillity of a state"""
        outcome = state.get_outcome()
        if outcome == 0:
            return 0
        if outcome == self.player:
            return 1
        if outcome != self.player:
            return -1
        return 0

    def result(self, state, action):
        """return the board after an action"""
        moves = self.get_successors(state)
        for move in moves:
            if move[1] == action[1]:
                return move[0]
        return 0

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb, col))
        return succ

# board1 = [[1, 2, 1, 2],
#         [1, 1, 2, 1],
#        [1, 1, 0, 0],
#       [2, 2, 0, 0],
#      [0, 0, 0, 0],
#     [0, 0, 0, 0]]
# b = board.Board(board1, 4, 6, 4)
# g = game.Game(4,  # width
#             6,  # height
#            4,  # tokens in a row to win
#           agent.InteractiveAgent("human"),  # player 1
#          AlphaBetaAgent("alphabeta", 4))  # player 2
# g.board = b

# outcome = g.go()

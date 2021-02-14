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
        alpha = -math.inf
        beta = math.inf
        if self.player == 1:
            best_move_value = self._min(brd, self.max_depth, alpha, beta)

        else:
            best_move_value = self._max(brd, self.max_depth, alpha, beta)
        moves = self.move_dictionary
        for move in moves:
            if move[1] == best_move_value:
                best_move = move[0]
        return best_move


    def _min(self, state, depth, alpha, beta):
        """search for the minimum move"""
        out = state.get_outcome()
        succ = self.get_successors(state)
        # if state.get_outcome() != 0 or depth == 0:
        #     return self.utillity(state)
        if not succ  or depth == 0:
            return self.utillity(state)

            
        v = float('inf')
        for a in succ:
            # v = min(v, self._max(self.result(state, a)))

            new_score = self._max(a[0], depth-1, alpha, beta)
            if new_score < v:
                v = new_score
                self.move_dictionary.append((a[1], v))

            beta = min(beta, v)
            if alpha >= beta:
                break
        
        return v

    def _max(self, state, depth, alpha, beta):
        """search for the maximum move"""
        out = state.get_outcome()
        succ = self.get_successors(state)
        # if state.get_outcome() != 0 or depth == 0:
        #     return self.utillity(state)
        if not succ or depth == 0:
            return self.utillity(state)
        v = float('-inf')
        for a in succ:
            # v = max(v, self.min(self.result(state, a)))
            # self.move_dictionary.append((a[1], v))

            new_score = self._min(a[0], depth-1, alpha, beta)
            if new_score > v:
                v = new_score
                self.move_dictionary.append((a[1], v))

            alpha = max(alpha, v)
            if alpha >= beta:
                break

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
        succ = self.get_successors(state)
        for move in succ:
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
#           agent.RandomAgent("random"), # player 1
#          AlphaBetaAgent("alphabeta", 4, 2))  # player 2
# g.board = b

# outcome = g.go()
THE_AGENT = AlphaBetaAgent("Group13", 4,1)
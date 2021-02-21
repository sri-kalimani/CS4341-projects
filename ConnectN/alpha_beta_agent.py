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
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.move_dictionary = []

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        # print(self.move_dictionary, "move_array")
        """Search for the best move (choice of column for the token)"""
        # Your code here
        move, score = self._max(brd, self.max_depth, -math.inf, math.inf)
        moves = self.move_dictionary
        for m in moves:
            if m[1] == score:
                return move

    def _min(self, state, depth, alpha, beta):
        """search for the minimum move"""
        out = state.get_outcome()  # getting the outcome of the game
        succ = self.get_successors(state)

        if out == self.player:  # if we won the game
            return (None, 100000000000000)
        elif out != self.player and out != 0:
            return (None, -100000000000000)  # if we lost the game

        if not succ or depth == 0:  # if there are no successors or depth is 0 then we are looking at terminal nodes
            return (None, self.evaluate(state))

        v = float('inf')
        for a in succ:
            _, new_score = self._max(a[0], depth - 1, alpha, beta)
            if new_score < v:  # if new score is better, add it to our move dictionary
                v = new_score
                move = a[1]
                self.move_dictionary.append((move, v))

            beta = min(beta, v)
            if alpha >= beta:
                break

        return (move, v)

    def _max(self, state, depth, alpha, beta):
        """search for the maximum move"""
        out = state.get_outcome()
        succ = self.get_successors(state)

        if out == self.player:
            return (None, 100000000000000)  # if we won the game
        elif out != self.player and out != 0:
            return (None, -100000000000000)  # if we lost the game

        if not succ or depth == 0:  # if there are no successors or depth is 0 then we are looking at terminal nodes
            return (None, self.evaluate(state))
        v = float('-inf')
        for a in succ:

            _, new_score = self._min(a[0], depth - 1, alpha, beta)
            if new_score > v:
                v = new_score
                move = a[1]
                self.move_dictionary.append((move, v))

            alpha = max(alpha, v)
            if alpha >= beta:
                break

        return (move, v)

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

    def utillity(self, brd, x, y, dx, dy):
        """Returns positive score or negative score for cell starting at (x,y) in direction (dx,dy)"""
        # checking for boundaries
        if ((x + (brd.n - 1) * dx >= brd.w) or (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)): return 0
        t = brd.board[y][x]  # token
        # Counting # of consecutive tokens
        count = 0
        if t != 0:
            count = 1

        # Going through elements
        for i in range(1, brd.n):
            current = brd.board[y + i * dy][x + i * dx]

            # If we the cell is blank then set t to be the token we are looking at
            if t == 0:
                t = current

            # Count then number of consecutive tokens
            if current == t and t != 0:
                count = count + 1

            # if different token is found, stop counting and return 0
            elif current != 0:return 0

        # If we counted oponent's tokens then multiply count by -1
        if t != self.player:
            count *= -1

        return count

    def evaluate(self, brd):
        score = 0

        # go through each cell, evaluate every move by assigning score
        for x in range(brd.w):
            for y in range(brd.h):
                score += self.utillity(brd, x, y, 1, 0)
                score += self.utillity(brd, x, y, 0, 1)
                score += self.utillity(brd, x, y, 1, 1)
                score += self.utillity(brd, x, y, 1, -1)

        return score

    def is_terminal_node(self, board):
        return board.get_outcome() or len(self.get_successors(board)) == 0


# outcome = g.go()
THE_AGENT = AlphaBetaAgent("Group13", 4)

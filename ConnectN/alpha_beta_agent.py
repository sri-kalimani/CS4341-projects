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
        print(self.move_dictionary, "sdasdas")
        """Search for the best move (choice of column for the token)"""
        # Your code here

        if self.player == 1:
            move, _ = self._max(brd, self.max_depth, -math.inf, math.inf)


        else:
            move, _ = self._min(brd, self.max_depth, -math.inf, math.inf)




        return move




    def _min(self, state, depth, alpha, beta):
        """search for the minimum move"""
        out = state.get_outcome()
        succ = self.get_successors(state)

        if out == 1:
            return (None,100000000000000)  # An arbitrarily large score for P1
        elif out == 2:
            return (None,-100000000000000)  # An equally arbitrarily large score for P2



        if not succ  or depth == 0 :
            # return self.utillity(state)
            return (None,self.evaluate(state))


        v = float('inf')
        for a in succ:
            # v = min(v, self._max(self.result(state, a)))

            _,new_score = self._max(a[0], depth-1, alpha, beta)
            if new_score < v:
                v = new_score
                move = a[1]
                self.move_dictionary.append((move, v))

            beta = min(beta, v)
            if alpha >= beta:
                break

        return (move,v)

    def _max(self, state, depth, alpha, beta):
        """search for the maximum move"""
        out = state.get_outcome()
        succ = self.get_successors(state)


        if out == 1:
            return (None,100000000000000)  # An arbitrarily large score for P1
        elif out == 2:
            return (None,-100000000000000)  # An equally arbitrarily large score for P2


        if not succ or depth == 0 :

            return (None,self.evaluate(state))
        v = float('-inf')
        for a in succ:


            _,new_score = self._min(a[0], depth-1, alpha, beta)
            if new_score > v:
                v = new_score
                move = a[1]
                self.move_dictionary.append((move, v))

            alpha = max(alpha, v)
            if alpha >= beta:
                break

        return (move,v)






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

    # def scoreN(self,brd, x, y, dx, dy):
    #     """Returns positive score or negative score for cell starting at (x,y) in direction (dx,dy)"""
    #     # Avoid out-of-bounds errors
    #     if ((x + (brd.n - 1) * dx >= brd.w) or
    #             (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)):
    #         return 0
    #     # Get token at (x,y)
    #     t = brd.board[y][x]
    #
    #     # Count number of tokens for a given player
    #     count = 0
    #     score  = 0
    #
    #     if t != 0:
    #         count = 1
    #
    #     # Go through elements
    #     for i in range(1, brd.n):
    #         current = brd.board[y + i * dy][x + i * dx]
    #
    #         # If first token is blank, set t to next player token
    #         if t == 0:
    #             t = current
    #
    #         # Add to count for every token found that is same as token t
    #         if current == t and t != 0:
    #             count = count + 1
    #
    #
    #         # If opponent token is found, this area is not useful, return 0
    #         elif current != 0:
    #             return 0
    #
    #         if count == 4 :
    #             score += 100
    #
    #         elif count == 3 :
    #             score += 10
    #         elif count == 2:
    #             score += 5
    #
    #         elif count == 1:
    #             score += 1
    #
    #     # Set count to negative if it's looking at player 2's tokens
    #     if t == 2:
    #         score*= -1
    #
    #     return score

    def scoreN(self,brd, x, y, dx, dy):
        """Returns positive score or negative score for cell starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (brd.n - 1) * dx >= brd.w) or
                (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)):
            return 0
        # Get token at (x,y)
        t = brd.board[y][x]

        # Count number of tokens for a given player
        count = 0

        if t != 0:
            count = 1

        # Go through elements
        for i in range(1, brd.n):
            current = brd.board[y + i * dy][x + i * dx]

            # If first token is blank, set t to next player token
            if t == 0:
                t = current

            # Add to count for every token found that is same as token t
            if current == t and t != 0:
                count = count + 1

            # If opponent token is found, this area is not useful, return 0
            elif current != 0:
                return 0

        # Set count to negative if it's looking at player 2's tokens
        if t == 2:
            count *= -1

        return count

    def evaluate(self,brd):
        score = 0

        # Check each cell in board
        for x in range(brd.w):
            for y in range(brd.h):
                # Sum score for cell and direction
                score += self.scoreN(brd, x, y, 1, 0)
                score += self.scoreN(brd, x, y, 0, 1)
                score += self.scoreN(brd, x, y, 1, 1)
                score += self.scoreN(brd, x, y, 1, -1)

        return score

    def is_terminal_node(self,board):
        return board.get_outcome() or len(self.get_successors(board)) == 0




# outcome = g.go()
THE_AGENT = AlphaBetaAgent("Group13", 4)
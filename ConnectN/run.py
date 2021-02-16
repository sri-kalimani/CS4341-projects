import random
import game
import agent
import alpha_beta_agent as aba

# Set random seed for reproducibility
random.seed(3)

#
# Random vs. Random
#
# g = game.Game(7, # width
#              6, # height
#              4, # tokens in a row to win
#              agent.RandomAgent("random1"),       # player 1
#             agent.RandomAgent("random2"))       # player 2

#
# Human vs. Random
#
# g = game.Game(4, # width
#               4, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human"),    # player 1
#               agent.RandomAgent("random"))        # player 2

#
# Random vs. AlphaBeta
#
g = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
              agent.RandomAgent("random"),  # player 1
              aba.AlphaBetaAgent("alphabeta", 4))  # player 2


g1 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
            aba.AlphaBetaAgent("alphabeta", 4),
              agent.RandomAgent("random")  # player 1
              )  # player 2
#


g2 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
              agent.RandomAgent("random"),  # player 1
              aba.AlphaBetaAgent("alphabeta", 4))  # player 2


g3 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
            aba.AlphaBetaAgent("alphabeta", 4),
              agent.RandomAgent("random")  # player 1
              )  # player 2


g4 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
              agent.RandomAgent("random"),  # player 1
              aba.AlphaBetaAgent("alphabeta", 4))  # player 2


g5 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
            aba.AlphaBetaAgent("alphabeta", 4),
              agent.RandomAgent("random")  # player 1
              )  # player 2



g6 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
               agent.RandomAgent("random"),  # player 1
              aba.AlphaBetaAgent("alphabeta", 4))  # player 2


g7 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
            aba.AlphaBetaAgent("alphabeta", 4),
              agent.RandomAgent("random")  # player 1
              )  # player 2



g8 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
              agent.RandomAgent("random"),  # player 1
              aba.AlphaBetaAgent("alphabeta", 4))  # player 2


g9 = game.Game(7,  # width
              6,  # height
              4,  # tokens in a row to win
            aba.AlphaBetaAgent("alphabeta", 4),
              agent.RandomAgent("random")  # player 1
              )  # player 2
# Human vs. AlphaBeta
#
g10 = game.Game(7, # width
               6, # height
               4, # tokens in a row to win
                aba.AlphaBetaAgent("alphabeta", 4),
               agent.InteractiveAgent("human"),    # player 1
               ) # player 2

#
# Human vs. Human
#
# g = game.Game(7, # width
#               6, # height
#               4, # tokens in a row to win
#               agent.InteractiveAgent("human1"),   # player 1
#               agent.InteractiveAgent("human2"))   # player 2

# Execute the game
outcome = g.go()
outcome1 = g1.go()
outcome2 = g2.go()
outcome3 = g3.go()
outcome4 = g4.go()
outcome5 = g5.go()
outcome6 = g6.go()
outcome7 = g7.go()
outcome8 = g8.go()
outcome9 = g9.go()
#outcome10 = g10.go()
print(g.players[outcome-1].name, " game 0 \n",
      g1.players[outcome1-1].name, " game 1 \n",
      g2.players[outcome2-1].name, " game 2 \n",
      g3.players[outcome3-1].name, " game 3 \n",
      g4.players[outcome4-1].name, " game 4 \n",
      g5.players[outcome5-1].name, " game 5 \n",
      g6.players[outcome6-1].name, " game 6 \n",
      g7.players[outcome7-1].name, " game 7 \n",
      g8.players[outcome8-1].name, " game 8 \n",
      g9.players[outcome9-1].name, " game 9 \n")
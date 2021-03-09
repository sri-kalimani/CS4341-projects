# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group13')
from expecti_max_AI import AI


# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
g.add_character(AI("Chut", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
g.go(1)
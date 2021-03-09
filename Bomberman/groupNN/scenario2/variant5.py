# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster


# TODO This is your code!
random.seed(123) # TODO Change this if you want different random choices
sys.path.insert(1, '../group13')
from expecti_max_v2 import AI

# Create the game

g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("monster", # name
                            "S",       # avatar
                            3, 5,      # position
))
g.add_monster(SelfPreservingMonster("monster", # name
                                    "A",       # avatar
                                    3, 13,     # position
                                    2          # detection range
))



# TODO Add your character
g.add_character(AI("Chut", "C", 0, 0))
# Run!
g.go(1)

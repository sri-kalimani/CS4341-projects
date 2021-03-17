training = False

# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from events import Event
from monsters.stupid_monster import StupidMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from agent2 import Agent

def initialize(randomMove):

    # Create the game
    random.seed() # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid", # name
                                "S",      # avatar
                                3, 9      # position
    ))

    # TODO Add your character
    char = Agent("me", # Name
                "C",  # Avatar
                0, 0, # Position
                's2v2.csv',
                's2v2.csv',
                training,
                randomMove
    )

    g.add_character(char)

    # Run!
    g.go(1)

    # Update weights for last move after game finishes
    if training:
        char.updateWeights(char.lastWrld, g.world)
        char.updateWeights(g.world, g.world)
    
    # Return whether the player won or not
    for i in g.world.events:
        if i.tpe == Event.CHARACTER_FOUND_EXIT:
            return True

    return False

if not training:
    initialize(0)
else:
    print("In training mode")

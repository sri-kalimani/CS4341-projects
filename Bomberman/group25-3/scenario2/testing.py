# This is necessary to find the main code
# import sys
# sys.path.insert(0, '../../bomberman')
# sys.path.insert(1, '..')

# # Import necessary stuff
# import random
# from game import Game
# from events import Event
# from monsters.selfpreserving_monster import SelfPreservingMonster

# # TODO This is your code!
# sys.path.insert(1, '../groupNN')
# from agent2 import Agent




import sys
sys.path.insert(0, '../bomberman')

from entity import CharacterEntity, BombEntity, MonsterEntity
from colorama import Fore, Back
from events import Event
from game import Game



from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster
from expecti_max_AI import AI


randomMove= 1

class training:
    def __init__(self):
        self.EPISODES = 25
        self.randomMove= 1



    # Train the algorithm
    def train(self):

        for episode in range(self.EPISODES):
            # print number of the current episode to keep track of them
            print(episode)
            # create and initialize a game
            g = Game.fromfile('map.txt', '../bomberman/sprites/')

            g.add_monster(SelfPreservingMonster("selfpreserving", # name
                                                "S",              # avatar
                                                3, 9,             # position
                                                1                 # detection range
            ))

            # TODO Add your character
            char = Agent("me", # Name
                        "C",  # Avatar
                        0, 0, # Position
                        's2v3.csv',
                        's2v3.csv',
                        training,
                        randomMove
            )

            g.add_character(char)
            g.go(1)


            

Q = training()
Q.train()


# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')

from entity import CharacterEntity, BombEntity, MonsterEntity
from colorama import Fore, Back
from events import Event
from game import Game
import random



from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster
from ai import AI
class training:
    def __init__(self):
        self.EPISODES = 10



    # Train the algorithm
    def train(self):

        for episode in range(self.EPISODES):
            # print number of the current episode to keep track of them
            print(episode)
            # create and initialize a game
            random.seed(episode)
            g = Game.fromfile('scenario2/map.txt', '../bomberman/sprites/')
            g.add_monster(StupidMonster("monster",  # name
                                        "S",  # avatar
                                        3, 5,  # position
                                        ))
            g.add_monster(SelfPreservingMonster("monster",  # name
                                                "A",  # avatar
                                                3, 13,  # position
                                                2  # detection range
                                                ))

            # TODO Add your character
            g.add_character(AI("Chut", "C", 0, 0, 800))
            g.go(1)

Q = training()
Q.train()
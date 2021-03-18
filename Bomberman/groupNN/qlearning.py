import numpy as np
import sys
import random
import math

sys.path.insert(0, '../bomberman')

from entity import CharacterEntity
from sensed_world import SensedWorld
from colorama import Fore, Back
from math import sqrt
import helper
import expecti_max_AI



class QLearning(CharacterEntity):

    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        
        self.alpha = 0.5
        self.epsln = 0.2
        self.gamma = 0.9
        self.state_size = 1000
        self.action_size = 5

    def getStates(self, wrld):
        worlds = []

        # Iterate over all possible actions.
        for bomb in [True, False]:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (self.me.x + dx >= 0 and self.me.x + dx < wrld.width() and
                        self.me.y + dy >= 0 and self.me.y + dy < wrld.height() and
                        not wrld.wall_at(self.me.x + dx, self.me.y + dy)):
                        
                        # Generate the new world.
                        tmpWrld = SensedWorld.from_world(wrld)
                        tmpChar = tmpWrld.me(self)
                        tmpChar.move(dx, dy)
                        if bomb:
                            tmpChar.place_bomb()
                        
                        # Add it to the list.
                        tmpWrld, _ = tmpWrld.next()
                        worlds.append((tmpWrld, (dx, dy, bomb)))

        return worlds


    def do(self, wrld):
        self.getAllFree(wrld)


# if __name__ == '__main__':

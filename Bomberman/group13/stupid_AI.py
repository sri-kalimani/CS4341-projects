# This is necessary to find the main code
import heapq
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from helper import *

class AI(CharacterEntity):
    def __init__(self, name, avatar, x, y,):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.exit = None

    def do(self, world):

        if self.exit is None:
            for x in range(world.width()):
                for y in range(world.height()):
                    if world.exit_at(x, y):
                        self.exit = (x, y)

        path = Astar(world, (self.x, self.y), self.exit)

        for i in range(1, len(path)):
            self.set_cell_color(path[i][0], path[i][1], Fore.RED + Back.GREEN)
        next_cell = path[1]
        if not world.wall_at(next_cell[0], next_cell[1]) :
            self.move(next_cell[0] - self.x, next_cell[1] - self.y)





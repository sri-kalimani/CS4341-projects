# This is necessary to find the main code
import heapq
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from astar import *

class Agent(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.exit = None
        self.bombed = None
        self.tiles = {}

    def do(self, world):
        if self.exit is None:
            for x in range(world.width()):
                for y in range(world.height()):
                    if world.exit_at(x, y):
                        self.exit = (x, y)

        if self.bombed is not None:
            path = Astar(world, (self.x, self.y), (0, 0))
        else:
            path = Astar(world, (self.x, self.y), self.exit)

        self.tiles = {}
        for i in range(1, len(path)):
            self.set_cell_color(path[i][0], path[i][1], Fore.RED + Back.GREEN)

        next_cell = path[1]
        if self.bombed is not None:
            if world.bomb_at(self.bombed[0], self.bombed[1]) is None \
                    and world.explosion_at(self.bombed[0], self.bombed[1]) is None:
                self.bombed = None
        elif not world.wall_at(next_cell[0], next_cell[1]):
            self.move(next_cell[0] - self.x, next_cell[1] - self.y)
        else:
            print('Placing bomb!')
            self.place_bomb()
            self.bombed = (self.x, self.y)
            self.move(next_cell[0] - self.x, next_cell[1] - self.y)

    # Adapted from RedBlobGames



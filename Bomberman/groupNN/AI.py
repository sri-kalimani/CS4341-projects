# This is necessary to find the main code
import heapq
import sys
from enum import Enum

from bomberman.monsters.selfpreserving_monster import SelfPreservingMonster
from bomberman.monsters.stupid_monster import StupidMonster

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from astar import *


class State(Enum):
    SAFE = 1
    RANDOM = 2
    AGGRESSIVE = 3
    RANAGGER = 4


class Agent(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.exit = None
        self.bombed = None
        self.tiles = {}
        self.state = State.SAFE

    def do(self, world):
        # find where exit is
        if self.exit is None:
            for x in range(world.width()):
                for y in range(world.height()):
                    if world.exit_at(x, y):
                        self.exit = (x, y)

        # change state depending if monsters are near
        for x in range(self.x - 3, self.x + 3):
            for y in range(self.y - 3, self.y + 3):
                if world.monsters_at(x, y):
                    if world.monsters.get(world.index(x, y)) == StupidMonster:
                        self.state = State.RANDOM
                    if world.monsters.get(world.index(x, y)) == SelfPreservingMonster:
                        self.state = State.AGGRESSIVE
                    if world.monsters.get(world.index(x, y)) == StupidMonster and world.monsters.get(
                            world.index(x, y)) == SelfPreservingMonster:
                        self.state = State.RANAGGER

        # change behavior depending on state
        if self.state == State.SAFE:
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
        elif self.state == State.RANDOM:
            print('near random monster')
            # expectimax
        elif self.state == State.AGGRESSIVE:
            print('near aggressive monster')
            # minmax
        elif self.state == State.RANAGGER:
            print('near an agressive and random monster')
            # q learning
        else:
            print('unknown state')

    # Adapted from RedBlobGames

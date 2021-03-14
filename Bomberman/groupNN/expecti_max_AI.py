
import sys
import random
import math

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from sensed_world import SensedWorld
from colorama import Fore, Back
from math import sqrt
from helper import *
import random




class AI(CharacterEntity):
    def __init__(self, name, avatar, x, y, ):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.bomb_timer = 0
        self.loc = []


    # avoid mosnter
    def avoid_mon(self, wrld, p):
        monsta,distance = 0,0
        monsters_array = []

        m1,m2 = p[0], p[1]

        for x in range(wrld.width()):
            for y in range(wrld.height()):
                monsters = wrld.monsters_at(x, y)
                if monsters: # look for monsters around
                    for mon in monsters:
                        monsters_array.append((mon, (x, y)))
        for mon in monsters_array:

            if (monsta == 0):
                monsta = mon
                
                distance = sqrt((m1 - mon[1][0])**2 + (m2 - mon[1][1])**2)
            else:
                dis = sqrt((m1 - mon[1][0])**2 + (m2 - mon[1][1])**2)
                if dis < distance:
                    monsta = mon
                    distance = dis

        return monsta, distance

    # reward system
    def fitness(self, wrld, loc):
        x = loc[0]
        y = loc[1]
        reward = 0
        reward += self.loc[x][y]

        m = self.avoid_mon(wrld, (x, y))
        if m[1]:
            if (m[1] < 9):
                reward -= 100
            if (m[1] < 8):
                reward -= 200
            if (m[1] < 7):
                reward -= 400
            if (m[1] < 6):
                reward -= 1400
            if (m[1] < 5):
                reward -= 2800
            if (m[1] < 4):
                reward -= 5600
            if (m[1] < 3):
                reward -= 11200
            if (m[1] < 2):
                reward -= 22400
            else:
                reward -= (1 / m[1]) * 2000

        if isEmpty(x, y, wrld) < 1:
            reward -= 2000
        if isEmpty(x, y, wrld) < 5:
            reward -= 100


        if bomb_distance(x, y, wrld) > 0:
            reward -= (10 / bomb_distance(x, y, wrld)) * 1000000
        if wrld.bomb_at(x, y) is not None:
            if wrld.bomb_at(x, y).timer <= 5:
                reward -= 100000

        if wrld.exit_at(x, y):

            reward += 10000000000000000

        if wrld.explosion_at(x, y) is not None:
            reward -= 10000000000000000000

        return reward

       

    def maxValue(self, wrld, val, level):
        if level >= 1:
            return self.fitness(wrld, val)
        value = -math.inf
        for loc in self.cell(wrld):
            newWorld = SensedWorld.from_world(loc[0])
            character = newWorld.me(self)
            character.x = loc[1][0]
            character.y = loc[1][1]
            value = max(value, self.expValue(newWorld, loc[1], level + 1))
        return value

    def expValue(self, wrld, val, level):

        if level >= 2:
            return self.fitness(wrld, val)
        value = 0
        mon = self.avoid_mon(wrld, val)
        if not mon[0]:
            value = value + (self.maxValue(wrld, val, level + 1))
            return value
        mon_val = self.monAction(wrld, mon[0][1])
        for vals in mon_val:
            vals[0].next()
            pb = monster_distance(val, vals[1])
            value = value + ((pb) * self.maxValue(vals[0], val, level + 1))
        return value


    def expectimax_search(self, wrld):
        # for Event in event:
        c_level = 0
        search_result = 0
        current_val = -math.inf
        max_val = -math.inf


        for wrld, val in self.cell(wrld):
            newWorld = SensedWorld.from_world(wrld)
            character = newWorld.me(self)
            character.x ,character.y = val[0],val[1]

            current_val = max(current_val, self.expValue(wrld, val, c_level + 1))
            if current_val > max_val:
                max_val = current_val
                search_result = val

        return search_result

 


    



    # 8 near safe cells
    def cell(self, brd):
        cells = []
        if isWall(self.x + 1, self.y, brd):
            cells.append((brd, (self.x + 1, self.y)))
        if isWall(self.x - 1, self.y, brd):
            cells.append((brd, (self.x - 1, self.y)))
        if isWall(self.x, self.y + 1, brd):
            cells.append((brd, (self.x, self.y + 1)))
        if isWall(self.x, self.y - 1, brd):
            cells.append((brd, (self.x, self.y - 1)))
        if isWall(self.x + 1, self.y + 1, brd):
            cells.append((brd, (self.x + 1, self.y + 1)))
        if isWall(self.x + 1, self.y - 1, brd):
            cells.append((brd, (self.x + 1, self.y - 1)))
        if isWall(self.x - 1, self.y + 1, brd):
            cells.append((brd, (self.x - 1, self.y + 1)))
        if isWall(self.x - 1, self.y - 1, brd):
            cells.append((brd, (self.x - 1, self.y - 1)))
        cells.append((brd, (self.x, self.y)))

        return cells


    def monAction(self, wrld, loc):
        cells = []
        x, y = loc

        for action in [(x, y - 1), (x, y + 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x + 1, y + 1),
                      (x - 1, y - 1)]:

            if isWall(action[0], action[1], wrld):
                newWorld = SensedWorld.from_world(wrld)
                monster = newWorld.monsters_at(x, y)[0]
                monster.move(action[0], action[1])
                cells.append((newWorld, action))

        return cells



    def do(self, wrld):

        bomb = boom(wrld)


        if self.loc == []:
            self.loc = [[0] * wrld.height() for _ in range(wrld.width())]
            exit_x, exit_y = wrld.exitcell
            self.loc[exit_x][exit_y] = math.inf

        if bomb:
            self.bomb_timer += 1
        self.place_bomb()

        if self.bomb_timer == 3:

            self.bomb_timer = 0

        move = self.expectimax_search(wrld)
        dx = move[0] - self.x
        dy = move[1] - self.y
        self.move(dx, dy)  # execute our final decided on motion

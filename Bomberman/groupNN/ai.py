# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue 
import math
from helper import *



class AI(CharacterEntity):

    def __init__(self, name, avatar, x, y, d):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.sensitivity = d   # d is distance to monster ,higher means stay further away from a monster near u

    def expectimax(self, wrld, events, depth):

        for event in events:
            if event.tpe == event.CHARACTER_FOUND_EXIT:
                # character is winning so best evaluation
                return math.inf

            elif event.tpe == event.BOMB_HIT_CHARACTER or event.tpe == event.CHARACTER_KILLED_BY_MONSTER:
                # character is dead so worst evaluation
                return -math.inf

        if depth >= 2:
            # if we reach the terminal nodes
            return eval(self.sensitivity,wrld)

        values_array = []
        c = next(iter(wrld.characters.values()))  
        c = c[0]

        monster_array = wrld.monsters.values()
        monster_num = 0
        if len(monster_array) == 0:
            monster_num = 1
        elif len(monster_array) == 1:
            m = next(iter(monster_array))[0]
        else:
            m1 = next(iter(monster_array))[0]
            m2 = next(iter(monster_array))[0]
            if max(m1.x - c.x, m1.y - c.y) > max(m2.x - c.x, m2.y - c.y):
                m = m2
            else:
                m = m1

        # go through the possible moves of the character
        
        for dx_c in [-1, 0, 1]:
            if (c.x + dx_c >= 0) and (c.x + dx_c < wrld.width()):  #   out-of-bound indexing
                for dy_c in [-1, 0, 1]:
                    if (c.y + dy_c >= 0) and (c.y + dy_c < wrld.height()):  # out-of-bound indexing
                        if not wrld.wall_at(c.x + dx_c, c.y + dy_c):  # check to make move in our wrld
                            c.move(dx_c, dy_c)
                            if monster_num:
                                (new_wrld, new_events) = wrld.next()
                                action = self.expectimax(new_wrld, new_events, depth + 1)
                                values_array.append(action)
                            else:
                                n = 0  # number of options for monster actions
                                sum_v = 0  # sum of all monster actions value

                                for dx_m in [-1, 0, 1]:  # go through the possible moves of the monster
                                    if (m.x + dx_m >= 0) and (m.x + dx_m < wrld.width()):  # out-of-bound check
                                        for dy_m in [-1, 0, 1]:
                                            if (dx_m != 0) or (dy_m != 0):
                                                if (m.y + dy_m >= 0) and (m.y + dy_m < wrld.height()):
                                                    if not wrld.wall_at(m.x + dx_m, m.y + dy_m):
                                                        m.move(dx_m, dy_m)
                                                        (new_wrld, new_events) = wrld.next()
                                                        n += 1  # number of options for monster movements
                                                        sum_v += self.expectimax(new_wrld, new_events, depth + 1)
                                values_array.append(sum_v / n)
        v = max(values_array)
        return v




    def expectimax_search(self, wrld, depth):

        action = (0, 0)
        max_value = -math.inf

        c = next(iter(wrld.characters.values())) 
        c = c[0]
        monster_array = wrld.monsters.values()
        monster_num = 0
        if len(monster_array) == 0:
            monster_num = 1
        elif len(monster_array) == 1:
            m = next(iter(monster_array))[0]
        else:
            m1 = next(iter(monster_array))[0]
            m2 = next(iter(monster_array))[0]
            if max(m1.x - c.x, m1.y - c.y) > max(m2.x - c.x, m2.y - c.y):
                m = m2  # m2 is closer to c
            else:
                m = m1  # m1 is closer to c

        # Go through the possible moves of the character
        for dx_c in [-1, 0, 1]:
            if (c.x + dx_c >= 0) and (c.x + dx_c < wrld.width()):
                for dy_c in [-1, 0, 1]:
                    if (c.y + dy_c >= 0) and (c.y + dy_c < wrld.height()):
                        if not wrld.wall_at(c.x + dx_c, c.y + dy_c):
                            c.move(dx_c, dy_c)
                            if monster_num:
                                (new_wrld, new_events) = wrld.next()
                                dist_to_best = distance((c.x + dx_c, c.y + dy_c), self.loc)
                                expect = self.expectimax(new_wrld, new_events, depth + 1)
                                expect -= dist_to_best
                                if expect > max_value:
                                    action = (dx_c, dy_c)
                                    max_value = expect
                            else:
                                n = 0  
                                sum_v = 0  
                                for dx_m in [-1, 0, 1]: # Go through the possible moves of the monster
                                    # Avoid out-of-bound indexing
                                    if (m.x + dx_m >= 0) and (m.x + dx_m < wrld.width()):
                                        for dy_m in [-1, 0, 1]:
                                            if (dx_m != 0) or (dy_m != 0):
                                                if (m.y + dy_m >= 0) and (m.y + dy_m < wrld.height()):
                                                    if not wrld.wall_at(m.x + dx_m, m.y + dy_m):
                                                        m.move(dx_m, dy_m)
                                                        (new_wrld, new_events) = wrld.next()
                                                        n += 1  
                                                        sum_v += self.expectimax(new_wrld, new_events, depth + 1)
                                dist_to_best = distance((c.x + dx_c, c.y + dy_c), self.loc)
                                expect = sum_v / n - dist_to_best
                                if expect > max_value:
                                    action = (dx_c, dy_c)
                                    max_value = expect

        return action






    def do(self, wrld):
        # Your code here

        path = aStar((self.x, self.y), wrld.exitcell, wrld)
        if path is not None:
            self.loc = path[0]

        # place bomb asap
        self.place_bomb()
        (dx,dy) = self.expectimax_search(wrld, 0)
        self.move(dx,dy) # Take the move based on expectimax

        return 0

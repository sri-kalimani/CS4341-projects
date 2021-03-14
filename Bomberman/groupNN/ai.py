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
        # d is distance to monster ,higher means stay further away from a monster near u

        self.sensitivity = d

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

        expect_values = []
        c = next(iter(wrld.characters.values()))  # get the character position in the wrld
        c = c[0]

        monster_array = wrld.monsters.values()
        noMonster = 0
        if len(monster_array) == 0:
            noMonster = 1
        elif len(monster_array) == 1:
            m = next(iter(monster_array))[0]
        else:
            m1 = next(iter(monster_array))[0]
            m2 = next(iter(monster_array))[0]
            if max(m1.x - c.x, m1.y - c.y) > max(m2.x - c.x, m2.y - c.y):
                m = m2
            else:
                m = m1

        # Go through the possible 9-moves of the character
        # Loop through delta x
        for dx_c in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (c.x + dx_c >= 0) and (c.x + dx_c < wrld.width()):
                # Loop through delta y
                for dy_c in [-1, 0, 1]:
                    # Avoid out-of-bound indexing
                    if (c.y + dy_c >= 0) and (c.y + dy_c < wrld.height()):
                        # No need to check impossible moves
                        if not wrld.wall_at(c.x + dx_c, c.y + dy_c):
                            # Set move in wrld
                            c.move(dx_c, dy_c)
                            if noMonster:
                                (new_wrld, new_events) = wrld.next()
                                expect = self.expectimax(new_wrld, new_events, depth + 1)
                                expect_values.append(expect)
                            else:
                                n = 0  # number of options for monster actions
                                sum_v = 0  # sum of all monster actions value

                                # Go through the possible 8-moves of the monster
                                # Loop through delta x
                                for dx_m in [-1, 0, 1]:
                                    # Avoid out-of-bound indexing
                                    if (m.x + dx_m >= 0) and (m.x + dx_m < wrld.width()):
                                        # Loop through delta y
                                        for dy_m in [-1, 0, 1]:
                                            # Make sure the monster is moving
                                            if (dx_m != 0) or (dy_m != 0):
                                                # Avoid out-of-bound indexing
                                                if (m.y + dy_m >= 0) and (m.y + dy_m < wrld.height()):
                                                    # No need to check impossible moves
                                                    if not wrld.wall_at(m.x + dx_m, m.y + dy_m):
                                                        # Set move in wrld
                                                        m.move(dx_m, dy_m)
                                                        # Get new world
                                                        (new_wrld, new_events) = wrld.next()
                                                        # do something with new world and events
                                                        n += 1  # number of options for monster movements
                                                        sum_v += self.expectimax(new_wrld, new_events, depth + 1)
                                expect_values.append(sum_v / n)
        v = max(expect_values)
        return v




    def expectimax_action(self, wrld, depth):

        action = (0, 0)
        max_v = -math.inf

        c = next(iter(wrld.characters.values()))  # get the character position in the wrld
        c = c[0]
        monster_array = wrld.monsters.values()
        noMonster = 0
        if len(monster_array) == 0:
            noMonster = 1
        elif len(monster_array) == 1:
            m = next(iter(monster_array))[0]
        else:
            m1 = next(iter(monster_array))[0]
            m2 = next(iter(monster_array))[0]
            if max(m1.x - c.x, m1.y - c.y) > max(m2.x - c.x, m2.y - c.y):
                m = m2  # m2 is closer to c
            else:
                m = m1  # m1 is closer to c

        # Go through the possible 9-moves of the character
        # Loop through delta x
        for dx_c in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (c.x + dx_c >= 0) and (c.x + dx_c < wrld.width()):
                # Loop through delta y
                for dy_c in [-1, 0, 1]:
                    # Avoid out-of-bound indexing
                    if (c.y + dy_c >= 0) and (c.y + dy_c < wrld.height()):
                        # No need to check impossible moves
                        if not wrld.wall_at(c.x + dx_c, c.y + dy_c):
                            # Set move in wrld
                            c.move(dx_c, dy_c)
                            if noMonster:
                                (new_wrld, new_events) = wrld.next()
                                dist_to_best = distance((c.x + dx_c, c.y + dy_c), self.loc)
                                expect = self.expectimax(new_wrld, new_events, depth + 1)
                                expect -= dist_to_best
                                if expect > max_v:
                                    action = (dx_c, dy_c)
                                    max_v = expect
                            else:
                                n = 0  # number of options for monster actions
                                sum_v = 0  # sum of all monster actions value

                                # Go through the possible 8-moves of the monster
                                # Loop through delta x
                                for dx_m in [-1, 0, 1]:
                                    # Avoid out-of-bound indexing
                                    if (m.x + dx_m >= 0) and (m.x + dx_m < wrld.width()):
                                        # Loop through delta y
                                        for dy_m in [-1, 0, 1]:
                                            # Make sure the monster is moving
                                            if (dx_m != 0) or (dy_m != 0):
                                                # Avoid out-of-bound indexing
                                                if (m.y + dy_m >= 0) and (m.y + dy_m < wrld.height()):
                                                    # No need to check impossible moves
                                                    if not wrld.wall_at(m.x + dx_m, m.y + dy_m):
                                                        # Set move in wrld
                                                        m.move(dx_m, dy_m)
                                                        # Get new world
                                                        (new_wrld, new_events) = wrld.next()
                                                        # do something with new world and events
                                                        n += 1  # number of options for monster movements
                                                        sum_v += self.expectimax(new_wrld, new_events, depth + 1)
                                dist_to_best = distance((c.x + dx_c, c.y + dy_c), self.loc)
                                expect = sum_v / n - dist_to_best
                                if expect > max_v:
                                    action = (dx_c, dy_c)
                                    max_v = expect

        return action






    def do(self, wrld):
        # Your code here

        path = aStar((self.x, self.y), wrld.exitcell, wrld)


        # if a_star_move returns none, there is no way to go closer to exit
        if path is not None:
            self.loc = path[0]


        # Place the bomb as soon as I can
        self.place_bomb()


        # Take the move based on expectimax
        (dx,dy) = self.expectimax_action(wrld, 0)

        self.move(dx,dy)

        return

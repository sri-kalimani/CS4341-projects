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

    def __init__(self, name, avatar, x, y, sensitivity):
        CharacterEntity.__init__(self, name, avatar, x, y)
        # sensitivity is a number that weight the distance to monster evaluation
        # higher value means stay further away from nearest monster (usually 100~1000)
        self.sensitivity = sensitivity




    def expectimax_action(self, wrld, depth):

        action = (0, 0)
        max_v = -math.inf

        c = next(iter(wrld.characters.values()))  # get the character position in the wrld
        c = c[0]
        mlist = wrld.monsters.values()
        noMonster = 0
        if len(mlist) == 0:
            noMonster = 1
        elif len(mlist) == 1:
            m = next(iter(mlist))[0]
        else:
            m1 = next(iter(mlist))[0]
            m2 = next(iter(mlist))[0]
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
                                # TODO
                                (new_wrld, new_events) = wrld.next()
                                dist_to_best = distance((c.x + dx_c, c.y + dy_c), self.bestmove)
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
                                dist_to_best = distance((c.x + dx_c, c.y + dy_c), self.bestmove)
                                expect = sum_v / n - dist_to_best  # TODO: adding a weight to the dist_to_best
                                # print("action:", dx_c, dy_c)
                                # print("value:", expect)
                                if expect > max_v:
                                    action = (dx_c, dy_c)
                                    max_v = expect
        # print("max action:", action)
        # print("max value:", max_v)
        return action

    # go through the event list to see if the wrld is terminated
    # Event.tpe: the type of the event. It is one of Event.BOMB_HIT_WALL,
    # Event.BOMB_HIT_MONSTER, Event.BOMB_HIT_CHARACTER,
    # Event.CHARACTER_KILLED_BY_MONSTER, Event.CHARACTER_FOUND_EXIT.


    def expectimax(self, wrld, events, depth):

        for event in events:
            if event.tpe == event.BOMB_HIT_CHARACTER or event.tpe == event.CHARACTER_KILLED_BY_MONSTER:
                # character is dead so worst evaluation
                return -10000000000
            elif event.tpe == event.CHARACTER_FOUND_EXIT:
                # character is winning so best evaluation
                return 10000000
        if depth >= 2:
            # reached searching depth, evaluate the wrld
            return self.evaluation(wrld)

        expect_values = []
        c = next(iter(wrld.characters.values()))  # get the character position in the wrld
        c = c[0]  # c was a list
        # TODO here need fix bug when no monster, will be killed by bomb
        # TODO add support for 0/1/2 monsters


        mlist = wrld.monsters.values()
        noMonster = 0
        if len(mlist) == 0:
            noMonster = 1
        elif len(mlist) == 1:
            m = next(iter(mlist))[0]
        else:
            m1 = next(iter(mlist))[0]
            m2 = next(iter(mlist))[0]
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
                                # TODO:
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

    # param: wrld
    # def:
    #   wrld
    # return: evaluation value
    def evaluation(self, wrld):
        c = next(iter(wrld.characters.values()))
        c = c[0]

        if len(wrld.monsters.values()) == 0: return 0
        mlist = next(iter(wrld.monsters.values()))
        score = 0
        for m in mlist:
            distx = abs(c.x - m.x)
            disty = abs(c.y - m.y)
            if distx <= 2 and disty <= 2:
                if distx <= 1 and disty <= 1:
                    score -= 100000
                score -= 10000
            score -= self.sensitivity / (distx+disty)**2
        return score





    def do(self, wrld):
        # Your code here
        # 1. go through the map and find current condition
        # 2. determine state(Ex. safe, monster, bomb, monster&bomb)
        # 3. move or bomb according to state

        #
        pos = (self.x, self.y)
        path = aStar(pos, wrld.exitcell, wrld)

        # (threaten, escape_x, escape_y) = self.threatens(c_position, wrld) # currently not using threaten function

        # if a_star_move returns none, there is no way to go closer to exit
        if path is not None:
            self.bestmove = path[0]
        # print(self.bestmove)

        # Place the bomb as soon as I can
        self.place_bomb()


        # Take the move based on expectimax
        (dx,dy) = self.expectimax_action(wrld, 0)

        self.move(dx,dy)

        return

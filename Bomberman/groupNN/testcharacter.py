# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import astar

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here

        # self.move(1,0)
        '''
        variant 1: 
        if neighbor is exit, move to neighbor
        to move in to a cell: check if empty, and no wall
        '''

        # print("EXIT = ", wr)
        path = astar.AStar(wrld, (0,0), wrld.exitcell)
        cell = path.pop(0)


        while cell != wrld.exitcell:
            print("Cell: ", cell)
            self.move(cell[0], cell[1])
            cell = path.pop(0)


        # pass


    # def getNeighbors(wrld, dx, dy):
    #     neighbors = []
    #     i = 1
    #     j = 0
    #     for n in range(0 , 7):
    #         if wrld.empty(dx+i, dy+j):
    #             neighbors.append(dx+i, dy+j)
    #         i

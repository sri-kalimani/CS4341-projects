# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from Astar import AStar

class TestCharacter(CharacterEntity):

    def do(self, wrld):

        print(AStar(wrld,(0,0),wrld.exitcell))







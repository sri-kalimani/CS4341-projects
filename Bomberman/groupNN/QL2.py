import math
import copy
import random
import csv

# This needs to happen before the system path is changed
# from helper import AStar
# from helper import getFutureExp
import helper

# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from sensed_world import SensedWorld
from events import Event

class Agent(CharacterEntity):

    def __init__(self, name, avatar, x, y, initPath, outPath, training, randomMove):
        super(Agent, self).__init__(name, avatar, x, y)
        
        self.training = training
        self.lastWrld = None
        self.outPath = outPath
        self.randomMove = randomMove
        self.me = None
        random.seed()
        
        with open(initPath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                feat = row['Feature']
                val = float(row['Weight'])
                
                if feat == 'wg':
                    self.wg = val # Weight of A* distance from the goal.
                elif feat == 'we':
                    self.we = val # Weight of A* distance from the nearest enemy.
                elif feat == 'wpx':
                    self.wpx = val # Weight of player being in explosion.
                elif feat == 'wex':
                    self.wex = val # Weight of an enemy being in explosion.
                elif feat == 'wwx':
                    self.wwx = val # Weight of a wall being in an explosion.

    def r(self, wrld):
        reward = helper.Astar(wrld, (self.me.x, self.me.y), wrld.exitcell) # Baseline reward
        if reward is not None:
            reward = -reward
        else:
            reward = -(abs(self.me.x - wrld.exitcell[0]) + abs(self.me.y - wrld.exitcell[1]))

        for e in wrld.events:
            if e.tpe == Event.BOMB_HIT_WALL and e.character == self:
                reward += 400
            elif e.tpe == Event.BOMB_HIT_MONSTER and e.character == self:
                reward += 70
            elif e.tpe == Event.BOMB_HIT_CHARACTER:
                if e.character != e.other and e.character == self:  # our character killed other character
                    reward += 100
                elif e.character != e.other:  # if other character (not ours) was killed - that's good!
                    reward += 50
                else:
                    # Killed himself or was killed by other character
                    reward -= 1000
            elif e.tpe == Event.CHARACTER_KILLED_BY_MONSTER and e.character == self:
                reward -= 1000
            elif e.tpe == Event.CHARACTER_FOUND_EXIT and e.character == self:
                reward += 1000

        # If character died but it is not shown in the events
        if len(wrld.events) == 0 and len(wrld.characters) == 0:
            reward -= 1000

        return reward

    def q(self, wrld):
        return (self.wg * self.fg(wrld)  # Distance from goal
                + self.we * math.exp(self.fe(wrld))  # Distance from enemy scales exponentially
               + self.wpx * self.fpx(wrld)               # The player being in an explosion
               + self.wex * self.fex(wrld)               # Enemies in an explosion
               + self.wwx * self.fwx(wrld)               # Walls in an explosion
        )
    
    # Normalized A* distance from the goal. Normalized against the largest dimension
    # of the map. The range is [0,inf). 1000 is returned on failure to find.
    #
    # PARAM [world] wrld: The current game state.
    # RETURN [float]: The normalized distance from the goal.
    def fg(self, wrld):
        # This either uses the current character state, or the character state before the game ended.
        if hasattr(wrld, 'me') and wrld.me(self) is not None:
            char = wrld.me(self)
        else:
            char = self.me

        dist = helper.Astar(wrld, (char.x, char.y), wrld.exitcell)

        # If a path wasn't found, return an manhatten distance
        if dist == None:
            return abs(char.x - wrld.exitcell[0]) + abs(char.y - wrld.exitcell[1])
        
        # Otherwise return the normalized distance
        else:
            return dist / max(wrld.width(), wrld.height())

    # Normalized A* distance from the nearest enemy. Normalized against the largest
    # dimension of the map. The range is [0,1000/max(height, width)].
    #
    # PARAM [(world] wrld: The current game state.
    # RETURN [float]: The normalized distance from the goal.
    def fe(self, wrld):
        # Max of e: A*(p, e)
        dist = None # Start with an arbitrarily large distance
        # This either uses the current character state, or the character state before the game ended.
        if hasattr(wrld, 'me') and wrld.me(self) is not None:
            char = wrld.me(self)
        else:
            char = self.me

        # Get the minimum distance from all enemies.
        if char is not None:
            for monList in wrld.monsters.values():
                for mon in monList:
                    tmp = helper.Astar(wrld, (char.x, char.y), (mon.x, mon.y))
                    if dist is None or (tmp is not None and tmp < dist):
                        dist = tmp
        
        # If no enemies or paths to enemy 
        if dist is None:
            dist = 0

        return dist / max(wrld.width(), wrld.height())

    # Whether or not the character is in an explosion. This feature does not care
    # about future explosions, and makes the assumption that the character will
    # always be able to sidestep an explosion.
    def fpx(self, wrld):
        if hasattr(wrld, 'me') and wrld.me(self) is not None:
            char = wrld.me(self)
        else:

            # If world has no characters or events
            if len(wrld.events) == 0:
                return 0
            char = wrld.events[0].character
        
        # If the character is in an explosion, return 1
        if char is not None and wrld.explosion_at(char.x, char.y):
            return 1
        
        # Check around each bomb for the player
        for bomb in wrld.bombs.values():
            # Only care about being in path when timer gets low
            if bomb.timer < 2:
                for exp in helper.getFutureExp(bomb, wrld.width(), wrld.height()):
                    # Check if player will be in future explosion
                    if (char.x,char.y) == (exp[0], exp[1]):
                        return 1

        return 0

    def fex(self, wrld):
        count = 0 # Number of monsters in explosions
        
        # Check each monster for an explosion
        for monList in wrld.monsters.values():
            for mon in monList:
                if wrld.explosion_at(mon.x, mon.y):
                    count += 1

        # Check around each bomb for monstesr
        for bomb in wrld.bombs.values():
            for exp in helper.getFutureExp(bomb, wrld.width(), wrld.height()):
                if wrld.monsters_at(exp[0], exp[1]):
                    count += 1
    
        return count

    def fwx(self, wrld):
        count = 0 # Number of walls in explosions and future explosions

        # Check each explosion for a wall
        for exp in wrld.explosions.values():
            if wrld.wall_at(exp.x, exp.y):
                count += 1

        # Check around each bomb for walls
        for bomb in wrld.bombs.values():
            for exp in helper.getFutureExp(bomb, wrld.width(), wrld.height()):
                if wrld.wall_at(exp[0], exp[1]):
                    count += 1
        
        return count

    def localDelta(self, lastWrld, wrld):
        gamma = 1

        return self.r(lastWrld) + gamma*self.q(wrld) - self.q(lastWrld)

    def updateWeights(self, lastWrld, wrld):
        delta = self.localDelta(lastWrld, wrld)
        alpha = 0.005

        self.wg = self.wg + alpha * delta * self.fg(lastWrld)
        self.we = self.we + alpha * delta * self.fe(lastWrld)
        self.wpx = self.wpx + alpha * delta * self.fpx(lastWrld)
        self.wex = self.wex + alpha * delta * self.fex(lastWrld)
        self.wwx = self.wwx + alpha * delta * self.fwx(lastWrld)

        with open(self.outPath, 'w', newline='') as f:
            fieldnames = ['Feature', 'Weight']  # Table headers
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            # Write to rows by referencing header and then putting value
            writer.writerow({'Feature': 'wg', 'Weight': self.wg})
            writer.writerow({'Feature': 'we', 'Weight': self.we})
            writer.writerow({'Feature': 'wpx', 'Weight': self.wpx})
            writer.writerow({'Feature': 'wex', 'Weight': self.wex})
            writer.writerow({'Feature': 'wwx', 'Weight': self.wwx})


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
                

    def forceToGoal(self, wrld, action):
        g = wrld.exitcell
        x = self.me.x
        y = self.me.y
        
        # All the cases where they may be adjacent:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (x + dx, y + dy) == g:
                    return (dx, dy, False)

        return action

    def do(self, wrld):
        if wrld.me is not None:
            self.me = wrld.me(self)

        maxQ = None # Start with no maxQ
        maxState = None # Start with no next state

        for i in self.getStates(wrld):
            tmpQ = self.q(i[0]) # This runs A* several times, so we only want to run it once
            if maxQ == None or tmpQ > maxQ:
                maxQ = tmpQ
                maxState = i

        # Random walk chance
        if random.random() <= self.randomMove:
            maxState = random.choice(self.getStates(wrld))

        # Force it to go into the goal if it's adjacant
        

        maxMove = maxState[1]
        maxMove = self.forceToGoal(maxState[0], maxMove)
        self.move(maxMove[0], maxMove[1])
        if maxMove[2]:
            self.place_bomb()

        if self.training:
            if self.lastWrld is not None:
                self.updateWeights(self.lastWrld, wrld)
            
            self.lastWrld = wrld

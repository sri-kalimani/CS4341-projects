import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue
import math
from colorama import Fore, Back
# Pythagorean distance.
def Distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# absolute distance between tuples
def distance( a, b):
    (x1, y1) = a
    (x2, y2) = b
    d = abs(x1 - x2) + abs(y1 - y2)

    return d

def distance2( x, y):
		return abs(x[0] - y[0]) + abs(x[1] - y[1])




# distance bettween agent and monster
def monster_distance( ai, mo):
    x1, y1 = ai
    x2, y2 = mo

    d = math.sqrt((abs(x2 - x1) * abs(y2 - y1)) + (abs(x2 - x1) * abs(y2 - y1)))
    print(d,"distance")
    if (d == 0):
        return 1
    return 2/d


# A*
#
# PARAM [wrld] wrld: The curr game state.
# PARAM [(int,int)] start: The cell to start from.
# PARAM [(int,int)] dest: The destination cell.
def Astar(wrld, start, dest):
    cameFrom = {}
    g = {start: 0}
    frontier = PriorityQueue()
    frontier.put(start, 0)
    
    

    while not frontier.empty():
        curr = frontier.get()

        #If we are at the destination
        if curr == dest:
            break

        for direction in [(1, 0), (-1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 0)]:
            next_cell = (curr[0] + direction[0], curr[1] + direction[1])
            if next_cell[0] < 0 or next_cell[0] >= wrld.width() or next_cell[1] < 0 or next_cell[1] >= wrld.height():
                continue
            if wrld.wall_at(next_cell[0], next_cell[1]):
                for dir2 in [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, -1), (0, 1)]:
                    if wrld.bomb_at(next_cell[0] + dir2[0], next_cell[1] + dir2[1]):
                        cost = 100
                    else:
                        cost = 100
            elif wrld.explosion_at(next_cell[0], next_cell[1]):
                cost = math.inf
            elif wrld.monsters_at(next_cell[0], next_cell[1]):
                cost = math.inf
            elif wrld.bomb_at(next_cell[0], next_cell[1]):
                cost = math.inf
            else:
                cost = 1

            for dir2 in [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, -1), (0, 1)]:
                if wrld.monsters_at(next_cell[0] + dir2[0], next_cell[1] + dir2[1]):
                    cost = 5

            for dir2 in [(2, 0), (2, 1), (2, 2), (2, -1), (2, -2), (-2, 0), (-2, 1), (-2, 2), (-2, -1), (-2, -2),
                         (0, 2), (1, 2), (-1, 2), (0, -2), (1, -2), (-1, -2)]:
                if wrld.monsters_at(next_cell[0] + dir2[0], next_cell[1] + dir2[1]):
                    cost = 3

            new_cost = g[curr] + cost
            if next_cell not in g or new_cost < g[next_cell]:
                g[next_cell] = new_cost
                priority = new_cost +Distance(dest, next_cell)
                frontier.put(next_cell, priority)
                cameFrom[next_cell] = curr
    curr = dest
    path = []
    while curr != start:
        path.append(curr)
        curr = cameFrom[curr]
    path.append(start)
    path.reverse()
    return path

# param: start is a start node as tuple (x, y)
#        goal is a goal node as tuple (x, y)
#        wrld is the current world
# return: the best next node towards exit
def aStar(start, goal, wrld):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in eCell(current, wrld):
            new_cost = cost_so_far[current] + 1  # cost from one node to its neighbor is 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost +distance(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    min =math.inf
    # search if we can reach goal
    for next in came_from:
        dis_to_goal = distance(next, goal)
        if dis_to_goal < min:
            min = dis_to_goal
            min_to_exit = next
    if next == goal:
        # we can reach goal
        while came_from[next] is not None:
            # set_cell_color(next[0], next[1], Fore.RED + Back.RED)
            if came_from[next] == start:
                return next, "success"  # next move from start to in the A* path
            next = came_from[next]

    while came_from[min_to_exit] is not None:
        # set_cell_color(min_to_exit[0], min_to_exit[1], Fore.RED + Back.RED)
        if came_from[min_to_exit] == start:
            return min_to_exit, "error! no path " # next move from start to in the A* path
        min_to_exit = came_from[min_to_exit]

    # goal can not be reached
    # return a move that get close to the goal
    return None




def isWall( x, y, wrld):
    if (x > 0 and x < wrld.width()):
        if (y > 0 and y < wrld.height()):
            if not wrld.wall_at(x, y):
                return True
    return False


# go through cells and assign scores
def score_cell(wrld, loc):
    x = loc[0]
    y = loc[1]
    # Go through neighboring cells
    count = 0

    for dx in [-2, 0, 2]:
        #  out-of-bounds
        if not ((x + dx >= 0) or not (x + dx < wrld.width())):
            count += 2
        if (x + dx >= 0) and (x + dx < wrld.width()):
            for dy in [-2, 0, 2]:
                # out-of-bounds
                if not ((y + dy >= 0) or not (y + dy < wrld.height())):
                    count += 2
                if (y + dy >= 0) and (y + dy < wrld.height()):
                    # Is this cell any good?
                    if wrld.wall_at(x + dx, y + dy):
                        count += 1


    return count

def inRange( x, y, wrld):
    if (x > 0 and x < wrld.width()):
        if (y > 0 and y < wrld.height()):
            return True
    return False

def mon_inRange(x,y ,wrld):
    for i in range(-4, 5):
        if wrld.monsters_at(x + i, y):
            return True
    for j in range(-4, 5):
        if wrld.monsters_at(x, y + j):
            return True
    return False


# distance to bomb
def bomb_distance( x, y, wrld):
    distance = 0
    for dx in range(-5,10):
        if inRange(x + dx, y, wrld):
            if wrld.bomb_at(x + dx, y):
                distance = abs(dx)
    for dy in range(-5, 10):
        if inRange(x, y + dy, wrld):
            if wrld.bomb_at(x, y + dy):
                distance = abs(dy)


    return distance



# returns all valid neighbors
def neighbors2( wrld, x, y):

    cells = []

    for dx in [-1, 0, 1]:

        if ((x + dx >= 0) and (x + dx < wrld.width())):
            for dy in [-1, 0, 1]:

                if ((y + dy >= 0) and (y + dy < wrld.height())):

                    if not wrld.explosion_at(x + dx, y + dy):
                        cells.append((x + dx, y + dy))

    return cells

def eCell( node, wrld):
    # List of empty cells
    cells = []
    # Go through neighboring cells
    for dx in [-1, 0, 1]:
        # Avoid out-of-bounds access
        if (node[0] + dx >= 0) and (node[0] + dx < wrld.width()):
            for dy in [-1, 0, 1]:
                # Avoid out-of-bounds access
                if (node[1] + dy >= 0) and (node[1] + dy < wrld.height()):
                    # Is this cell safe?
                    if wrld.exit_at(node[0] + dx, node[1] + dy) or wrld.empty_at(node[0] + dx, node[1] + dy):
                        # Yes
                        if not (dx == 0 and dy == 0):
                            cells.append((node[0] + dx, node[1] + dy))
    # All done
    return cells


def boom(wrld):
    for x in range(wrld.width()):
        for y in range(wrld.height()):
            if wrld.explosion_at(x, y):
                return True
    return False


# param: wrld
# def:
#   wrld
# return: evaluation value
def eval(sens, wrld):
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
        score -= sens / (distx+disty)**2
    return score


def neighbors(wrld, curr):
    neighbors = [curr]

    for dx in [-1, 0, 1]:
        if (curr[0] + dx >= 0) and (curr[0] + dx < wrld.width()):
            for dy in [-1, 0, 1]:
                if (curr[1] + dy >= 0) and (curr[1] + dy < wrld.height()):
                    if not wrld.wall_at(curr[0] + dx, curr[1] + dy):
                        neighbors.append((curr[0] + dx, curr[1] + dy))
    return neighbors
# function to check if a cell will explode next turn
def exp(f ,x, y,loc):
    if (f <= 2) and f != -1:
        if (x, y) in loc:
            return True
    return False

def isEmpty( x, y, wrld):
    empty = 0
    for dx in range(-1, 2, 1):
        for dy in range(-1, 2, 1):
            if (inRange(x + dx, y + dy, wrld)):
                if (wrld.empty_at(x + dx, y + dy)):
                    empty += 1
    return empty



# return true if a monster is present within a certain radius of a location
def isMon(wrld, x, y, r):
    # Go through neighboring cells
    for dx in range(-r, r):
        # Avoid out-of-bounds access
        if ((x + dx >= 0) and (x + dx < wrld.width())):
            for dy in range(-r, r):
                # Avoid out-of-bounds access
                if ((y + dy >= 0) and (y + dy < wrld.height())):

                    if wrld.monsters_at(x + dx, y + dy):

                        return True
    return False


# Returns x, y coordinate of monster
def monCoor( wrld, x, y, radius):
    for dx in range(-radius, radius):
        if ((x + dx >= 0) and (x + dx < wrld.width())):
            for dy in range(-radius, radius):
                if ((y + dy >= 0) and (y + dy < wrld.height())):
                    if wrld.monsters_at(x + dx, y + dy):
                        return (x + dx, y + dy)


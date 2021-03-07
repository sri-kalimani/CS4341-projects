import heapq
import math
from queue import PriorityQueue
from math import sqrt

# Pythagorean distance.
def Distance(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

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

def isWall( x, y, wrld):
    if (x > 0 and x < wrld.width()):
        if (y > 0 and y < wrld.height()):
            if not wrld.wall_at(x, y):
                return True
    return False


def inRange( x, y, wrld):
    if (x > 0 and x < wrld.width()):
        if (y > 0 and y < wrld.height()):
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





# distance bettween agent and monster
def monster_distance( ai, mo):
    x1, y1 = ai
    x2, y2 = mo

    d = sqrt((abs(x2 - x1) * abs(y2 - y1)) + (abs(x2 - x1) * abs(y2 - y1)))
    print(d,"distance")
    if (d == 0):
        return 1
    return 2/d





def neighbors(wrld, curr):
    neighbors = [curr]

    # Loop through x directions
    for dx in [-1, 0, 1]:
        # Check that x coordinate is within grid
        if (curr[0] + dx >= 0) and (curr[0] + dx < wrld.width()):
            # Loop through y directions
            for dy in [-1, 0, 1]:
                # Check that y coordinate is within grid
                if (curr[1] + dy >= 0) and (curr[1] + dy < wrld.height()):
                    # Add to list of neighbors if new cell is not a wall
                    if not wrld.wall_at(curr[0] + dx, curr[1] + dy):
                        neighbors.append((curr[0] + dx, curr[1] + dy))
    return neighbors


def isEmpty( x, y, wrld):
    empty = 0
    for dx in range(-1, 2, 1):
        for dy in range(-1, 2, 1):
            if (inRange(x + dx, y + dy, wrld)):
                if (wrld.empty_at(x + dx, y + dy)):
                    empty += 1
    return empty
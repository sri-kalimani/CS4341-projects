from queue import PriorityQueue
from math import sqrt


def pythDist(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def AStar(wrld, start, dest):
    # Initialize data structures.
    cameFrom = {}
    g = { start : 0 }
    frontier = PriorityQueue()
    frontier.put((0, start))

    while not frontier.empty():
        cur = (frontier.get())[1]

        # If we're at the destination.
        if cur == dest:
            # Get length of path...
            length = 0
            while cur != start:
                length += 1
                cur = cameFrom[cur]

            # ...And then return it
            return length

        # Otherwise touch all neighbors
        for i in neighbors(wrld, cur):
            # Tentative cost is the path to current plus 1 because all cells are identical
            cost = g[cur] + 1

            # If the tentative cost is better, then assign it and put it on the frontier
            if i not in g or cost < g[i]:
                # Just putting this on without removing any potential previous entries uses more memory
                # than is strictly required, but it shouldn't end up using so much memory that it becomes a
                # a problem. Memory useage is still linear.
                frontier.put((cost + pythDist(i, dest), i))
                g[i] = cost
                cameFrom[i] = cur

    # In case of failure, return None
    return None


# Finds neighboring cells around a given cell for A*
#
# PARAM [world] wrld: current state of world
# PARAM [(int, int)] current: current cell being examined
# RETURN [ [(int, int)] ]: list of coordinates of neighboring cells
def neighbors(wrld, current):
    neighbors = [current]

    # Loop through x directions
    for dx in [-1, 0, 1]:
        # Check that x coordinate is within grid
        if (current[0] + dx >= 0) and (current[0] + dx < wrld.width()):
            # Loop through y directions
            for dy in [-1, 0, 1]:
                # Check that y coordinate is within grid
                if (current[1] + dy >= 0) and (current[1] + dy < wrld.height()):
                    # Add to list of neighbors if new cell is not a wall
                    if not wrld.wall_at(current[0] + dx, current[1] + dy):
                        neighbors.append((current[0] + dx, current[1] + dy))
    return neighbors



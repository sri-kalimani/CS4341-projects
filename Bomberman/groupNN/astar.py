from queue import PriorityQueue
from math import sqrt

# Pythagorean distance.
#
# PARAM [(int,int)] a,b: The points to get the distance between.
def pythDist(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# A*
#
# PARAM [world] wrld: The current game state.
# PARAM [(int,int)] start: The cell to start from.
# PARAM [(int,int)] dest: The destination cell.
def AStar(wrld, start, dest):
    # Initialize data structures.
    cameFrom = {}
    g = { start : 0 }
    frontier = PriorityQueue()
    frontier.put((0, start))
    path = []


    while not frontier.empty():
        cur = (frontier.get())[1]
        # print("Currently seatchng: ", cur)

        # If we're at the destination.
        if cur == dest:            
            cur = dest
            while cur != start:
                path.insert(0, cur)
                cur = cameFrom[cur]

            return path
        # Otherwise touch all neighbors
        for i in neighbors(wrld, cur):
            # print()
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

        # return None


     
    # In case of failure, return None
    # return path
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

def getFutureExp(bomb, w, h):
        x = bomb.x
        y = bomb.y
        cells = []

        # The bomb itself
        cells.append((x, y))

        # The left arm
        if x - 1 >= 0:
            cells.append((x-1, y))
        if x - 2 >= 0:
            cells.append((x-2, y))
        if x - 3 >= 0:
            cells.append((x-3, y))
        if x - 4 >= 0:
            cells.append((x-4, y))

        # The right arm
        if x + 1 < w:
            cells.append((x+1, y))
        if x + 2 < w:
            cells.append((x+2, y))
        if x + 3 < w:
            cells.append((x+3, y))
        if x + 4 < w:
            cells.append((x+4, y))

        # The top arm
        if y - 1 >= 0:
            cells.append((x, y-1))
        if y - 2 >= 0:
            cells.append((x, y-2))
        if y - 3 >= 0:
            cells.append((x, y-3))
        if y - 4 >= 0:
            cells.append((x, y-4))

        # The bottom arm
        if y + 1 < h:
            cells.append((x, y+1))
        if y + 2 < h:
            cells.append((x, y+2))
        if y + 3 < h:
            cells.append((x, y+3))
        if y + 4 < h:
            cells.append((x, y+4))

        return cells

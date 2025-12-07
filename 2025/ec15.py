from collections import deque, defaultdict
from heapq import heappop, heappush

from shapely import LineString, Point

notes = "L6,L3,L6,R3,L6,L3,L3,R6,L6,R6,L6,L6,R3,L3,L3,R3,R3,L6,L6,L3"
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
dir = 0
pos = 0, 0
nodes = [(0, 0)]


def mark(r, c):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nodes.append((r + dr, c + dc))


mark(0, 0)


def lines_overlap(line1, line2):
    return LineString(line1).intersects(LineString(line2))


lines = []
minr, maxr, minc, maxc = 0, 0, 0, 0

for instr in notes.split(","):
    d, num = instr[0], int(instr[1:])
    if d == "R":
        dir += 1
    else:
        dir -= 1
    dir %= len(dirs)

    r, c = pos[0] + dirs[dir][0] * num, pos[1] + dirs[dir][1] * num
    mark(r, c)

    minr = min(minr, r)
    maxr = max(maxr, r)
    minc = min(minc, c)
    maxc = max(maxc, c)

    if pos == (0, 0):
        pos = pos[0] + dirs[dir][0], pos[1] + dirs[dir][1]
    lines.append((pos, (r, c)))
    pos = (r, c)

nodes.append((0, 0))
nodes.append(pos)

lines[-1] = (lines[-1][0], (pos[0] + dirs[dir][0] * -1, pos[1] + dirs[dir][1] * -1))
G = defaultdict(list)
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        n1, n2 = nodes[i], nodes[j]
        if n1 == n2:
            continue
        route = (n1, n2)

        if not any(lines_overlap(route, line) for line in lines):
            G[n1].append(n2)
            G[n2].append(n1)



Q = [(0, (0, 0))]
costs = {(0, 0): 0}
while Q:
    cost, (r, c) = heappop(Q)
    if cost != costs[(r, c)]:
        continue

    if (r, c) == pos:
        print(cost)
        break
    for nb in G[(r, c)]:
        nbr, nbc = nb
        route = ((r, c), (nbr, nbc))
        nb_cost = cost + abs(r - nbr) + abs(c - nbc)
        if (nbr, nbc) not in costs or nb_cost < costs[(nbr, nbc)]:
            costs[(nbr, nbc)] = nb_cost
            heappush(Q, (nb_cost, nb))

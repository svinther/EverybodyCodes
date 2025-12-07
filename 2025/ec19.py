from collections import deque, defaultdict
from heapq import heappop, heappush


def parse(notes: str) -> list[tuple[int, int, int]]:
    ans = []
    for t in notes.split("\n"):
        t = t.strip()
        if not t:
            continue
        ans.append([int(x.strip()) for x in t.split(",")])
    return ans


def is_wall(rc: tuple[int, int], parsed_notes: list[tuple[int, int, int]]) -> bool:
    r, c = rc
    walls_for_c = []
    for wall_c, wall_o_start, wall_o_height in parsed_notes:
        if wall_c < c:
            continue
        if wall_c > c:
            break
        walls_for_c.append((wall_o_start, wall_o_height))

    if not walls_for_c:
        return False

    if any(
        wall_o_start <= r < wall_o_start + wall_o_height
        for wall_o_start, wall_o_height in walls_for_c
    ):
        return False
    return True


def p1(notes: str):
    parsed_notes = parse(notes)
    seen = {(0, 0)}
    Q = deque([((0, 0), 0)])
    while Q:
        (r, c), cost = Q.popleft()
        if c == parsed_notes[-1][0]:
            return cost
        for dr, dc in [(-1, 1), (1, 1)]:
            nbr, nbc = r + dr, c + dc
            if nbr <= 0:
                continue
            if (nbr, nbc) in seen:
                continue
            if is_wall((nbr, nbc), parsed_notes):
                continue
            seen.add((nbr, nbc))
            Q.append(((nbr, nbc), cost + (1 if dr == 1 else 0)))


def p3(notes: str):
    parsed_notes = parse(notes)
    nodes_r_by_c = defaultdict(set)
    for c, r0, rh in parsed_notes:
        for r in range(r0, r0 + rh):
            nodes_r_by_c[c].add(r)
    sorted_c = sorted(list(nodes_r_by_c.keys()))

    costs = {(0, 0): 0}
    Q = [(0, (0, 0), -1)]
    while Q:
        cost, (r, c), c_idx = heappop(Q)
        if costs[(r, c)] != cost:
            continue
        if c_idx == len(sorted_c) - 1:
            return cost
        nbc = sorted_c[c_idx + 1]
        for nbr in nodes_r_by_c[nbc]:
            dist_c = nbc - c
            dist_r = nbr - r
            if abs(dist_r) > dist_c:
                continue
            if dist_c % 2 != dist_r % 2:
                continue

            nb_cost = cost
            if dist_r > 0:
                nb_cost += dist_r
                nb_cost += (dist_c - dist_r) // 2
            else:
                nb_cost += (dist_c + dist_r) // 2

            if (nbr, nbc) not in costs or nb_cost < costs[(nbr, nbc)]:
                costs[(nbr, nbc)] = nb_cost
                heappush(Q, (nb_cost, (nbr, nbc), c_idx + 1))


small_notes = """\
7, 7, 2
12, 0, 4
15, 5, 3
24, 1, 6
28, 5, 5
40, 8, 2
"""

p1_notes = """\
xxx
"""

p2_small_notes = """\
7,7,2
7,1,3
12,0,4
15,5,3
24,1,6
28,5,5
40,3,3
40,8,2
"""

p2_notes = """\
xxx
"""

p3_notes = """\
xxx
"""

print("p1 small", p1(small_notes))

print("p1", p1(p1_notes))

print("p2 small", p1(p2_small_notes))

print("p2", p1(p2_notes))

print("p3 small_p2_notes", p3(p2_small_notes))

print("p3 p2 notes", p3(p2_notes))

print("p3 p1 notes", p3(p1_notes))

print("p3 p1_small_notes", p3(small_notes))

print("p3", p3(p3_notes))

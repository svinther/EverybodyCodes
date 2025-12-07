from functools import reduce
from operator import mul

def parse_notes(notes: str) -> list[int]:
    return list(map(int, notes.split(",")))


def block_count(spell: list[int], i) -> int:
    col = sum(i % n == 0 for n in spell)
    return col


def compute_spell(blockcounts: list[int]) -> str:
    rnotes = []
    for i in range(1, len(blockcounts) + 1):
        if blockcounts[i - 1] == 1:
            for j in range(1, len(blockcounts) + 1):
                if j % i == 0:
                    blockcounts[j - 1] -= 1
            rnotes.append(str(i))
    return ",".join(rnotes)

def p1(notes: str):
    spell = parse_notes(notes)
    block_counts = [block_count(spell, i) for i in range(1, 91)]
    return sum(block_counts)


def p2(notes: str):
    block_counts = parse_notes(notes)
    spell = compute_spell(block_counts)
    return reduce(mul, parse_notes(spell))


def p3(notes: str, block_limit: int):
    block_counts = parse_notes(notes)
    spell = compute_spell(block_counts)
    spell = parse_notes(spell)

    def helper(size):
        return sum(size // s for s in spell)

    hi = 10**30
    lo = 1
    while lo < hi:
        mid = 1 + lo + (hi - lo) // 2
        res = helper(mid)
        if res > block_limit:
            hi = mid - 1
        else:
            lo = mid
    assert lo == hi
    return hi


p1_notes = "xxx"
print("p1", p1(p1_notes))

p2_notes = "xxx"
print("p2", p2(p2_notes))

p3_limit = 202520252025000
p3_notes = "xxx"
print("p3", p3(p3_notes, p3_limit))

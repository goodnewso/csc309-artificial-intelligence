"""puzzle8.py: how much a good heuristic saves on the 8-puzzle.

A state is a tuple of 9 numbers read row by row; 0 is the blank.
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "u06-uninformed"))
from search import Problem, breadth_first, astar          # noqa: E402

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVES = {"up": -3, "down": 3, "left": -1, "right": 1}   # blank's moves


def misplaced(s):                        # h1: tiles out of place
    return sum(1 for i, t in enumerate(s) if t and t != GOAL[i])


def manhattan(s):                        # h2: total city-block distance
    total = 0
    for i, t in enumerate(s):
        if t:
            g = t - 1                    # goal index of tile t
            total += abs(i // 3 - g // 3) + abs(i % 3 - g % 3)
    return total


class Puzzle(Problem):
    def __init__(self, start, h=lambda s: 0):
        super().__init__(start)
        self.hfun = h

    def actions(self, s):
        b = s.index(0)
        acts = []
        if b >= 3: acts.append("up")
        if b < 6: acts.append("down")
        if b % 3: acts.append("left")
        if b % 3 < 2: acts.append("right")
        return acts

    def result(self, s, a):
        b = s.index(0)
        t = b + MOVES[a]
        s = list(s)
        s[b], s[t] = s[t], s[b]
        return tuple(s)

    def is_goal(self, s):
        return s == GOAL

    def h(self, s):
        return self.hfun(s)


if __name__ == "__main__":
    start = (8, 6, 7, 2, 5, 4, 3, 0, 1)
    print("start:", start[:3], start[3:6], start[6:])
    print(f"h1 = {misplaced(start)}, h2 = {manhattan(start)}\n")
    print(f"{'method':20}{'moves':>6}{'expanded':>10}")
    for name, algo, h in [("breadth-first", breadth_first, None),
                          ("A* with h1", astar, misplaced),
                          ("A* with h2", astar, manhattan)]:
        prob = Puzzle(start, h) if h else Puzzle(start)
        goal, stats = algo(prob)
        print(f"{name:20}{goal.depth:>6}{stats['expanded']:>10}")

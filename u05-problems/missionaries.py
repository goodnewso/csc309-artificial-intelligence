"""missionaries.py: the missionaries-and-cannibals problem as a state space.

State (m, c, b): missionaries and cannibals on the LEFT bank, and b = 1
if the boat is on the left.  Start (3, 3, 1); goal (0, 0, 0).
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "u06-uninformed"))
from search import Problem                              # noqa: E402

LOADS = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]       # (m, c) in boat


def safe(m, c):
    """No bank may have missionaries outnumbered by cannibals."""
    left_ok = m == 0 or m >= c
    right_ok = (3 - m) == 0 or (3 - m) >= (3 - c)
    return 0 <= m <= 3 and 0 <= c <= 3 and left_ok and right_ok


class Missionaries(Problem):
    def __init__(self):
        super().__init__((3, 3, 1))

    def actions(self, s):
        m, c, b = s
        sign = -1 if b == 1 else 1          # boat leaves the left bank
        return [(dm, dc) for dm, dc in LOADS
                if safe(m + sign * dm, c + sign * dc)]

    def result(self, s, a):
        m, c, b = s
        sign = -1 if b == 1 else 1
        return (m + sign * a[0], c + sign * a[1], 1 - b)

    def is_goal(self, s):
        return s == (0, 0, 0)


if __name__ == "__main__":
    p = Missionaries()
    states = [(m, c, b) for m in range(4) for c in range(4) for b in (0, 1)]
    legal = [s for s in states if safe(s[0], s[1])]
    print(f"{len(states)} possible states, {len(legal)} safe")
    print("From the start, the legal moves are:")
    for a in p.actions(p.initial):
        print(f"  carry {a[0]}M {a[1]}C -> {p.result(p.initial, a)}")

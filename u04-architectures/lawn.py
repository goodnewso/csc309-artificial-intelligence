"""lawn.py: a lawn-trimming robot with a bump sensor, two ways.

Lawn: 12 x 20 cells with a flower bed the robot must not enter.  The
robot senses only whether the cell ahead is blocked.
  bounce   - simple reflex: drive straight; when blocked (and now and
             then at random, 1 step in 10), turn to a random heading.
  sweep    - model-based: mow in rows (back and forth), remembering
             which cells are cut and heading for the nearest uncut one.
"""
import random
from collections import deque

ROWS, COLS = 12, 20
BED = {(r, c) for r in range(4, 7) for c in range(8, 13)}   # obstacle
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def free(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS and (r, c) not in BED


def bounce(steps, rng):
    r, c, d = 0, 0, 0
    cut = {(r, c)}
    for _ in range(steps):
        dr, dc = DIRS[d]
        if free(r + dr, c + dc) and rng.random() > 0.1:
            r, c = r + dr, c + dc
            cut.add((r, c))
        else:                                # bump: pick a new heading
            d = rng.randrange(4)
    return cut


def sweep(steps):
    r, c = 0, 0
    cut, moved = {(r, c)}, 0
    while moved < steps:
        # breadth-first search from here to the nearest uncut cell
        frontier, came = deque([(r, c)]), {(r, c): None}
        target = None
        while frontier:
            cell = frontier.popleft()
            if cell not in cut:
                target = cell
                break
            # prefer moving along the row: gives back-and-forth rows
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nxt = (cell[0] + dr, cell[1] + dc)
                if free(*nxt) and nxt not in came:
                    came[nxt] = cell
                    frontier.append(nxt)
        if target is None:
            break                            # everything is cut
        path = []
        while target != (r, c):
            path.append(target)
            target = came[target]
        for cell in reversed(path):
            r, c = cell
            cut.add(cell)
            moved += 1
            if moved == steps:
                break
    return cut


if __name__ == "__main__":
    lawn = ROWS * COLS - len(BED)
    print(f"lawn: {lawn} cells to cut")
    print(f"{'steps':>6}{'bounce':>10}{'sweep':>10}")
    for steps in (100, 225, 400, 800):
        b = len(bounce(steps, random.Random(309)))
        s = len(sweep(steps))
        print(f"{steps:>6}{100 * b / lawn:>9.0f}%{100 * s / lawn:>9.0f}%")

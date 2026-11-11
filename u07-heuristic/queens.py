"""queens.py: local search for the 8-queens problem.

A state lists the row of the queen in each column.  The cost is the
number of pairs of queens that attack each other; a solution has cost 0.
"""
import math
import random

N = 8


def attacks(s):
    return sum(1 for i in range(N) for j in range(i + 1, N)
               if s[i] == s[j] or abs(s[i] - s[j]) == j - i)


def neighbours(s):                       # move one queen within its column
    for col in range(N):
        for row in range(N):
            if row != s[col]:
                yield s[:col] + (row,) + s[col + 1:]


def hill_climb(s):
    """Steepest descent: take the best neighbour until none is better."""
    steps = 0
    while True:
        best = min(neighbours(s), key=attacks)
        if attacks(best) >= attacks(s):
            return s, steps              # a local (maybe global) minimum
        s, steps = best, steps + 1


def random_state(rng):
    return tuple(rng.randrange(N) for _ in range(N))


def random_restart(rng):
    tries = 0
    while True:
        tries += 1
        s, _ = hill_climb(random_state(rng))
        if attacks(s) == 0:
            return s, tries


def anneal(rng, t0=2.0, cooling=0.995, steps=20000):
    s = random_state(rng)
    t = t0
    for _ in range(steps):
        if attacks(s) == 0:
            return s
        col, row = rng.randrange(N), rng.randrange(N)
        s2 = s[:col] + (row,) + s[col + 1:]
        delta = attacks(s2) - attacks(s)
        if delta <= 0 or rng.random() < math.exp(-delta / t):
            s = s2                       # accept; worse moves sometimes
        t = max(t * cooling, 0.01)
    return s


if __name__ == "__main__":
    rng = random.Random(309)
    runs = [hill_climb(random_state(rng)) for _ in range(1000)]
    ok = [r for r in runs if attacks(r[0]) == 0]
    print(f"hill climbing: {len(ok)} of 1000 runs solved "
          f"({len(ok) / 10:.1f}%), average {sum(r[1] for r in runs) / 1000:.1f}"
          " steps")
    tries = [random_restart(rng)[1] for _ in range(100)]
    print(f"random restart: always solves; average "
          f"{sum(tries) / 100:.1f} climbs per solution")
    sols = [anneal(rng) for _ in range(100)]
    print(f"simulated annealing: {sum(attacks(s) == 0 for s in sols)}"
          " of 100 runs solved")
    s, _ = random_restart(rng)
    print("a solution:", s)
    for r in range(N):
        print("  " + " ".join("Q" if s[c] == r else "." for c in range(N)))

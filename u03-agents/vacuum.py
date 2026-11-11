"""vacuum.py: three cleaning agents in the same environment.

A 4 x 4 classroom floor; each step a clean square becomes dirty with
probability 0.02.  The agent perceives only its own square (location,
dirty?) and acts: Suck, Up, Down, Left or Right.
Performance measure: +10 per square cleaned, -1 per move, over 500 steps.
"""
import random

SIZE, DIRT_RATE, STEPS = 4, 0.02, 500
MOVES = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}


class Floor:                                   # the ENVIRONMENT
    def __init__(self, rng):
        self.rng = rng
        self.dirty = {(r, c) for r in range(SIZE) for c in range(SIZE)
                      if rng.random() < 0.5}
        self.pos, self.score = (0, 0), 0

    def percept(self):
        return self.pos, self.pos in self.dirty

    def execute(self, action):
        if action == "Suck":
            if self.pos in self.dirty:
                self.dirty.remove(self.pos)
                self.score += 10
        else:
            dr, dc = MOVES[action]
            r, c = self.pos[0] + dr, self.pos[1] + dc
            if 0 <= r < SIZE and 0 <= c < SIZE:
                self.pos = (r, c)
            self.score -= 1
        for sq in ((r, c) for r in range(SIZE) for c in range(SIZE)):
            if self.rng.random() < DIRT_RATE:
                self.dirty.add(sq)


def random_agent(rng):
    return lambda percept: rng.choice(["Suck"] + list(MOVES))


def reflex_agent(rng):
    """Simple reflex: condition-action rules on the current percept."""
    def act(percept):
        _, dirty = percept
        return "Suck" if dirty else rng.choice(list(MOVES))
    return act


def model_agent():
    """Model-based: remembers when it last saw each square and heads for
    the square it has not visited for the longest time."""
    last_seen = {}
    clock = [0]

    def act(percept):
        (r, c), dirty = percept
        clock[0] += 1
        last_seen[(r, c)] = clock[0]
        if dirty:
            return "Suck"
        target = min(((rr, cc) for rr in range(SIZE) for cc in range(SIZE)),
                     key=lambda sq: (last_seen.get(sq, 0),
                                     abs(sq[0] - r) + abs(sq[1] - c)))
        if target[0] != r:
            return "Down" if target[0] > r else "Up"
        return "Right" if target[1] > c else "Left"
    return act


def run(make_agent, seed):
    rng = random.Random(seed)
    env = Floor(rng)
    agent = make_agent(random.Random(seed + 1))
    for _ in range(STEPS):
        env.execute(agent(env.percept()))
    return env.score, len(env.dirty)


if __name__ == "__main__":
    agents = [("random", random_agent), ("simple reflex", reflex_agent),
              ("model-based", lambda rng: model_agent())]
    print(f"{'agent':15}{'average score':>15}{'dirty at end':>14}")
    for name, make in agents:
        results = [run(make, seed) for seed in range(20)]
        score = sum(r[0] for r in results) / len(results)
        left = sum(r[1] for r in results) / len(results)
        print(f"{name:15}{score:>15.1f}{left:>14.1f}")

"""ants.py: a colony of simple reflex agents foraging for food.

No ant knows where the food is or talks to another ant.  An ant that
finds food carries it home and lays a pheromone trail; ants looking for
food prefer squares with more pheromone.  Pheromone evaporates.  The
colony finds and uses short routes although no single ant plans one.
"""
import random

W = H = 41
NEST = (20, 20)
FOOD = {(5 + dx, 6 + dy) for dx in range(3) for dy in range(3)} | \
       {(33 + dx, 30 + dy) for dx in range(3) for dy in range(3)}
STEPS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
           (1, 1)]


def simulate(pheromone=True, ants=60, steps=1500, seed=309):
    rng = random.Random(seed)
    trail = [[0.0] * W for _ in range(H)]
    food = {sq: 30 for sq in FOOD}          # units of food per square
    colony = [{"pos": NEST, "carrying": False} for _ in range(ants)]
    delivered, history = 0, []
    for t in range(steps):
        for ant in colony:
            x, y = ant["pos"]
            if ant["carrying"]:              # go home, laying pheromone
                if pheromone:
                    trail[y][x] += 1.0
                x += (NEST[0] > x) - (NEST[0] < x)
                y += (NEST[1] > y) - (NEST[1] < y)
                if (x, y) == NEST:
                    ant["carrying"] = False
                    delivered += 1
            else:                            # search, biased by pheromone
                opts = [(x + dx, y + dy) for dx, dy in STEPS_8
                        if 0 <= x + dx < W and 0 <= y + dy < H]
                weights = [1 + 20 * trail[b][a] for a, b in opts]
                x, y = rng.choices(opts, weights)[0]
                if food.get((x, y), 0) > 0:
                    food[(x, y)] -= 1
                    ant["carrying"] = True
            ant["pos"] = (x, y)
        for row in trail:                    # evaporation
            for i in range(W):
                row[i] *= 0.98
        if (t + 1) % 300 == 0:
            history.append(delivered)
    return history, trail, colony


if __name__ == "__main__":
    for flag in (False, True):
        hist, _, _ = simulate(pheromone=flag)
        label = "with pheromone   " if flag else "without pheromone"
        print(label, "food delivered after 300, 600, ... 1500 steps:",
              ", ".join(map(str, hist)))

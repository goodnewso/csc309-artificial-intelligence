"""boids.py: flocking from three local rules (after Reynolds, 1987).

Each bird sees only neighbours within RADIUS and steers by
  separation - move away from birds that are too close,
  alignment   - match the average heading of neighbours,
  cohesion    - move towards the neighbours' centre.
"Order" is the length of the average unit heading: near 0 when birds fly
in all directions, 1 when they all fly the same way.
"""
import math
import random

N, SIZE, RADIUS, CLOSE, SPEED = 60, 100.0, 15.0, 4.0, 1.0


def wrap(d):                                 # shortest offset on a torus
    return (d + SIZE / 2) % SIZE - SIZE / 2


def step(birds):
    new = []
    for i, (x, y, vx, vy) in enumerate(birds):
        sx = sy = ax = ay = cx = cy = 0.0
        n = 0
        for j, (x2, y2, vx2, vy2) in enumerate(birds):
            if i == j:
                continue
            dx, dy = wrap(x2 - x), wrap(y2 - y)
            d = math.hypot(dx, dy)
            if d < RADIUS:
                n += 1
                ax, ay, cx, cy = ax + vx2, ay + vy2, cx + dx, cy + dy
                if d < CLOSE:
                    sx, sy = sx - dx / d, sy - dy / d
        if n:
            vx += 0.05 * (ax / n - vx) + 0.01 * cx / n + 0.1 * sx
            vy += 0.05 * (ay / n - vy) + 0.01 * cy / n + 0.1 * sy
        norm = math.hypot(vx, vy) or 1
        vx, vy = SPEED * vx / norm, SPEED * vy / norm
        new.append(((x + vx) % SIZE, (y + vy) % SIZE, vx, vy))
    return new


def order(birds):
    return math.hypot(sum(b[2] for b in birds),
                      sum(b[3] for b in birds)) / (SPEED * len(birds))


def flock(seed=309, steps=300):
    rng = random.Random(seed)
    birds = []
    for _ in range(N):
        a = rng.uniform(0, 2 * math.pi)
        birds.append((rng.uniform(0, SIZE), rng.uniform(0, SIZE),
                      math.cos(a), math.sin(a)))
    snapshots = {0: birds}
    for t in range(1, steps + 1):
        birds = step(birds)
        if t in (50, 100, 200, 300):
            snapshots[t] = birds
    return snapshots


if __name__ == "__main__":
    for t, birds in flock().items():
        print(f"step {t:3}: order = {order(birds):.2f}")

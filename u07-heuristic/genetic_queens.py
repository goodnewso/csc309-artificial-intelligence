"""Unit 7: a genetic algorithm for the 8-queens problem.

A state lists the row of the queen in each column. Fitness is the number
of non-attacking pairs (28 is a solution). Each generation keeps the
best two, then breeds children from parents chosen by tournament, using
crossover and mutation.
"""
import random

N, POP, GENS = 8, 60, 500
MAX = N * (N - 1) // 2


def fitness(s):
    clash = sum(1 for i in range(N) for j in range(i + 1, N)
                if s[i] == s[j] or abs(s[i] - s[j]) == j - i)
    return MAX - clash


def child(a, b, rng):
    cut = rng.randrange(1, N)                    # one-point crossover
    c = a[:cut] + b[cut:]
    if rng.random() < 0.8:                       # mutation: move a queen
        c[rng.randrange(N)] = rng.randrange(N)
    return c


def pick(pop, rng):                              # tournament selection
    return max(rng.sample(pop, 3), key=fitness)


rng = random.Random(309)
pop = [[rng.randrange(N) for _ in range(N)] for _ in range(POP)]
for gen in range(GENS):
    pop.sort(key=fitness, reverse=True)
    best = pop[0]
    if gen % 20 == 0 or fitness(best) == MAX:
        print(f"generation {gen:3d}: best fitness {fitness(best)} of {MAX}")
    if fitness(best) == MAX:
        break
    pop = pop[:2] + [child(pick(pop, rng), pick(pop, rng), rng)
                     for _ in range(POP - 2)]            # keep the best 2
print("solution (row of each queen):", best)
for r in range(N):
    print("   " + " ".join("Q" if best[c] == r else "." for c in range(N)))

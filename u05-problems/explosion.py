"""explosion.py: how fast a search tree grows (combinatorial explosion).

A tree with branching factor b has b**d nodes at depth d.  Assume a
computer that generates one million nodes per second and stores each in
100 bytes.
"""
RATE, BYTES = 1_000_000, 100


def human(seconds):
    for unit, size in (("years", 3.156e7), ("days", 86400),
                       ("hours", 3600), ("minutes", 60)):
        if seconds >= size:
            return f"{seconds / size:,.1f} {unit}"
    return f"{seconds:.3g} seconds"


def memory(nodes):
    size = nodes * BYTES
    for unit, n in (("PB", 1e15), ("TB", 1e12), ("GB", 1e9), ("MB", 1e6),
                    ("KB", 1e3)):
        if size >= n:
            return f"{size / n:,.0f} {unit}"
    return f"{size:.0f} bytes"


print(f"{'depth':>5}{'nodes (b = 10)':>26}{'time':>18}"
      f"{'memory':>10}")
for d in (2, 4, 6, 8, 10, 12, 14, 16):
    n = sum(10 ** i for i in range(d + 1))     # whole tree to depth d
    print(f"{d:>5}{n:>26,}{human(n / RATE):>18}{memory(n):>10}")

print("\nGames (approximate branching factor b and length d of a game):")
for game, b, d in (("noughts and crosses", 4, 9), ("draughts", 8, 70),
                   ("chess", 35, 80), ("Go (19 x 19)", 250, 150)):
    print(f"  {game:22} b**d is about 10**{len(str(b ** d)) - 1}")

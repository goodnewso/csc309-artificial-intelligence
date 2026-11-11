"""roadmap.py: route finding on a simplified road map of Rivers State.

Positions are approximate (degrees); road lengths are approximate
kilometres chosen for teaching, not survey figures.
"""
import math
from search import Problem

POS = {                                  # (latitude, longitude)
    "Port Harcourt": (4.815, 7.050), "Choba": (4.893, 6.906),
    "Emohua": (4.877, 6.857), "Isiokpo": (4.998, 6.880),
    "Elele": (5.106, 6.813), "Ahoada": (5.078, 6.649),
    "Omoku": (5.343, 6.656), "Oyigbo": (4.879, 7.148),
    "Onne": (4.723, 7.152), "Bori": (4.672, 7.367),
}
ROADS = [                                # (town, town, km)
    ("Port Harcourt", "Choba", 21), ("Choba", "Emohua", 8),
    ("Choba", "Isiokpo", 16), ("Isiokpo", "Elele", 17),
    ("Emohua", "Ahoada", 42), ("Elele", "Ahoada", 24),
    ("Elele", "Omoku", 48), ("Ahoada", "Omoku", 33),
    ("Port Harcourt", "Oyigbo", 16), ("Port Harcourt", "Onne", 22),
    ("Onne", "Bori", 29), ("Oyigbo", "Bori", 42),
]
GRAPH = {t: {} for t in POS}
for a, b, km in ROADS:
    GRAPH[a][b] = GRAPH[b][a] = km


def straight_km(a, b):
    """Great-circle (straight-line) distance between two towns."""
    (la1, lo1), (la2, lo2) = POS[a], POS[b]
    la1, lo1, la2, lo2 = map(math.radians, (la1, lo1, la2, lo2))
    d = (math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2)
         * math.sin((lo2 - lo1) / 2) ** 2)
    return 2 * 6371 * math.asin(math.sqrt(d))


# a road can never be shorter than the straight line between its ends
assert all(km >= straight_km(a, b) for a, b, km in ROADS)


class Route(Problem):
    def __init__(self, start, goal):
        super().__init__(start)
        self.goal = goal

    def actions(self, s):
        return sorted(GRAPH[s])          # action = the town to drive to

    def result(self, s, a):
        return a

    def is_goal(self, s):
        return s == self.goal

    def cost(self, s, a, s2):
        return GRAPH[s][s2]

    def h(self, s):                      # straight-line distance to goal
        return straight_km(s, self.goal)


def show(name, goal, stats):
    towns = [s for _, s in goal.path()]
    print(f"{name:14} {goal.g:4} km, {stats['expanded']:2} expanded: "
          + " -> ".join(towns))


if __name__ == "__main__":
    from search import breadth_first, uniform_cost
    p = Route("Port Harcourt", "Omoku")
    show("breadth-first", *breadth_first(p))
    show("uniform-cost", *uniform_cost(p))

"""route_astar.py: uninformed versus heuristic search on the road map."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "u06-uninformed"))
from roadmap import Route, show, straight_km, POS          # noqa: E402
from search import uniform_cost, greedy, astar             # noqa: E402

print(f"{'town':14}{'h to Omoku':>11}{'h to Ahoada':>12}")
for town in sorted(POS, key=lambda t: straight_km(t, "Omoku")):
    print(f"{town:14}{straight_km(town, 'Omoku'):11.1f}"
          f"{straight_km(town, 'Ahoada'):12.1f}")

for goal in ("Omoku", "Ahoada"):
    p = Route("Port Harcourt", goal)
    print(f"\nPort Harcourt to {goal}:")
    show("uniform-cost", *uniform_cost(p))
    show("greedy", *greedy(p))
    show("A*", *astar(p))

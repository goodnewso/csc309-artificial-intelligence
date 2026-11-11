"""solve_mc.py: four uninformed searches on missionaries and cannibals."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "u05-problems"))
from missionaries import Missionaries                     # noqa: E402
from search import (breadth_first, depth_first,           # noqa: E402
                    iterative_deepening, uniform_cost)

p = Missionaries()
goal, _ = breadth_first(p)
print("Breadth-first solution:")
for step, (action, state) in enumerate(goal.path()):
    side = "left " if state[2] == 1 else "right"
    if action:
        print(f"  {step:2}. carry {action[0]}M {action[1]}C  -> "
              f"left bank {state[0]}M {state[1]}C, boat {side}")
    else:
        print(f"   0. start                -> "
              f"left bank {state[0]}M {state[1]}C, boat {side}")

print(f"\n{'algorithm':22}{'crossings':>10}{'expanded':>10}")
for name, algo in [("breadth-first", breadth_first),
                   ("depth-first", depth_first),
                   ("iterative deepening", iterative_deepening),
                   ("uniform-cost", uniform_cost)]:
    goal, stats = algo(p)
    print(f"{name:22}{goal.depth:>10}{stats['expanded']:>10}")

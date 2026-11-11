"""example_water_jug.py: formulating the water-jug problem.

A 4-litre jug and a 3-litre jug, a tap, no markings.  Goal: exactly
2 litres in the 4-litre jug.  State = (litres in 4L jug, litres in 3L jug).
"""
CAP = (4, 3)

def successors(state):
    a, b = state
    pour_ab = min(a, CAP[1] - b)          # amount that fits
    pour_ba = min(b, CAP[0] - a)
    return {
        "fill 4L": (CAP[0], b),  "fill 3L": (a, CAP[1]),
        "empty 4L": (0, b),      "empty 3L": (a, 0),
        "pour 4L->3L": (a - pour_ab, b + pour_ab),
        "pour 3L->4L": (a + pour_ba, b - pour_ba),
    }

def is_goal(state):
    return state[0] == 2

initial = (0, 0)
print("initial state:", initial)
for action, result in successors((4, 0)).items():
    print(f"from (4, 0): {action:<12} -> {result}")
print("is (2, 0) a goal?", is_goal((2, 0)))

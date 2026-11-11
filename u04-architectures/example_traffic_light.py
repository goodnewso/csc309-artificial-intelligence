"""example_traffic_light.py: a simple reflex controller versus a
model-based one at a junction.

When the light changes there is an amber phase, so only one car passes.
The reflex controller looks only at the queues now and switches often;
the model-based one remembers how long the current road has had green
(its internal state) and switches less.
"""
import random

def reflex(q):                          # green for the longer queue
    return "NS" if q["NS"] >= q["EW"] else "EW"

class ModelBased:
    def __init__(self):
        self.green, self.held = "NS", 0      # internal state
    def act(self, q):
        other = "EW" if self.green == "NS" else "NS"
        if self.held >= 4 and q[other] > 0 or q[self.green] == 0:
            self.green, self.held = other, 0
        self.held += 1
        return self.green

for name, ctl in [("reflex", reflex), ("model-based", ModelBased().act)]:
    random.seed(4)
    q, waited, switches, last = {"NS": 0, "EW": 0}, 0, 0, "NS"
    for step in range(60):
        q["NS"] += random.choice([1, 2]); q["EW"] += random.choice([1, 2])
        g = ctl(q)
        passed = 1 if g != last else 3      # amber when the light changes
        switches += g != last
        q[g], last = max(0, q[g] - passed), g
        waited += q["NS"] + q["EW"]
    print(f"{name:<12} switches: {switches:2}  total car-waits: {waited}")

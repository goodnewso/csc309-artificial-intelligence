"""example_ripeness.py: a hand-written rule versus a rule learnt from data.

Classify mangoes as ripe or unripe from a softness score (0-10).
"""
# 1. Rule-based: a person writes the rule.
def rule_based(softness):
    return "ripe" if softness >= 5 else "unripe"

# 2. Learning: find the threshold that makes the fewest mistakes on examples.
examples = [(2, "unripe"), (3, "unripe"), (4, "unripe"), (6, "unripe"),
            (7, "ripe"), (8, "ripe"), (9, "ripe"), (6.5, "ripe")]

def mistakes(t):
    return sum((s >= t) != (label == "ripe") for s, label in examples)

best = min([x / 2 for x in range(0, 21)], key=mistakes)
print("learnt threshold:", best, "with", mistakes(best), "mistakes")
print("hand-written rule makes", mistakes(5), "mistakes")
for s in (4.5, 6.2, 8):
    print(f"softness {s}: rule says {rule_based(s)},",
          "learnt says", "ripe" if s >= best else "unripe")

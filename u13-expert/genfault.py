"""genfault.py: a small rule-based expert system that advises on why a
petrol generator will not start or runs badly.

Knowledge base : IF-THEN rules with certainty factors (CF, -1 .. 1).
Working memory : facts with their CFs.
Inference      : backward chaining from each possible fault (asking the
                 user only for facts it needs); forward chaining from
                 known facts is shown for comparison.
Explanation    : WHY a question is asked; HOW a conclusion was reached.
The rules are illustrative teaching material, not a repair manual.
"""
RULES = [
    # (name, conditions (all must hold), conclusion, CF of the rule)
    ("R1", ["engine does not crank"], "battery or starter fault", 0.6),
    ("R2", ["engine cranks", "no fuel in tank"], "out of fuel", 0.95),
    ("R3", ["engine cranks", "fuel present", "fuel is old"],
     "stale fuel", 0.7),
    ("R4", ["engine cranks", "fuel present", "no spark at plug"],
     "spark plug fault", 0.8),
    ("R5", ["engine runs", "black smoke"], "choke or air filter blocked",
     0.75),
    ("R6", ["engine runs", "stops under load"], "generator overloaded", 0.8),
    ("R7", ["spark plug fault", "plug is wet"], "engine flooded", 0.6),
]
FAULTS = ["battery or starter fault", "out of fuel", "stale fuel",
          "spark plug fault", "engine flooded",
          "choke or air filter blocked", "generator overloaded"]
OPPOSITE = {"engine cranks": "engine does not crank",
            "fuel present": "no fuel in tank"}


class Engine:
    def __init__(self, answers):
        self.answers = answers           # simulated user: fact -> CF
        self.memory = {}                 # working memory: fact -> CF
        self.how = {}                    # fact -> rule that concluded it
        self.asked = []

    def ask(self, fact, why_rule):
        if fact not in self.memory:
            cf = self.answers.get(fact, 0.0)
            if fact not in self.answers and fact in OPPOSITE.values():
                pos = [k for k, v in OPPOSITE.items() if v == fact][0]
                cf = -self.answers.get(pos, 0.0)
            self.memory[fact] = cf
            self.asked.append((fact, why_rule, cf))
        return self.memory[fact]

    def prove(self, goal, why_rule=None):
        """Backward chaining: CF of goal from the rules that conclude it,
        or from the user if no rule does."""
        if goal in self.memory:
            return self.memory[goal]
        rules = [r for r in RULES if r[2] == goal]
        if not rules:
            return self.ask(goal, why_rule)
        best = 0.0
        for name, conds, _, rule_cf in rules:
            cf = 1.0
            for c in conds:
                cf = min(cf, self.prove(c, name))     # AND: minimum
                if cf <= 0.2:                         # give up early
                    break
            if cf > 0.2:
                new = cf * rule_cf
                # combine evidence from several rules: a + b(1 - a)
                best = best + new * (1 - best)
                self.how[goal] = (name, conds, round(cf, 2), rule_cf)
        self.memory[goal] = best
        return best

    def forward(self, facts):
        """Forward chaining (data-driven), ignoring CFs: fire every rule
        whose conditions are all known, until nothing new appears."""
        known, fired = set(facts), []
        changed = True
        while changed:
            changed = False
            for name, conds, concl, _ in RULES:
                if concl not in known and all(c in known for c in conds):
                    known.add(concl)
                    fired.append(f"{name} -> {concl}")
                    changed = True
        return fired

    def diagnose(self):
        return sorted(((f, round(self.prove(f), 2)) for f in FAULTS
                       if self.prove(f) > 0), key=lambda x: -x[1])


if __name__ == "__main__":
    user = {"engine cranks": 1.0, "fuel present": 1.0, "fuel is old": 0.4,
            "no spark at plug": 0.9, "plug is wet": 0.8,
            "engine runs": -1.0}
    es = Engine(user)
    results = es.diagnose()
    print("Questions asked (fact, asked for rule, user's certainty):")
    for fact, rule, cf in es.asked:
        print(f"  {fact:24} WHY? needed by {rule:3}  answer CF {cf:+.1f}")
    print("\nConclusions:")
    for fault, cf in results:
        print(f"  {fault:22} CF {cf:.2f}")
    print("\nHOW was 'engine flooded' concluded?")
    fact = "engine flooded"
    while fact in es.how:
        rule, conds, cf, rcf = es.how[fact]
        print(f"  {fact} <- {rule} (rule CF {rcf}), because")
        print(f"    IF {' AND '.join(conds)}  (CF {cf})")
        fact = next((c for c in conds if c in es.how), None)
    print("\nForward chaining from the facts:")
    facts = ["engine cranks", "fuel present", "no spark at plug",
             "plug is wet"]
    print("  facts:", ", ".join(facts))
    for step in es.forward(facts):
        print("  fired", step)

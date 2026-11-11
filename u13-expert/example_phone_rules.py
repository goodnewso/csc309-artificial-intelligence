"""example_phone_rules.py: forward chaining over IF-THEN rules, with a
HOW explanation.  Domain: a phone that will not charge."""
RULES = [
    ("R1", {"no charging", "other charger works"}, "charger faulty"),
    ("R2", {"no charging", "no charger works"}, "suspect port or battery"),
    ("R3", {"suspect port or battery", "port has dirt"}, "clean the port"),
    ("R4", {"suspect port or battery", "port is clean"}, "replace battery"),
]

def forward_chain(facts):
    facts, how = set(facts), {}
    changed = True
    while changed:
        changed = False
        for name, conds, concl in RULES:
            if conds <= facts and concl not in facts:
                facts.add(concl)
                how[concl] = (name, conds)
                changed = True
    return facts, how

facts, how = forward_chain({"no charging", "no charger works",
                            "port is clean"})
print("advice:", "replace battery" if "replace battery" in facts
      else "none")
for concl, (rule, conds) in how.items():
    print(f"HOW {concl}? by {rule} because {' and '.join(sorted(conds))}")

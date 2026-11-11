"""Unit 13: a tiny backward-chaining expert system that explains itself.

Rules are IF conditions THEN conclusion. To test a goal, the system works
back through the rules and asks the user only about facts it needs. It
answers "why?" (why it is asking) and "how?" (how it concluded).
The answers are scripted here so the program runs on its own; set
INTERACTIVE = True to type yes/no answers yourself. For teaching only:
this is not medical advice.
"""
INTERACTIVE = False
RULES = [
    ("see a doctor today", ["malaria likely", "danger sign"]),
    ("see a doctor today", ["malaria likely", "no test available"]),
    ("malaria likely", ["fever", "chills", "lives in malaria area"]),
    ("danger sign", ["confusion"]),
    ("danger sign", ["vomits everything"]),
]
SCRIPT = {"fever": "yes", "chills": "yes", "lives in malaria area": "yes",
          "confusion": "no", "vomits everything": "no",
          "no test available": "yes"}
known, how = {}, {}


def ask(fact, why):
    if INTERACTIVE:
        ans = input(f"Is it true that: {fact}? (yes/no/why) ")
        while ans == "why":
            print("   because I am trying to establish:", why)
            ans = input(f"Is it true that: {fact}? (yes/no) ")
    else:
        ans = SCRIPT[fact]
        print(f"  Q: {fact}? -> {ans}   (asked to establish: {why})")
    return ans == "yes"


def prove(goal, why="the final advice"):
    if goal in known:
        return known[goal]
    rules = [r for r in RULES if r[0] == goal]
    if not rules:                                # a fact: ask the user
        known[goal] = ask(goal, why)
        return known[goal]
    for concl, conds in rules:
        if all(prove(c, goal) for c in conds):
            known[goal], how[goal] = True, conds
            return True
    known[goal] = False
    return False


result = prove("see a doctor today")
print("ADVICE:", "see a doctor today" if result else "no urgent visit")
if result:
    print("HOW:", "see a doctor today because",
          " and ".join(how["see a doctor today"]))
    print("    malaria likely because", " and ".join(how["malaria likely"]))

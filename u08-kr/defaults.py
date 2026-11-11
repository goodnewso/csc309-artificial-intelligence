"""defaults.py: non-monotonic reasoning with default rules.

A default rule says: if PRE holds, conclude C, UNLESS an exception is
known.  "Known" uses the closed-world assumption: what cannot be derived
is taken to be false (negation as failure).  Adding a fact can therefore
REMOVE a conclusion, which never happens in classical logic.
"""

# facts are (predicate, subject) pairs
STRICT = [                                  # if A(x) then B(x), always
    ("ostrich", "bird"), ("bird", "animal"), ("penguin", "bird"),
]
DEFAULTS = [                                # (pre, conclusion, exceptions)
    ("bird", "flies", ["ostrich", "penguin", "injured"]),
    ("animal", "walks", ["injured"]),
]


def closure(facts):
    """Apply strict rules, then defaults whose exceptions are not known."""
    known = set(facts)
    changed = True
    while changed:
        changed = False
        for pre, post in STRICT:
            for p, x in list(known):
                if p == pre and (post, x) not in known:
                    known.add((post, x))
                    changed = True
    for pre, post, exceptions in DEFAULTS:
        for p, x in list(known):
            if p == pre and not any((e, x) in known for e in exceptions):
                known.add((post, x))        # assumed, not proved
    return known


def show(label, facts, who):
    known = closure(facts)
    props = sorted(p for p, x in known if x == who)
    print(f"{label:38} {who}: {', '.join(props)}")


if __name__ == "__main__":
    facts = {("bird", "Kiki")}
    show("Kiki is a bird.", facts, "Kiki")
    facts.add(("injured", "Kiki"))
    show("...and we learn Kiki is injured.", facts, "Kiki")
    facts = {("ostrich", "Ozzy")}
    show("Ozzy is an ostrich.", facts, "Ozzy")

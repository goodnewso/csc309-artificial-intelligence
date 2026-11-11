"""to_logic.py: translating English sentences into predicate logic.

Each grammar rule has a semantic rule (compositional semantics): the
meaning of a phrase is built from the meanings of its parts.  Noun
phrases become functions that take a property and build a formula, which
is how "every" yields a universal quantifier and "some" an existential.
"""
import itertools
from cfgparse import parses

fresh = itertools.count(1)


def cap(w):
    return w[0].upper() + w[1:]


def meaning(tree):
    kind = tree[0]
    if kind == "S":                           # S -> NP VP
        return meaning(tree[1])(meaning(tree[2]))
    if kind == "NP":
        if tree[1][0] == "PropN":             # a name: apply P to it
            name = tree[1][1]
            return lambda P: P(name)
        det, noun = tree[1][1], cap(tree[2][1])
        def quantified(P):
            v = f"x{next(fresh)}"
            if det == "every":
                return f"∀{v} ({noun}({v}) → {P(v)})"
            return f"∃{v} ({noun}({v}) ∧ {P(v)})"   # some / a / the
        return quantified
    if kind == "VP":
        verb = cap(tree[1][1])
        if len(tree) == 2:                    # VP -> V
            return lambda x: f"{verb}({x})"
        obj = meaning(tree[2])                # VP -> V NP
        return lambda x: obj(lambda y: f"{verb}({x}, {y})")
    raise ValueError(kind)


if __name__ == "__main__":
    for s in ["Amaka passes the course.",
              "Every student reads a note.",
              "Some lecturer teaches every student.",
              "Every student likes Ada."]:
        print(s)
        print("   ", meaning(parses(s)[0]))

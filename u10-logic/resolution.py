"""resolution.py: answering queries by resolution refutation.

Clauses are written as strings such as
    "~Student(x) | ~Attends(x) | Passes(x)"
Variables are lower-case (x, y, z); constants and functions start with a
capital letter or are function terms such as Sup(x).  Answers are found
with an Answer(...) literal added to the negated query.
"""
import itertools
import re

counter = itertools.count(1)


# ---------- parsing --------------------------------------------------------
def parse_term(t):
    t = t.strip()
    m = re.fullmatch(r"(\w+)\((.*)\)", t)
    if m:
        return (m.group(1),) + tuple(parse_term(a) for a in split(m.group(2)))
    return t


def split(s):                                  # split on top-level commas
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
            continue
        depth += (ch == "(") - (ch == ")")
        cur += ch
    return out + [cur]


def parse_clause(text):
    lits = []
    for part in text.split("|"):
        part = part.strip()
        neg = part.startswith("~")
        m = re.fullmatch(r"(\w+)\((.*)\)", part.lstrip("~"))
        lits.append((neg, m.group(1), tuple(parse_term(a)
                                            for a in split(m.group(2)))))
    return tuple(lits)


def is_var(t):
    return isinstance(t, str) and t[0].islower()


def show_term(t):
    if isinstance(t, tuple):
        return f"{t[0]}({', '.join(show_term(a) for a in t[1:])})"
    return t


def show(clause):
    if not clause:
        return "[] (the empty clause)"
    return " | ".join(("~" if n else "") + p + "("
                      + ", ".join(show_term(a) for a in args) + ")"
                      for n, p, args in clause)


# ---------- unification -------------------------------------------------
def substitute(t, s):
    if is_var(t):
        return substitute(s[t], s) if t in s else t
    if isinstance(t, tuple):
        return (t[0],) + tuple(substitute(a, s) for a in t[1:])
    return t


def occurs(v, t, s):
    t = substitute(t, s)
    return t == v or (isinstance(t, tuple)
                      and any(occurs(v, a, s) for a in t[1:]))


def unify(a, b, s):
    """Return a substitution that makes a and b identical, or None."""
    if s is None:
        return None
    a, b = substitute(a, s), substitute(b, s)
    if a == b:
        return s
    if is_var(a):
        return None if occurs(a, b, s) else {**s, a: b}
    if is_var(b):
        return unify(b, a, s)
    if isinstance(a, tuple) and isinstance(b, tuple) and \
            a[0] == b[0] and len(a) == len(b):
        for x, y in zip(a[1:], b[1:]):
            s = unify(x, y, s)
        return s
    return None


def rename(clause):
    """Standardise apart: give the clause's variables fresh names."""
    n = next(counter)
    def r(t):
        if is_var(t):
            return f"{t}{n}"
        if isinstance(t, tuple):
            return (t[0],) + tuple(r(a) for a in t[1:])
        return t
    return tuple((neg, p, tuple(r(a) for a in args))
                 for neg, p, args in clause)


def resolvents(c1, c2):
    c2 = rename(c2)
    for i, (n1, p1, a1) in enumerate(c1):
        for j, (n2, p2, a2) in enumerate(c2):
            if p1 == p2 and n1 != n2 and len(a1) == len(a2):
                s = {}
                for x, y in zip(a1, a2):
                    s = unify(x, y, s)
                if s is not None:
                    rest = [lit for k, lit in enumerate(c1) if k != i] + \
                           [lit for k, lit in enumerate(c2) if k != j]
                    new = []
                    for neg, p, args in rest:
                        lit = (neg, p, tuple(substitute(a, s) for a in args))
                        if lit not in new:
                            new.append(lit)
                    yield tuple(new), s


# ---------- the prover ---------------------------------------------------
def prove(kb_texts, goal_texts, max_steps=2000):
    """Set-of-support resolution: every step uses a clause derived from the
    negated goal.  Stops at the empty clause or an Answer-only clause."""
    kb = [parse_clause(t) for t in kb_texts]
    support = [parse_clause(t) for t in goal_texts]
    parent = {c: None for c in support}
    seen = set(kb) | set(support)
    queue = list(support)
    while queue and max_steps:
        c1 = queue.pop(0)
        for c2 in kb + list(parent):
            for new, s in resolvents(c1, c2):
                max_steps -= 1
                if new in seen:
                    continue
                seen.add(new)
                parent[new] = (c1, c2)
                if all(p == "Answer" for _, p, _ in new):
                    return new, parent
                queue.append(new)
    return None, parent


def explain(clause, parent):
    """Print the derivation of a clause, earliest steps first."""
    steps = []
    def walk(c):
        if parent.get(c) and c not in steps:
            a, b = parent[c]
            walk(a)
            walk(b)
            steps.append(c)
    walk(clause)
    for i, c in enumerate(steps, 1):
        a, b = parent[c]
        print(f"{i}. {show(a)}\n     + {show(b)}\n    => {show(c)}")

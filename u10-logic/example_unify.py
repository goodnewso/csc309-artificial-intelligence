"""example_unify.py: unification, the pattern matching behind resolution.

Variables are strings starting with an upper-case letter; compound terms
are tuples (predicate first, in lower case) such as ("owns", "X", "tecno").
"""
def is_var(t):
    return isinstance(t, str) and t[0].isupper()

def unify(a, b, s):
    if s is None:
        return None
    a, b = s.get(a, a) if is_var(a) else a, s.get(b, b) if is_var(b) else b
    if a == b:
        return s
    if is_var(a):
        return {**s, a: b}
    if is_var(b):
        return {**s, b: a}
    if isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b):
        for x, y in zip(a, b):
            s = unify(x, y, s)
        return s
    return None

print(unify(("phone", "X"), ("phone", "tecno"), {}))
print(unify(("owns", "X", "Y"), ("owns", "ada", "tecno"), {}))
print(unify(("phone", "X"), ("laptop", "hp"), {}))

"""semnet.py: a semantic network with inheritance and exceptions.

Nodes are concepts or individuals; labelled arcs are relations:
  instance-of (individual -> class), is-a (class -> class),
  has-part, and attribute arcs such as colour or habitat.
A property is looked up on the node itself first, then inherited along
instance-of / is-a arcs, so the NEAREST value wins (exceptions).
"""
ARCS = [
    ("Vehicle", "is-a", "Thing"),
    ("Car", "is-a", "Vehicle"), ("Keke", "is-a", "Vehicle"),
    ("Boat", "is-a", "Vehicle"),
    ("Vehicle", "has-part", "engine"),
    ("Vehicle", "moves-on", "land"),        # default for vehicles
    ("Boat", "moves-on", "water"),          # exception overrides it
    ("Car", "wheels", 4), ("Keke", "wheels", 3),
    ("Keke", "used-for", "short trips"),
    ("Car", "has-part", "steering wheel"),
    ("Okada", "is-a", "Vehicle"), ("Okada", "wheels", 2),
    ("Ada's car", "instance-of", "Car"),
    ("Ada's car", "colour", "blue"),
    ("Bonny ferry", "instance-of", "Boat"),
]


def parents(node):
    return [b for a, r, b in ARCS if a == node and r in ("is-a",
                                                       "instance-of")]


def lookup(node, relation):
    """Breadth-first up the hierarchy; return the first value found and
    the node it came from."""
    queue, seen = [node], set()
    while queue:
        n = queue.pop(0)
        values = [b for a, r, b in ARCS if a == n and r == relation]
        if values:
            return values, n
        seen.add(n)
        queue += [p for p in parents(n) if p not in seen]
    return None, None


def isa(node, cls):                          # follow the hierarchy up
    return node == cls or any(isa(p, cls) for p in parents(node))


def all_parts(node):                         # parts accumulate (no override)
    parts, queue = [], [node]
    while queue:
        n = queue.pop(0)
        parts += [b for a, r, b in ARCS if a == n and r == "has-part"]
        queue += parents(n)
    return parts


if __name__ == "__main__":
    for node, rel in [("Ada's car", "colour"), ("Ada's car", "wheels"),
                      ("Ada's car", "moves-on"), ("Bonny ferry", "moves-on"),
                      ("Keke", "used-for"), ("Okada", "colour")]:
        values, source = lookup(node, rel)
        where = f" (from {source})" if source else ""
        print(f"{node} {rel}: {values}{where}")
    print("Ada's car has parts:", all_parts("Ada's car"))
    print("Is Ada's car a Vehicle?", isa("Ada's car", "Vehicle"))
    print("Is the Bonny ferry a Car?", isa("Bonny ferry", "Car"))

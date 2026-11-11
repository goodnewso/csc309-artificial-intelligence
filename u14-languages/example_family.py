"""example_family.py: the Prolog family example written in Python."""
PARENT = [("ada", "bayo"), ("bayo", "chika"), ("bayo", "dayo")]

def grandparent(x):
    return [z for (a, y) in PARENT if a == x
              for (b, z) in PARENT if b == y]

print("grandchildren of ada:", grandparent("ada"))

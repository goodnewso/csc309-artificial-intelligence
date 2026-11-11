"""example_inheritance.py: inheritance with exceptions in a tiny network."""
ISA = {"okra": "vegetable", "cucumber": "vegetable", "vegetable": "food",
       "food": None}
PROPS = {"food": {"has": "calories"},
         "vegetable": {"eaten": "cooked", "colour": "green"},
         "cucumber": {"eaten": "raw"}}            # an exception

def lookup(node, slot):
    """Climb the is-a links until some node stores the slot."""
    while node is not None:
        if slot in PROPS.get(node, {}):
            return PROPS[node][slot], node
        node = ISA[node]
    return None, None

for item in ("okra", "cucumber"):
    for slot in ("eaten", "colour", "has"):
        value, where = lookup(item, slot)
        print(f"{item:<9} {slot:<7} = {value:<9} (from {where})")

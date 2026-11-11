"""frames.py: frames with slots, facets, defaults and demons.

A frame is a named collection of slots.  Each slot has facets:
  value      - a value given for this frame,
  default    - a value assumed if none is given,
  if_needed  - a procedure that computes the value when it is asked for,
  if_added   - a procedure that runs when a value is put in the slot.
Frames inherit from their 'is_a' (class) or 'instance_of' frame.
"""
FRAMES = {}


class Frame:
    def __init__(self, name, parent=None, **slots):
        self.name, self.parent, self.slots = name, parent, {}
        for slot, value in slots.items():
            self.slots[slot] = {"value": value}
        FRAMES[name] = self

    def facet(self, slot, facet, value):
        self.slots.setdefault(slot, {})[facet] = value
        return self

    def get(self, slot):
        frame = self
        while frame:                         # look up the chain
            facets = frame.slots.get(slot, {})
            if "value" in facets:
                return facets["value"]
            if "if_needed" in facets:
                return facets["if_needed"](self)   # demon computes it
            if "default" in facets:
                return facets["default"]
            frame = FRAMES.get(frame.parent)
        return None

    def put(self, slot, value):
        self.slots.setdefault(slot, {})["value"] = value
        frame = self
        while frame:                         # find an if_added demon
            demon = frame.slots.get(slot, {}).get("if_added")
            if demon:
                demon(self, value)
                break
            frame = FRAMES.get(frame.parent)


def grade_point(student):
    total = sum(u for u, _ in student.get("results"))
    points = sum(u * (5 if s >= 70 else 4 if s >= 60 else 3 if s >= 50
                      else 2 if s >= 45 else 1 if s >= 40 else 0)
                 for u, s in student.get("results"))
    return round(points / total, 2)


def warn_if_low(student, value):
    if value < 1.5:
        print(f"  [if_added] warning: {student.name}'s GPA is low")


# the class frame Student, and two instance frames
Frame("Student", None, university="RiSU") \
    .facet("level", "default", 100) \
    .facet("status", "default", "full-time") \
    .facet("gpa", "if_needed", grade_point) \
    .facet("gpa_record", "if_added", warn_if_low)
Frame("Ibiere", "Student", level=200, results=[(3, 78), (3, 64), (2, 55)])
Frame("Tamuno", "Student", results=[(3, 41), (2, 38), (3, 45)],
      status="part-time")

if __name__ == "__main__":
    for name in ("Ibiere", "Tamuno"):
        f = FRAMES[name]
        print(f"{name}: university={f.get('university')}, "
              f"level={f.get('level')}, status={f.get('status')}, "
              f"gpa={f.get('gpa')}")
        f.put("gpa_record", f.get("gpa"))

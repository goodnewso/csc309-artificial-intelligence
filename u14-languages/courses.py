"""courses.py: the same prerequisite knowledge in Python."""
PREREQ = {"csc309": ["csc203", "cos201"], "cos201": ["cos102"],
          "cos102": ["cos101"], "csc203": ["mth101"]}
PASSED = {"amaka": {"cos101", "cos102", "mth101"}}


def needs(course):
    out = []
    for before in PREREQ.get(course, []):
        out += [before] + needs(before)
    return out


def can_take(student, course):
    return all(p in PASSED[student] for p in PREREQ.get(course, []))


courses = set(PREREQ) | {c for v in PREREQ.values() for c in v}
print("Before csc309 you need:", needs("csc309"))
print("Amaka can take next:", sorted(c for c in courses
      if can_take("amaka", c) and c not in PASSED["amaka"]))
print("Can Amaka take csc309 now?", can_take("amaka", "csc309"))

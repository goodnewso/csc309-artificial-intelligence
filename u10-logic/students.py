"""students.py: the worked example of Unit 10, answered by resolution.

English                                      clause form
1 Every student who attends lectures passes  ~Student(x) | ~Attends(x)
  CSC 309.                                     | Passes(x)
2 Anyone who passes CSC 309 is happy.        ~Passes(x) | Happy(x)
3 Every student attends lectures or reads    ~Student(x) | Attends(x)
  the lecture note.                            | Reads(x)
4 Anyone who reads the lecture note passes.  ~Reads(x) | Passes(x)
5 Every student has a supervisor.            ~Student(x)
                                               | Supervises(Sup(x), x)
6 Amaka is a student.                        Student(Amaka)
"""
from resolution import prove, explain, show

KB = ["~Student(x) | ~Attends(x) | Passes(x)",
      "~Passes(x) | Happy(x)",
      "~Student(x) | Attends(x) | Reads(x)",
      "~Reads(x) | Passes(x)",
      "~Student(x) | Supervises(Sup(x), x)",
      "Student(Amaka)"]

print("Query 1: Is Amaka happy?  Negated goal: ~Happy(Amaka)")
result, parent = prove(KB, ["~Happy(Amaka) | Answer(Yes)"])
explain(result, parent)
print("Answer:", show(result))

print("\nQuery 2: Who supervises Amaka?  "
      "Negated goal: ~Supervises(y, Amaka)")
result, parent = prove(KB, ["~Supervises(y, Amaka) | Answer(y)"])
explain(result, parent)
print("Answer:", show(result))

print("\nQuery 3: Is Chidi happy?  (nothing is known about Chidi)")
result, _ = prove(KB, ["~Happy(Chidi) | Answer(Yes)"])
print("Answer:", "no proof found" if result is None else show(result))

"""Unit 2: scoring the class Turing test practical.

Each judge chats with two hidden partners, one a person and one a
program (or a student imitating one), and says which is the machine.
Record the results in the list below; the program reports how often
the machine was spotted. The data here are an EXAMPLE for practice.
"""
from collections import Counter

# (judge, hidden machine was partner A or B, judge's guess)
results = [
    ("Ada", "A", "A"), ("Bayo", "B", "B"), ("Chidi", "A", "B"),
    ("Dami", "B", "B"), ("Ebi", "A", "A"), ("Femi", "B", "A"),
    ("Gift", "A", "A"), ("Hauwa", "B", "B"), ("Ifeoma", "A", "B"),
    ("Jide", "B", "B"),
]
correct = sum(truth == guess for _, truth, guess in results)
n = len(results)
print(f"judges who spotted the machine: {correct} of {n} "
      f"({correct / n:.0%})")
print("guessing at random would be right about 50% of the time")
fooled = [j for j, t, g in results if t != g]
print("judges fooled:", ", ".join(fooled))
print("guesses per partner:", dict(Counter(g for _, _, g in results)))
if correct / n < 0.6:
    print("verdict: the machine did well; discuss what fooled the judges")
else:
    print("verdict: the machine was easy to spot; discuss the clues")

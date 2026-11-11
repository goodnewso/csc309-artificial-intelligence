"""Unit 1: a short tour of the Python tools used for AI in this course.

NumPy (arrays), scikit-learn (machine learning) and the standard library
(text and search). Run it to check that your computer is set up.
"""
import sys
from collections import deque
import numpy as np
import sklearn
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

print("Python", sys.version.split()[0], "| NumPy", np.__version__,
      "| scikit-learn", sklearn.__version__)

# NumPy: arithmetic on whole arrays at once
scores = np.array([45, 62, 71, 38, 90])
print("scores:", scores, "mean:", scores.mean(), "passed:", scores >= 40)

# scikit-learn: learn to recognise three kinds of iris flower
X, y = load_iris(return_X_y=True)
model = DecisionTreeClassifier(max_depth=2, random_state=309).fit(X, y)
print("decision tree accuracy on the iris flowers:",
      round(model.score(X, y), 3))

# the standard library: a breadth-first search over a tiny road map
roads = {"Port Harcourt": ["Choba", "Eleme"], "Choba": ["Emohua"],
         "Eleme": ["Onne"], "Emohua": [], "Onne": []}
frontier, seen = deque(["Port Harcourt"]), {"Port Harcourt"}
order = []
while frontier:
    town = frontier.popleft()
    order.append(town)
    for nxt in roads[town]:
        if nxt not in seen:
            seen.add(nxt)
            frontier.append(nxt)
print("breadth-first order:", " -> ".join(order))

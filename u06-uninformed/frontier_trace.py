"""Unit 6: watch the frontier of breadth-first and depth-first search.

A small tree of towns; the program prints the frontier before each
expansion, so you can check your hand traces against it.
"""
from collections import deque

tree = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F", "G"],
        "D": [], "E": ["H"], "F": [], "G": [], "H": []}
GOAL = "G"


def trace(name, pop):
    frontier = deque(["A"])
    print(name)
    step = 0
    while frontier:
        step += 1
        print(f"  {step}. frontier {list(frontier)}", end="")
        node = pop(frontier)
        print(f" -> expand {node}")
        if node == GOAL:
            print(f"  goal {GOAL} reached after {step} expansions")
            return
        children = tree[node]
        if pop is deque.pop:                     # LIFO: push in reverse so
            children = reversed(children)        # the left child is next
        frontier.extend(children)


trace("breadth-first (FIFO queue)", deque.popleft)
trace("depth-first (LIFO stack)", deque.pop)

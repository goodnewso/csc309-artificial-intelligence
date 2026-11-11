"""example_bfs_dfs.py: the order in which BFS and DFS expand a small tree."""
from collections import deque

TREE = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F", "G"],
        "D": [], "E": [], "F": [], "G": []}

def bfs(start):
    frontier, order = deque([start]), []        # FIFO queue
    while frontier:
        node = frontier.popleft()
        order.append(node)
        frontier.extend(TREE[node])
    return order

def dfs(start):
    frontier, order = [start], []               # LIFO stack
    while frontier:
        node = frontier.pop()
        order.append(node)
        frontier.extend(reversed(TREE[node]))   # left child on top
    return order

print("BFS:", " ".join(bfs("A")))
print("DFS:", " ".join(dfs("A")))

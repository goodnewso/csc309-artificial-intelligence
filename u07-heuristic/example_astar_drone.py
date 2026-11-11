"""example_astar_drone.py: A* for a delivery drone over a small network.

Edges carry flying distances (km); H gives the straight-line distance
from each point to the customer at G.
"""
import heapq

EDGES = {"S": {"A": 4, "B": 3}, "A": {"C": 5, "G": 12},
         "B": {"C": 7, "D": 7}, "C": {"G": 6}, "D": {"G": 6}, "G": {}}
H = {"S": 12, "A": 9, "B": 10, "C": 5, "D": 4, "G": 0}

def astar(start, goal):
    frontier = [(H[start], 0, start, [start])]     # (f, g, node, path)
    best_g, expanded = {start: 0}, []
    while frontier:
        f, g, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, g, expanded
        if g > best_g[node]:
            continue                               # a worse, older copy
        expanded.append(f"{node}(f={f})")
        for nxt, cost in EDGES[node].items():
            g2 = g + cost
            if g2 < best_g.get(nxt, float("inf")):
                best_g[nxt] = g2
                heapq.heappush(frontier,
                               (g2 + H[nxt], g2, nxt, path + [nxt]))

path, cost, expanded = astar("S", "G")
print("expanded:", ", ".join(expanded))
print("route:", " -> ".join(path), f"({cost} km)")

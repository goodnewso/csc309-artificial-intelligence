"""search.py: problem-solving agents' search algorithms (Units 6 and 7).

A problem supplies: initial, actions(s), result(s, a), is_goal(s) and,
optionally, cost(s, a, s2) and h(s).  Every search function returns
(goal_node or None, stats) where stats counts the work done.
"""
import heapq
from collections import deque
from itertools import count


class Problem:
    def __init__(self, initial):
        self.initial = initial

    def actions(self, s):
        raise NotImplementedError

    def result(self, s, a):
        raise NotImplementedError

    def is_goal(self, s):
        raise NotImplementedError

    def cost(self, s, a, s2):
        return 1

    def h(self, s):                     # heuristic: 0 unless overridden
        return 0


class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state, self.parent, self.action, self.g = state, parent, action, g
        self.depth = 0 if parent is None else parent.depth + 1

    def path(self):                     # list of (action, state) from start
        node, out = self, []
        while node:
            out.append((node.action, node.state))
            node = node.parent
        return out[::-1]


def expand(problem, node):
    for a in problem.actions(node.state):
        s2 = problem.result(node.state, a)
        yield Node(s2, node, a, node.g + problem.cost(node.state, a, s2))


def breadth_first(problem):
    """FIFO frontier; goal test when a node is generated."""
    stats = {"expanded": 0, "max_frontier": 1}
    start = Node(problem.initial)
    if problem.is_goal(start.state):
        return start, stats
    frontier, reached = deque([start]), {problem.initial}
    while frontier:
        node = frontier.popleft()
        stats["expanded"] += 1
        for child in expand(problem, node):
            if child.state not in reached:
                if problem.is_goal(child.state):
                    return child, stats
                reached.add(child.state)
                frontier.append(child)
        stats["max_frontier"] = max(stats["max_frontier"], len(frontier))
    return None, stats


def depth_first(problem):
    """LIFO frontier (graph search: never revisit a state)."""
    stats = {"expanded": 0, "max_frontier": 1}
    frontier, reached = [Node(problem.initial)], {problem.initial}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node, stats
        stats["expanded"] += 1
        for child in reversed(list(expand(problem, node))):
            if child.state not in reached:
                reached.add(child.state)
                frontier.append(child)
        stats["max_frontier"] = max(stats["max_frontier"], len(frontier))
    return None, stats


def depth_limited(problem, limit, stats=None):
    """Recursive DFS to a fixed depth; avoids cycles along the path."""
    stats = stats if stats is not None else {"expanded": 0}

    def recurse(node, on_path):
        if problem.is_goal(node.state):
            return node
        if node.depth == limit:
            return None
        stats["expanded"] += 1
        for child in expand(problem, node):
            if child.state not in on_path:
                found = recurse(child, on_path | {child.state})
                if found:
                    return found
        return None
    return recurse(Node(problem.initial), {problem.initial}), stats


def iterative_deepening(problem, max_depth=50):
    stats = {"expanded": 0}
    for limit in range(max_depth + 1):
        found, _ = depth_limited(problem, limit, stats)
        if found:
            stats["limit"] = limit
            return found, stats
    return None, stats


def best_first(problem, f):
    """Priority-queue search on f(node); goal test when a node is
    expanded, so that the first goal taken from the queue is the best."""
    stats = {"expanded": 0, "max_frontier": 1}
    tie = count()                       # breaks ties in insertion order
    start = Node(problem.initial)
    frontier = [(f(start), next(tie), start)]
    best_g = {problem.initial: 0}
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node.g > best_g.get(node.state, float("inf")):
            continue                    # a cheaper copy was found later
        if problem.is_goal(node.state):
            return node, stats
        stats["expanded"] += 1
        for child in expand(problem, node):
            if child.g < best_g.get(child.state, float("inf")):
                best_g[child.state] = child.g
                heapq.heappush(frontier, (f(child), next(tie), child))
        stats["max_frontier"] = max(stats["max_frontier"], len(frontier))
    return None, stats


def uniform_cost(problem):
    return best_first(problem, lambda n: n.g)


def greedy(problem):
    return best_first(problem, lambda n: problem.h(n.state))


def astar(problem):
    return best_first(problem, lambda n: n.g + problem.h(n.state))

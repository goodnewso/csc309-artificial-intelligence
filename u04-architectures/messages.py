"""messages.py: communicating agents searching a network.

Each node of a small network is an agent that knows only its own files
and its neighbours.  A QUERY message is passed from agent to agent with a
time-to-live (TTL); an agent that has the file sends a HIT back along the
path the query came by.  Agents ignore a query they have already seen.
"""
from collections import deque

NETWORK = {"A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
           "D": ["B", "G"], "E": ["B", "F"], "F": ["C", "E", "H"],
           "G": ["D"], "H": ["F"]}
FILES = {"G": {"ai-notes.pdf"}, "H": {"ai-notes.pdf", "timetable.xls"},
         "E": {"timetable.xls"}}


class Agent:
    def __init__(self, name):
        self.name, self.seen, self.log = name, set(), []

    def receive(self, msg, outbox):
        kind, qid, item, path, ttl = msg
        if kind == "QUERY":
            if qid in self.seen:
                return                       # duplicate: ignore it
            self.seen.add(qid)
            if item in FILES.get(self.name, set()):
                # reply to the sender, along the reverse of the path
                outbox.append((path[-1], ("HIT", qid, self.name,
                                          path[:-1], 0)))
            if ttl > 1:
                for nb in NETWORK[self.name]:
                    if nb not in path:
                        outbox.append((nb, ("QUERY", qid, item,
                                            path + [self.name], ttl - 1)))
        elif kind == "HIT":                  # pass the answer back
            self.log.append(f"hit from {item}")
            outbox.append((path[-1], (kind, qid, item, path[:-1], 0)))


def search(start, item, ttl):
    agents = {n: Agent(n) for n in NETWORK}
    agents[start].seen.add(1)
    queue = deque((nb, ("QUERY", 1, item, [start], ttl))
                  for nb in NETWORK[start])
    sent = len(queue)
    hits = []
    while queue:
        to, msg = queue.popleft()
        if msg[0] == "HIT" and to == start:
            hits.append(msg[2])
            continue
        outbox = []
        agents[to].receive(msg, outbox)
        sent += len(outbox)
        queue.extend(outbox)
    return sorted(set(hits)), sent


if __name__ == "__main__":
    for ttl in (1, 2, 3, 4):
        found, sent = search("A", "ai-notes.pdf", ttl)
        print(f"TTL {ttl}: found at {found or 'nowhere'}, {sent} messages")

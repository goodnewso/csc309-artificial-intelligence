"""spell.py: a spelling corrector built on edit distance and word
frequency.  Candidates are known words within one or two edits
(delete, insert, replace, transpose); the most frequent is chosen.
"""
import re
from collections import Counter

CORPUS = """artificial intelligence is the study of agents that perceive
their environment and act rationally an intelligent agent uses search
knowledge and reasoning to choose actions search algorithms explore a
state space heuristic search uses knowledge to guide the search the
knowledge base of an expert system holds rules and facts the inference
engine applies the rules natural language processing lets computers
understand language and machine learning lets agents improve with
experience the student must study the lecture note before the examination
the examination tests knowledge of search knowledge representation
reasoning language and learning"""
COUNTS = Counter(re.findall(r"[a-z]+", CORPUS))
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def edits1(w):
    splits = [(w[:i], w[i:]) for i in range(len(w) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits if b for c in LETTERS]
    inserts = [a + c + b for a, b in splits for c in LETTERS]
    return set(deletes + transposes + replaces + inserts)


def known(ws):
    return {w for w in ws if w in COUNTS}


def correct(word):
    candidates = (known([word]) or known(edits1(word))
                  or known(e2 for e1 in edits1(word) for e2 in edits1(e1))
                  or {word})
    return max(candidates, key=lambda w: COUNTS[w])


def distance(a, b):
    """Levenshtein distance by dynamic programming."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


if __name__ == "__main__":
    print(f"{len(COUNTS)} known words; edits1('serch') has "
          f"{len(edits1('serch'))} strings")
    for typo in ["serch", "knowlege", "inteligence", "agnet", "lecutre",
                 "examnation", "zebra"]:
        fix = correct(typo)
        print(f"{typo:12} -> {fix:12} (distance {distance(typo, fix)})")

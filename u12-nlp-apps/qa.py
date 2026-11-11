"""qa.py: a small question-answering system over course facts.

Two techniques:
  1. pattern-based: a question pattern maps to a database query;
  2. retrieval-based: otherwise, return the sentence of the handbook text
     that shares the most (weighted) words with the question.
"""
import math
import re
from collections import Counter

FACTS = {("CSC 309", "units"): "2", ("CSC 309", "level"): "300",
         ("CSC 309", "lab hours"): "45", ("CSC 308", "units"): "3",
         ("CSC 308", "level"): "300"}
TEXT = """CSC 309 introduces artificial intelligence. The course covers
intelligent agents, search, knowledge representation, natural language
processing and expert systems. An expert system has a knowledge base and
an inference engine. The Turing test asks whether a judge can tell a
machine from a person in conversation. A heuristic is a rule of thumb that
estimates how close a state is to a goal. Laboratory work includes a
chatbot and a spam filter."""
STOP = {"a", "an", "the", "is", "of", "and", "what", "how", "does", "do",
        "to", "in", "from", "can", "whether", "which", "that", "has"}
PATTERNS = [
    (r"how many (lab hours|units) (?:does|has) (\w+ \d+)",
     lambda m: FACTS.get((m.group(2).upper(), m.group(1)))),
    (r"(?:what|which) level is (\w+ \d+)",
     lambda m: FACTS.get((m.group(1).upper(), "level"))),
]
SENTENCES = [s.strip().replace("\n", " ")
             for s in re.split(r"(?<=\.)\s+", TEXT)]


def tokens(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP]


DF = Counter(w for s in SENTENCES for w in set(tokens(s)))


def retrieve(question):
    q = set(tokens(question))
    def score(s):           # rarer shared words count more (IDF weights)
        return sum(math.log(len(SENTENCES) / DF[w])
                   for w in q & set(tokens(s)))
    best = max(SENTENCES, key=score)
    return best if score(best) > 0 else "Sorry, I do not know."


def answer(question):
    q = question.lower().rstrip("?")
    for pattern, action in PATTERNS:
        m = re.search(pattern, q)
        if m and action(m):
            return action(m)
    return retrieve(question)


if __name__ == "__main__":
    for q in ["How many units does CSC 309 have?",
              "What level is CSC 308?",
              "How many lab hours does CSC 309 have?",
              "What is a heuristic?",
              "What does an expert system have?",
              "What is the Turing test?",
              "Who won the league?"]:
        print(f"Q: {q}\nA: {answer(q)}")

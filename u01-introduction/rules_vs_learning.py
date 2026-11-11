"""Unit 1: writing the rules by hand versus learning them from data.

Task: decide whether a text message is a scam. A programmer writes rules;
a learning program is shown labelled examples and finds its own rules.
"""
import textwrap
from collections import Counter

train = [
    ("scam", "you have won a prize send your bank pin now"),
    ("scam", "urgent your account is blocked send bvn to unblock"),
    ("scam", "congratulations claim your free data bundle now"),
    ("ok", "lecture holds at ten in the faculty hall"),
    ("ok", "please send the lab report before friday"),
    ("ok", "your exam timetable is now on the portal"),
]
test = [
    ("scam", "claim your prize now send pin"),
    ("ok", "the lab holds on friday in the faculty"),
    ("scam", "your account is blocked click to unblock"),
    ("ok", "please check the portal for your results"),
]


def by_rules(text):                      # rules written by a person
    return "scam" if ("prize" in text or "pin" in text) else "ok"


def learn(examples):                     # count which words go with scams
    scam, ok = Counter(), Counter()
    for label, text in examples:
        (scam if label == "scam" else ok).update(text.split())
    return {w for w in scam if scam[w] > ok[w]}


scam_words = learn(train)


def by_learning(text):
    words = text.split()
    hits = sum(w in scam_words for w in words)
    return "scam" if hits >= 2 else "ok"


print("words the program learnt to link with scams:")
print(textwrap.fill(", ".join(sorted(scam_words)), 72,
                    initial_indent="  ", subsequent_indent="  "))
for name, f in [("hand-written rules", by_rules),
                ("learnt rules", by_learning)]:
    right = sum(f(t) == label for label, t in test)
    print(f"{name:18s}: {right} of {len(test)} test messages correct")

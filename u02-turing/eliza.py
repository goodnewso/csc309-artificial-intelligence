"""eliza.py: a tiny ELIZA-style conversation program (after Weizenbaum,
1966).  It understands nothing: it matches patterns, swaps pronouns and
fills in templates, yet it can seem to listen.  Run it with no arguments
to talk to it, or let the scripted conversation below play.
"""
import random
import re
import sys

REFLECT = {"i": "you", "me": "you", "my": "your", "am": "are",
           "you": "I", "your": "my", "i'm": "you are", "mine": "yours"}

RULES = [                                   # (pattern, replies)
    (r"i need (.*)", ["Why do you need {0}?",
                      "Would {0} really help you?"]),
    (r"i am (.*)", ["How long have you been {0}?",
                    "Why do you say you are {0}?"]),
    (r"i feel (.*)", ["What makes you feel {0}?",
                      "Do you often feel {0}?"]),
    (r"(.*) exam(.*)", ["Exams can be stressful. How are you preparing?"]),
    (r"(.*) mother|(.*) father(.*)", ["Tell me more about your family."]),
    (r"are you (.*)", ["Why does it matter whether I am {0}?"]),
    (r"(.*)\?", ["Why do you ask that?", "What do you think?"]),
    (r"(.*)", ["Please go on.", "I see. Tell me more.",
               "How does that make you feel?"]),
]


def reflect(text):
    words = text.lower().strip(" ?").split()
    return " ".join(REFLECT.get(w, w) for w in words)


def reply(sentence, rng):
    s = sentence.lower().strip(" .!")
    for pattern, answers in RULES:
        m = re.fullmatch(pattern, s)
        if m:
            parts = [reflect(g) for g in m.groups() if g is not None]
            return rng.choice(answers).format(*parts)


if __name__ == "__main__":
    rng = random.Random(309)
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        while (line := input("> ")) not in ("bye", ""):
            print(reply(line, rng))
    else:
        for line in ["I am worried about my CSC 309 exam",
                     "I need more time to read",
                     "I feel that my notes are not enough",
                     "Are you a computer?",
                     "My father wants me to study medicine",
                     "The weather is hot today"]:
            print("Student:", line)
            print("ELIZA:  ", reply(line, rng))

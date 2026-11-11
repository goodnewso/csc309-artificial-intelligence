"""chatbot.py: an intent-based chatbot for student services.

Each intent has example phrases and a response.  A message is matched to
the intent whose examples share the most words with it (after removing
common words and reducing words to a crude stem).  A confidence threshold
sends unclear messages to a human.
"""
import re

INTENTS = {
    "greeting": (["hello", "hi there", "good morning"],
                 "Hello! How can I help you today?"),
    "fees": (["how do I pay my school fees", "fee payment portal",
              "pay fees"],
             "Pay fees on the University portal; keep your receipt."),
    "transcript": (["how do I get my transcript",
                    "request academic transcript"],
                   "Apply for transcripts at the Exams and Records unit."),
    "timetable": (["when is the exam", "examination timetable",
                   "when are lectures"],
                  "Timetables are on the Faculty notice board and portal."),
    "hostel": (["hostel accommodation", "how do I get a room in hostel"],
               "Hostel spaces are allocated through Student Affairs."),
    "thanks": (["thank you", "thanks"], "You are welcome!"),
}
STOP = {"i", "my", "a", "the", "do", "is", "how", "to", "me", "can",
        "you", "when", "are", "get", "in", "of", "at", "please", "what",
        "there", "where", "need"}


def stem(w):
    for suffix in ("ation", "ing", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            return w[: -len(suffix)]
    return w


def bag(text):
    return {stem(w) for w in re.findall(r"[a-z]+", text.lower())
            if w not in STOP}


def respond(message):
    words = bag(message)
    best, best_score = None, 0.0
    for intent, (examples, _) in INTENTS.items():
        for ex in examples:
            e = bag(ex)
            score = len(words & e) / len(words | e) if words | e else 0
            if score > best_score:
                best, best_score = intent, score
    if best_score < 0.2:
        return "fallback", "I am not sure. Let me pass you to a staff member."
    return best, INTENTS[best][1]


if __name__ == "__main__":
    for msg in ["Good morning", "Where can I pay my fees?",
                "I need my transcript", "When is the examination?",
                "Is there space in the hostels?", "Who is the Dean?",
                "Thanks!"]:
        intent, text = respond(msg)
        print(f"Student: {msg}\nBot [{intent}]: {text}")

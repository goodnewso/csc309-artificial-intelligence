"""example_keyword_bot.py: a bookshop assistant that only matches keywords.

It can look intelligent for a few turns, but it understands nothing:
this is the point of Searle's Chinese Room.
"""
RULES = [
    (("price", "cost", "how much"), "Most textbooks cost between N5,000 "
                                    "and N12,000."),
    (("open", "time", "hour"), "We open 8 a.m. to 6 p.m., Monday to "
                               "Saturday."),
    (("deliver",), "Yes, we deliver within the city for N1,500."),
]

def reply(text):
    text = text.lower()
    for keys, answer in RULES:
        if any(k in text for k in keys):
            return answer
    return "Interesting. Tell me more."     # fallback hides ignorance

for q in ["How much is the AI textbook?", "Do you deliver to Rumuola?",
          "Why is the sky blue?"]:
    print("User:", q)
    print("Bot: ", reply(q))

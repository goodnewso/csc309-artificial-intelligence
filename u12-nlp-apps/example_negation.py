"""example_negation.py: lexicon-based sentiment with negation and
intensifiers."""
LEXICON = {"good": 2, "great": 3, "bad": -2, "slow": -1, "friendly": 2}
INTENSIFIERS = {"very": 1.5, "really": 1.5}
NEGATIONS = {"not", "never", "no"}

def score(text):
    total, flip, boost = 0, 1, 1
    for w in text.lower().replace(".", "").split():
        if w in NEGATIONS:
            flip = -1
        elif w in INTENSIFIERS:
            boost = INTENSIFIERS[w]
        elif w in LEXICON:
            total += flip * boost * LEXICON[w]
            flip, boost = 1, 1                  # reset after a word
    return total

for review in ["The service was good.", "The service was not good.",
               "The service was very good.", "Friendly staff but very slow."]:
    print(f"{score(review):+5.1f}  {review}")

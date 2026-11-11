"""sentiment.py: lexicon-based sentiment analysis with negation and
intensifiers.  Each word has a polarity score; "not" flips the next
sentiment word and "very" strengthens it.
"""
import re

LEXICON = {"good": 2, "great": 3, "excellent": 3, "clear": 2, "helpful": 2,
           "interesting": 2, "love": 3, "like": 1, "easy": 1,
           "bad": -2, "poor": -2, "boring": -2, "confusing": -2,
           "hard": -1, "late": -1, "terrible": -3, "hate": -3, "slow": -1}
NEGATORS = {"not", "never", "no", "isn't", "wasn't", "don't", "didn't"}
BOOST = {"very": 1.5, "really": 1.5, "too": 1.3, "so": 1.3}


def score(text):
    total, flip, boost = 0.0, False, 1.0
    for w in re.findall(r"[a-z']+", text.lower()):
        if w in NEGATORS:
            flip = True
        elif w in BOOST:
            boost *= BOOST[w]
        elif w in LEXICON:
            v = LEXICON[w] * boost
            total += -v if flip else v
            flip, boost = False, 1.0
    return total


def label(s):
    return "positive" if s > 0.5 else "negative" if s < -0.5 else "neutral"


if __name__ == "__main__":
    for review in ["The lectures were very clear and helpful.",
                   "The practical was not easy but it was interesting.",
                   "The notes came late and the slides were confusing.",
                   "I don't like the timetable.",
                   "The class holds in Hall B."]:
        s = score(review)
        print(f"{s:6.1f}  {label(s):8}  {review}")

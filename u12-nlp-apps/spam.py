"""spam.py: a naive Bayes filter for unwanted text messages.

Training messages are invented for teaching.  Each message is a bag of
words; for each class c we estimate P(c) and P(word | c) with add-one
(Laplace) smoothing, and classify by the larger
    log P(c) + sum of log P(word | c).
"""
import math
import re
from collections import Counter

TRAIN = [
    ("spam", "urgent your bvn is blocked send your pin now"),
    ("spam", "congratulations you won a prize claim now"),
    ("spam", "your account will be closed update bvn urgent"),
    ("spam", "win cash now send pin to claim prize"),
    ("spam", "free data bundle click link to claim now"),
    ("spam", "dear customer verify your account send otp"),
    ("ham", "lecture moved to hall b at ten tomorrow"),
    ("ham", "please send the lab report before friday"),
    ("ham", "are you coming to the group meeting today"),
    ("ham", "the csc 309 test holds on monday"),
    ("ham", "mummy says call her when you get home"),
    ("ham", "can you send me the lecture note please"),
]


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


class NaiveBayes:
    def fit(self, data):
        self.docs = Counter(c for c, _ in data)
        self.counts = {c: Counter() for c in self.docs}
        for c, text in data:
            self.counts[c].update(words(text))
        self.vocab = set().union(*self.counts.values())
        return self

    def log_scores(self, text):
        n = sum(self.docs.values())
        scores = {}
        for c in self.docs:
            total = sum(self.counts[c].values())
            s = math.log(self.docs[c] / n)
            for w in words(text):
                if w in self.vocab:        # unknown words are ignored
                    s += math.log((self.counts[c][w] + 1)
                                  / (total + len(self.vocab)))
            scores[c] = s
        return scores

    def predict(self, text):
        s = self.log_scores(text)
        best = max(s, key=s.get)
        p = 1 / (1 + math.exp(-(s["spam"] - s["ham"])))   # P(spam|text)
        return best, p


if __name__ == "__main__":
    model = NaiveBayes().fit(TRAIN)
    print(f"{len(TRAIN)} training messages, {len(model.vocab)} words")
    for msg in ["URGENT: send your BVN and PIN to claim your prize",
                "Please bring the lab report to the lecture",
                "Your data bundle: click the link now",
                "Group meeting moved to Monday"]:
        label, p = model.predict(msg)
        print(f"{label:4}  P(spam) = {p:.3f}  {msg}")

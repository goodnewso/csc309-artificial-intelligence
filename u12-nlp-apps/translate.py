"""translate.py: why machine translation needs more than a dictionary.

A word-for-word English-to-French translator, then the same with three
transfer rules: French adjectives of colour follow the noun, articles
and adjectives agree with the noun's gender, and le/la become l' before
a vowel.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):      # print logic symbols on Windows
    sys.stdout.reconfigure(encoding="utf-8")
DICT = {"the": "le", "a": "un", "black": "noir", "white": "blanc",
        "cat": "chat", "house": "maison", "student": "étudiant",
        "sees": "voit", "eats": "mange", "big": "grand", "fish": "poisson"}
FEMININE = {"maison"}
AFTER_NOUN = {"noir", "blanc"}             # adjectives placed after noun
FEM_FORM = {"le": "la", "un": "une", "noir": "noire", "blanc": "blanche",
            "grand": "grande"}


def word_for_word(sentence):
    return " ".join(DICT.get(w, w) for w in sentence.lower().split())


def with_rules(sentence):
    words = [DICT.get(w, w) for w in sentence.lower().split()]
    out, i = [], 0
    while i < len(words):
        w = words[i]
        if w in AFTER_NOUN and i + 1 < len(words):   # swap ADJ NOUN
            out += [words[i + 1], w]
            i += 2
        else:
            out.append(w)
            i += 1
    # agreement: words next to a feminine noun take the feminine form
    for k, w in enumerate(out):
        if w in FEMININE:
            for j in (k - 2, k - 1, k + 1):
                if 0 <= j < len(out) and out[j] in FEM_FORM:
                    out[j] = FEM_FORM[out[j]]
    # elision: le / la before a vowel becomes l'
    text = " ".join(out)
    for art in ("le ", "la "):
        for v in "aeiouéè":
            text = text.replace(art + v, "l'" + v)
    return text


if __name__ == "__main__":
    for s in ["the student sees a black cat",
              "the cat eats a big fish",
              "the student sees the white house"]:
        print(f"English:        {s}")
        print(f"word for word:  {word_for_word(s)}")
        print(f"with rules:     {with_rules(s)}\n")

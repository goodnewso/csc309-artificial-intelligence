"""cfgparse.py: tokenising, tagging and parsing English with a small
context-free grammar.  The parser returns EVERY parse tree, so it shows
structural ambiguity.
"""
import re

LEXICON = {
    "Det": {"the", "a", "every", "some"},
    "N": {"student", "lecturer", "note", "binoculars", "hall", "course"},
    "PropN": {"Ada", "Amaka", "Chidi"},
    "V": {"saw", "reads", "teaches", "passes", "likes"},
    "P": {"with", "in", "on"},
}
GRAMMAR = {                      # left side -> list of right sides
    "S": [["NP", "VP"]],
    "NP": [["Det", "N"], ["Det", "N", "PP"], ["PropN"]],
    "VP": [["V", "NP"], ["V", "NP", "PP"], ["V"]],
    "PP": [["P", "NP"]],
}


def tokenise(text):
    """Split into words; lower-case all but proper names."""
    return [w if w in LEXICON["PropN"] else w.lower()
            for w in re.findall(r"[A-Za-z]+", text)]


def tags(word):
    return [t for t, words in LEXICON.items() if word in words]


def parse(symbol, words, i):
    """Yield (tree, next position) for every way `symbol` can cover
    words[i:...].  Top-down, depth-first, with backtracking."""
    if symbol in LEXICON:
        if i < len(words) and words[i] in LEXICON[symbol]:
            yield (symbol, words[i]), i + 1
        return
    for rhs in GRAMMAR[symbol]:
        yield from parse_seq(rhs, words, i, [symbol])


def parse_seq(rhs, words, i, built):
    if not rhs:
        yield tuple(built), i
        return
    for tree, j in parse(rhs[0], words, i):
        yield from parse_seq(rhs[1:], words, j, built + [tree])


def parses(sentence):
    words = tokenise(sentence)
    return [t for t, j in parse("S", words, 0) if j == len(words)]


def bracket(tree):
    if isinstance(tree[1], str):
        return f"[{tree[0]} {tree[1]}]"
    return f"[{tree[0]} " + " ".join(bracket(t) for t in tree[1:]) + "]"


def draw(tree, indent=""):
    if isinstance(tree[1], str):
        print(f"{indent}{tree[0]}: {tree[1]}")
        return
    print(f"{indent}{tree[0]}")
    for child in tree[1:]:
        draw(child, indent + "  ")


if __name__ == "__main__":
    s = "Ada saw the student with the binoculars."
    words = tokenise(s)
    print("tokens:", words)
    print("tags:  ", [(w, tags(w)) for w in words])
    trees = parses(s)
    print(f"{len(trees)} parses:")
    for t in trees:
        print(" ", bracket(t))
    print("\nThe first parse as a tree:")
    draw(trees[0])
    print("\nUngrammatical:", "student the saw Ada",
          "->", len(parses("student the saw Ada")), "parses")

"""example_pipeline.py: the first levels of language analysis.

Tokenisation, a crude lemmatiser (suffix rules) and part-of-speech
tagging by dictionary lookup.
"""
import re

TAGS = {"the": "Det", "a": "Det", "farmer": "N", "goat": "N", "yam": "N",
        "market": "N", "sell": "V", "carry": "V", "to": "P", "at": "P"}

def tokenise(text):
    return re.findall(r"[a-z]+", text.lower())

def lemma(word):
    for suffix, repl in (("ied", "y"), ("ies", "y"), ("ing", ""), ("ed", ""),
                         ("es", ""), ("s", "")):
        if word.endswith(suffix) and word[:-len(suffix)] + repl in TAGS:
            return word[:-len(suffix)] + repl
    return word

sentence = "The farmers carried yams to the market."
for w in tokenise(sentence):
    lw = lemma(w)
    print(f"{w:<9} lemma={lw:<7} tag={TAGS.get(lw, '?')}")

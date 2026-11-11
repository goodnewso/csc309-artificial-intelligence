"""bayes.py: probabilistic reasoning about a suspicious text message.

Bayes' rule:  P(H | E) = P(E | H) P(H) / P(E),
where P(E) = P(E | H) P(H) + P(E | not H) P(not H).
The numbers are illustrative, not measured.
"""
P_SCAM = 0.10                               # prior: 1 message in 10
EVIDENCE = {                                # word: (P(w|scam), P(w|genuine))
    "urgent": (0.60, 0.05),
    "bvn": (0.40, 0.02),                    # bank verification number
    "lecture": (0.01, 0.20),
}


def posterior(words, prior=P_SCAM):
    """Update the belief one word at a time (naive Bayes: the words are
    assumed independent given the class)."""
    p = prior
    for w in words:
        like_scam, like_ok = EVIDENCE[w]
        p = like_scam * p / (like_scam * p + like_ok * (1 - p))
        print(f"  after '{w}': P(scam) = {p:.3f}")
    return p


if __name__ == "__main__":
    print(f"prior P(scam) = {P_SCAM}")
    print("Message contains 'urgent':")
    posterior(["urgent"])
    print("Message contains 'urgent' and 'bvn':")
    posterior(["urgent", "bvn"])
    print("Message contains 'lecture':")
    posterior(["lecture"])

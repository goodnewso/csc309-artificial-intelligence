"""Unit 12: speech recognition by template matching with dynamic time
warping (DTW), the method of early isolated-word recognisers.

Real systems compute features (such as MFCCs) from recorded sound; here
each "utterance" is a SIMULATED sequence of 2-number feature frames, so
the program needs no microphone. People say words at different speeds,
so DTW stretches time to line two sequences up before comparing them.
"""
import numpy as np

rng = np.random.default_rng(309)
shapes = {                       # feature patterns of three spoken words
    "yes": [(0, 0), (3, 1), (3, 4), (1, 4)],
    "no": [(0, 0), (1, 3), (4, 3), (4, 0)],
    "stop": [(0, 0), (4, 0), (4, 4), (0, 4)],
}


def utterance(word, frames_per_part):
    """Interpolate the word's pattern, at a given speaking speed."""
    pts = np.array(shapes[word], float)
    seq = [pts[i] + (pts[i + 1] - pts[i]) * t
           for i in range(len(pts) - 1)
           for t in np.linspace(0, 1, frames_per_part, endpoint=False)]
    return np.array(seq) + rng.normal(0, 0.3, (len(seq), 2))


def dtw(a, b):
    n, m = len(a), len(b)
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = np.linalg.norm(a[i - 1] - b[j - 1])
            D[i, j] = cost + min(D[i - 1, j], D[i, j - 1], D[i - 1, j - 1])
    return D[n, m] / (n + m)


templates = {w: utterance(w, 8) for w in shapes}       # recorded once
for word, speed in [("yes", 4), ("no", 13), ("stop", 6), ("yes", 11)]:
    spoken = utterance(word, speed)                     # said fast/slow
    scores = {w: dtw(spoken, t) for w, t in templates.items()}
    best = min(scores, key=scores.get)
    shown = "  ".join(f"{w}={s:.2f}" for w, s in scores.items())
    print(f"said '{word}' ({len(spoken):2d} frames): {shown} -> heard "
          f"'{best}'")

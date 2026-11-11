"""faces.py: a simulation of facial recognition by feature vectors.

A real system finds a face, measures it (today with a neural network that
outputs a vector of numbers, an "embedding") and compares vectors.  Here
each person is described by five measurements in millimetres; every new
photograph measures them with some error.  A face is VERIFIED if its
nearest enrolled face is closer than a threshold; otherwise it is
reported as unknown.
"""
import math
import random

FEATURES = ["eye distance", "nose length", "mouth width",
            "face width", "forehead height"]
PEOPLE = {"Amaka": [60, 48, 50, 135, 58], "Tamuno": [66, 54, 56, 147, 66],
          "Ngozi": [56, 44, 47, 128, 62], "Daniel": [70, 52, 60, 152, 60]}


def photo(true, rng, noise=1.0):              # one noisy measurement
    return [v + rng.gauss(0, noise) for v in true]


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def recognise(face, gallery, threshold):
    name, d = min(((n, dist(face, v)) for n, v in gallery.items()),
                  key=lambda t: t[1])
    return (name if d < threshold else "unknown"), d


if __name__ == "__main__":
    rng = random.Random(309)
    gallery = {n: photo(v, rng) for n, v in PEOPLE.items()}   # enrolment
    visitor = [63, 50, 53, 140, 63]                # not enrolled
    print(f"{'threshold':>9}{'correct':>9}{'wrong':>7}{'rejected':>10}"
          f"{'stranger let in':>17}")
    for threshold in (2, 4, 6, 8, 10):
        right = wrong = rejected = stranger = 0
        for _ in range(200):
            who = rng.choice(list(PEOPLE))
            got, _ = recognise(photo(PEOPLE[who], rng), gallery, threshold)
            if got == who: right += 1
            elif got == "unknown": rejected += 1
            else: wrong += 1
            got, _ = recognise(photo(visitor, rng), gallery, threshold)
            stranger += got != "unknown"
        print(f"{threshold:>9}{right:>9}{wrong:>7}{rejected:>10}"
              f"{stranger:>13} of 200")

"""digits.py: recognising handwritten digits with k-nearest neighbours.

The data are the 1,797 8 x 8 grey-level images of digits that come with
scikit-learn.  Each image is a vector of 64 numbers (0 = white, 16 =
black).  To classify a new image, find the k most similar training
images (smallest Euclidean distance) and take a vote.
"""
from collections import Counter

import numpy as np
from sklearn.datasets import load_digits

data = load_digits()
X, y = data.data, data.target
rng = np.random.default_rng(309)
order = rng.permutation(len(X))
train, test = order[:1200], order[1200:]            # 1200 / 597 images


def show(img):
    shades = " .:-=+*#%@"
    for row in img.reshape(8, 8):
        print("    " + "".join(shades[int(v * 9 / 16)] * 2 for v in row))


def knn(x, k):
    d = np.sqrt(((X[train] - x) ** 2).sum(axis=1))   # distances to all
    nearest = train[np.argsort(d)[:k]]
    return Counter(y[nearest]).most_common(1)[0][0]


if __name__ == "__main__":
    print(f"{len(X)} images of {X.shape[1]} pixels; "
          f"{len(train)} for training, {len(test)} for testing")
    print(f"test image {test[0]} (label {y[test[0]]}):")
    show(X[test[0]])
    for k in (1, 3, 5):
        pred = np.array([knn(X[i], k) for i in test])
        acc = (pred == y[test]).mean()
        print(f"k = {k}: accuracy {acc:.3f} "
              f"({(pred != y[test]).sum()} mistakes)")
    pred = np.array([knn(X[i], 3) for i in test])
    wrong = Counter((int(a), int(b)) for a, b in zip(y[test], pred) if a != b)
    print("most common mistakes (true -> predicted):",
          ", ".join(f"{a}->{b} x{n}" for (a, b), n in wrong.most_common(3)))

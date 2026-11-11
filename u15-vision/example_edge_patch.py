"""example_edge_patch.py: a 3 x 3 kernel finding a vertical edge."""
import numpy as np

image = np.array([[10, 10, 200, 200],
                  [10, 10, 200, 200],
                  [10, 10, 200, 200],
                  [10, 10, 200, 200]])
kernel = np.array([[-1, 0, 1],               # Sobel: left-to-right change
                   [-2, 0, 2],
                   [-1, 0, 1]])

rows, cols = image.shape
out = np.zeros((rows - 2, cols - 2), dtype=int)
for r in range(rows - 2):
    for c in range(cols - 2):
        out[r, c] = (image[r:r + 3, c:c + 3] * kernel).sum()
print("image:\n", image)
print("edge response:\n", out)

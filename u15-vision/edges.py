"""edges.py: finding edges in an image by convolution.

An image is a grid of brightness values.  Sliding a small 3 x 3 kernel
over it and summing the products gives a new image; the Sobel kernel
below responds strongly where brightness changes from left to right,
i.e. at vertical edges.  Early layers of a convolutional neural network
learn kernels like this one by themselves.
"""
IMAGE = [[0, 0, 0, 0, 0, 0, 0, 0],             # a bright square on dark
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 9, 9, 9, 9, 0, 0],
         [0, 0, 9, 9, 9, 9, 0, 0],
         [0, 0, 9, 9, 9, 9, 0, 0],
         [0, 0, 9, 9, 9, 9, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]
SOBEL_X = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]


def convolve(img, k):
    h, w = len(img), len(img[0])
    return [[sum(k[i][j] * img[r + i - 1][c + j - 1]
                 for i in range(3) for j in range(3))
             for c in range(1, w - 1)] for r in range(1, h - 1)]


if __name__ == "__main__":
    print("image:")
    for row in IMAGE:
        print("  " + " ".join(f"{v:3}" for v in row))
    print("after the vertical-edge (Sobel x) kernel:")
    for row in convolve(IMAGE, SOBEL_X):
        print("  " + " ".join(f"{v:3}" for v in row))

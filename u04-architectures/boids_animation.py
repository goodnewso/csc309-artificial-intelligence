"""Unit 4: an AI animation exercise: animate a flock of boids.

Each bird follows three local rules (separation, alignment, cohesion);
the flock emerges. The animation is saved as figures/boids.gif.
Change the rule weights and watch the behaviour change.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

N, SIZE, FRAMES = 40, 100.0, 120
W_SEP, W_ALI, W_COH = 1.5, 1.0, 0.8        # try changing these
rng = np.random.default_rng(309)
pos = rng.uniform(0, SIZE, (N, 2))
vel = rng.normal(0, 1, (N, 2))


def step():
    global pos, vel
    diff = pos[:, None, :] - pos[None, :, :]
    dist = np.linalg.norm(diff, axis=2) + np.eye(N) * 1e9
    near = dist < 15
    close = dist < 5
    sep = (diff * close[..., None]).sum(axis=1)
    cnt = near.sum(axis=1, keepdims=True).clip(min=1)
    ali = (vel[None, :, :] * near[..., None]).sum(axis=1) / cnt - vel
    coh = (pos[None, :, :] * near[..., None]).sum(axis=1) / cnt - pos
    coh[near.sum(axis=1) == 0] = 0
    vel = vel + 0.05 * (W_SEP * sep + W_ALI * ali + W_COH * coh)
    speed = np.linalg.norm(vel, axis=1, keepdims=True)
    vel = vel / speed.clip(min=1e-9) * 1.5
    pos = (pos + vel) % SIZE


def order():                                # 1 = all fly the same way
    v = vel / np.linalg.norm(vel, axis=1, keepdims=True)
    return np.linalg.norm(v.mean(axis=0))


fig, ax = plt.subplots(figsize=(4, 4))
dots = ax.quiver(pos[:, 0], pos[:, 1], vel[:, 0], vel[:, 1], color="#2a7f62")
ax.set(xlim=(0, SIZE), ylim=(0, SIZE), xticks=[], yticks=[])


def frame(i):
    step()
    dots.set_offsets(pos)
    dots.set_UVC(vel[:, 0], vel[:, 1])
    ax.set_title(f"frame {i}  order {order():.2f}")
    return (dots,)


print(f"order before: {order():.2f}")
out = Path(__file__).resolve().parent / "figures"
out.mkdir(exist_ok=True)
FuncAnimation(fig, frame, frames=FRAMES).save(out / "boids.gif",
                                              writer=PillowWriter(fps=15))
print(f"order after {FRAMES} frames: {order():.2f}")
print("saved figures/boids.gif")

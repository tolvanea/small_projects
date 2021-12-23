# Plots self similar fractalic curve between points (0,0) and (0,1)
# Does this by taking mid point between the points, then adding some
# random displacement to it, then iterates this recursicely

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1)
points = np.array([[0,0], [1,0]])
for i in range(12):
    points_new = np.zeros((len(points)*2 - 1, 2))
    for j in range(len(points_new)):
        if j%2 == 0:
            points_new[j] = points[j//2]
    for j in range(1, len(points_new)-1):
        if j%2 == 1:
            mid = (points_new[j-1] + points_new[j+1]) / 2
            l = np.linalg.norm(points_new[j-1] - points_new[j+1])
            points_new[j] = mid + np.random.randn(2) * l * 0.15
    points = points_new

ax.plot([0, 1], [0, 0], "o", ls="")
ax.plot(points_new[:,0], points_new[:,1])
ax.set_ylim([-0.55, 0.55])
ax.set_xlim([-0.05, 1.05])
ax.axis("equal")
plt.show()

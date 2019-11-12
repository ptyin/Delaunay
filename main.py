from pyhull.convex_hull import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
import random
import itertools
from mpl_toolkits.mplot3d import Axes3D


def downward(point, face) -> bool:  # judge whether a face is downward or not
    a1 = np.array([face[1][index] - face[0][index] for index in range(3)])
    a2 = np.array([face[2][index] - face[0][index] for index in range(3)])

    flat = np.cross(a1, a2)
    a = np.array([point[index] - face[0][index] for index in range(3)])
    print(a)

    if np.dot(flat, a) < 0:
        flat = -flat
    return flat[2] >= 0


def test():
    face = [[1, 0, 1], [0, 1, 1], [0, 0, 1]]
    pts = [[1, 0, 1], [0, 1, 1], [0, 0, 1], [0, 0, 0]]
    if downward(pts, face):
        print(pts)


fig = plt.figure(2)
ax1 = fig.add_subplot(111, projection='3d')
ax2 = fig.add_subplot(222)

n = input("Please input the number of random 3D points you want to generate(random range from x, y:-10000 to 10000):")
points = []
for i in range(int(n)):
    temp = [random.uniform(-10, 10), random.randint(-10, 10)]  # random number generator
    temp.append(temp[0] ** 2 + temp[1] ** 2)
    points.append(temp)

for pt in points:
    ax1.plot([pt[0]], [pt[1]], [0], 'ro')
    ax2.plot(pt[0], pt[1], 'ro')

    ax1.plot([pt[0]], [pt[1]], [pt[2]], 'ro')

d = ConvexHull(points)

central_point = [0, 0, 0]
for simplex in d.simplices:
    for index in range(3):
        central_point[index] += (simplex.coords[0][index] + simplex.coords[1][index] + simplex.coords[2][index]) / 3
for index in range(3):
    central_point[index] /= len(d.simplices)

lines = set()

for simplex in d.simplices:

    if not downward(central_point, simplex.coords):
        continue

    for index in range(3):
        lines.add(((*simplex.coords[index - 1][0:2],), (*simplex.coords[index][0:2],)))

print(lines)

for line in lines:
    ax1.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], [0, 0], 'g-')
    ax2.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], 'g-')

for s in d.simplices:
    for data in itertools.combinations(s.coords, 3):
        if downward(central_point, data):
            data = np.array(data)
            ax1.plot(data[:, 0], data[:, 1], data[:, 2], 'b-')
        else:
            data = np.array(data)
            ax1.plot(data[:, 0], data[:, 1], data[:, 2], 'r-')

plt.show()

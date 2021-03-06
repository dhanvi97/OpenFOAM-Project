import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

xs = []
ys = []
zs = []
with open("dakotaData.dat", "r") as f:
	for i, line in enumerate(f):
		if i > 0:
			x = float(line.split()[2])
			y = float(line.split()[3])
			z = float(line.split()[4])*-1
			if z > 1:
				xs.append(float(x))
				ys.append(float(y))
				zs.append(float(z))

c = zs

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
cmhot = plt.get_cmap("plasma")
surf = ax.scatter(xs, ys, zs, c = c, cmap = cmhot)
plt.show()

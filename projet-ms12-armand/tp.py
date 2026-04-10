import matplotlib.tri as tri
from pathlib import Path
import numpy as np
import pyff
import vec2d
import curves
import matplotlib.pyplot as plt


def r(curve, dir_inc, t):
    n = curve.N(t)
    a = vec2d.dot(dir_inc, n)
    if a < 0:
        t = curve.T(t)
        b = vec2d.dot(dir_inc, t)
        ref = -a*n + b*t
    else:
        return dir_inc
    return ref

origine_inc = vec2d.vec(-3.5, 0)
dir_inc = vec2d.vec(1, -1)
origine_inc.plotArrow(dir_inc, color="red")

L = 1
x_mesh = np.array([])
y_mesh = np.array([])

T = np.linspace(0, 2 * np.pi, 200)

e = curves.roundedPolygon(5) 
e.plot()
for t in T:
    refle = r(e, dir_inc, t)
    origine_t = e.M(t)
    origine_t.plotArrow(refle)
    for l in np.linspace(0, L, 10):
        x_mesh = np.append(x_mesh, origine_t.x + l*refle.x)
        y_mesh = np.append(y_mesh, origine_t.y + l*refle.y)
        ## Calcul de la phase de réflexion pour les points du maillage
        phase = 2*np.pi*vec2d.dot(origine_t - origine_inc, dir_inc) / vec2d.norm(dir_inc)
        # print(f"Point ({origine_t.x:.2f}, {origine_t.y:.2f}), phase de réflexion : {phase:.2f} radians")

points = np.column_stack((x_mesh, y_mesh))

# Supprimer les doublons
points_uniques = np.unique(points, axis=0)

# Séparer à nouveau x et y
x_mesh = points_uniques[:, 0]
y_mesh = points_uniques[:, 1]

Th = tri.Triangulation(x_mesh.flatten(), y_mesh.flatten())
Path("GO_data/").mkdir(parents=True, exist_ok=True)

plt.plot(x_mesh, y_mesh, 'x')
plt.triplot(Th)
pyff.savemesh(Th,"GO_data/mesh.msh")

# uh = np.cos(Th.x + Th.y)
# pyff.savevector(uh,"GO_data/uh.txt")

plt.axis("equal")
plt.show()
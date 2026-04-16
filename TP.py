import matplotlib.tri as tri
import matplotlib.pyplot as plt
import numpy as np
import curves
import vec2d
import pyff

obstacle = curves.circle()
# obstacle.plot()
# plt.axis("equal")
# plt.show()

x_min                = -2
theta_min, theta_max = np.pi/2, 3*np.pi/2
L                    = 3.5
nb_rayons            = 100
nb_points            = 50

rayons_init = np.linspace(theta_min, theta_max, nb_rayons) # paramètres des impacts de rayon sur la sphère
distances   = np.linspace(0, L, nb_points)

points   = obstacle.M(rayons_init)
normales = obstacle.N(rayons_init)

X_impact = points.x
Y_impact = points.y
S_impact = X_impact
n_x      = normales.x
n_y      = normales.y

X_total = []
Y_total = []
S_total = []
A_total = []

one = np.ones((nb_rayons,))

for distance in distances:

  v_ref = (1 - 2*n_x*n_x, -2*n_x*n_y)

  X_rayon = X_impact + distance*v_ref[0]
  Y_rayon = Y_impact + distance*v_ref[1]
  S_rayon = S_impact + distance*one

  n_x_safe = np.minimum(n_x, -1e-5) 
    
  J = 1 - (2 * distance) / n_x_safe
  A_rayon = -1.0 / np.sqrt(J)

  X_total.extend(X_rayon)
  Y_total.extend(Y_rayon)
  S_total.extend(S_rayon)
  A_total.extend(A_rayon)

# Th = tri.Triangulation(X_total, Y_total)

# 1. On laisse Delaunay faire son maillage brut (avec les mauvais triangles)
Th_brut = tri.Triangulation(X_total, Y_total)

# 2. On calcule les coordonnées (x,y) du centre de chaque triangle
triangles = Th_brut.triangles
x_centers = np.mean(Th_brut.x[triangles], axis=1)
y_centers = np.mean(Th_brut.y[triangles], axis=1)

# 3. On crée nos masques géométriques
# Condition A : Le centre doit être hors du cercle
hors_cercle = (x_centers**2 + y_centers**2) >= 0.99

# Condition B : Le centre doit être hors de la zone d'ombre (le couloir derrière l'obstacle)
# L'ombre est la zone où x > 0 et y est entre -0.99 et 0.99
hors_ombre = ~((x_centers > 0) & (np.abs(y_centers) < 0.99))

# On garde uniquement les triangles qui respectent les DEUX conditions
valides = hors_cercle & hors_ombre

# 4. On extrait uniquement les triangles valides
triangles_propres = triangles[valides]

# 5. On recrée l'objet Triangulation, mais cette fois propre et orienté correctement !
Th = tri.Triangulation(X_total, Y_total, triangles=triangles_propres)

# Sauvegarde habituelle
pyff.savemesh(Th, "exo/data/mesh.msh")
pyff.savevector(np.array(S_total), "exo/data/S.txt")
pyff.savevector(np.array(A_total), "exo/data/A.txt")

pyff.savemesh(Th, "exo/data/mesh.msh")
pyff.savevector(np.array(S_total), "exo/data/S.txt")
pyff.savevector(np.array(A_total), "exo/data/A.txt")

plt.figure(figsize=(10, 8))

# tracé q1 et q2
contour = plt.tricontourf(Th, S_total, levels=50, cmap='viridis')
plt.colorbar(contour, label='Phase S (Chemin optique)')

t_plot = np.linspace(0, 2*np.pi, 200)
plt.fill(obstacle.M(t_plot).x, obstacle.M(t_plot).y, color='white')

for i in range(nb_rayons):

    x_depart = x_min
    y_depart = Y_impact[i] 
    
    x_imp = X_impact[i]
    y_imp = Y_impact[i]
    
    v_ref_x = 1 - 2 * n_x[i]**2
    v_ref_y = -2 * n_x[i] * n_y[i]
    x_fin = x_imp + L * v_ref_x
    y_fin = y_imp + L * v_ref_y
    
    plt.plot([x_depart, x_imp, x_fin], [y_depart, y_imp, y_fin], color='red', alpha=0.3)

plt.gca().set_aspect('equal', adjustable='box')
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.title("Optique géométrique : Rayons et Phase S")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
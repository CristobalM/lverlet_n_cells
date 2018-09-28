from params import Params
from particle_interaction import WCAParticleInteraction
from simulation import Simulation
from wall import WallA
import matplotlib.pyplot as plt

import numpy as np

sim_steps = 10
epsilon = 1
sigma = 1

xmin = 0.0
xmax = 1000.0
ymin = 0.0
ymax = 1000.0

interaction = WCAParticleInteraction(epsilon, sigma)
wall = WallA(xmin, xmax, ymin, ymax)

X_u = np.linspace(xmin +0.1, xmax-0.1, 100)
Y_u = np.linspace(ymin +0.1, ymax-0.1, 100)
XX, YY= np.meshgrid(X_u, Y_u)

pts = np.vstack([XX.ravel(), YY.ravel()])
pts3 = np.column_stack([XX.ravel(), YY.ravel()])
print("Numero de particulas = %d" % len(pts3))


rc = interaction.get_rc()
lambd = 0.2
rv = (1+lambd)*rc
v0 = 10000
mu = 1
deltat = 0.1
diffcoef = 1


params = Params(rc=rc, rv=rv, v0=v0, mu=mu, deltat=deltat, DiffCoef=diffcoef)

sim = Simulation(sim_steps, interaction, wall, pts3, params)
grid_rows = sim.particle_handlers.grid.rows
grid_cols = sim.particle_handlers.grid.cols
results = sim.run()

print("Tiempo\t\t\t\t\t\t\t\t\tsegundos")
print("Total limpiar grilla\t\t\t\t\t%.5f" % sim.acc_ctime)
if sim.c_ctime > 0:
    print("Promedio limpiar grilla\t\t\t\t\t%.5f" % float(sim.acc_ctime/sim.c_ctime))
print("Total asignar en grilla\t\t\t\t\t%.5f" % sim.acc_asstime)
if sim.c_asstime > 0:
    print("Promedio asignar en grilla\t\t\t\t%.5f" % float(sim.acc_asstime/sim.c_asstime))
print("Total crear verlet\t\t\t\t\t\t%.5f" % sim.acc_vtime)
if sim.c_vtime > 0:
    print("Promedio crear verlet\t\t\t\t\t%.5f" % float(sim.acc_vtime/sim.c_vtime))
print("Total ejecucion\t\t\t\t\t\t\t%.5f" % sim.total_time)
print("Numero de celdas: %d" % (grid_rows*grid_cols))


Xr, Yr = zip(*results)
plt.figure(figsize=(15, 15))
plt.scatter(Xr, Yr)
plt.axvline(x=xmin, c='r')
plt.axvline(x=xmax, c='r')
plt.axhline(y=ymin, c='r')
plt.axhline(y=ymax, c='r')
plt.show()

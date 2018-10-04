import matplotlib.pyplot as plt
import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
from src.wall import WallA, WallPeriodicBC

sim_steps = 100
epsilon = 1
sigma = 1

xmin = 0.0
xmax = 1000.0
ymin = 0.0
ymax = 1000.0

interaction = WCAParticleInteraction(epsilon, sigma)
wall = WallA(xmin, xmax, ymin, ymax)
#wall = WallPeriodicBC(xmin, xmax, ymin, ymax)

#X_u = np.linspace(xmin +0.1, xmax-0.1, 10)
#Y_u = np.linspace(ymin +0.1, ymax-0.1, 10)

#X_u = [np.random.random()*(xmax-xmin) + xmin for _ in range(2)]
#Y_u = [np.random.random()*(ymax-ymin) + ymin for _ in range(1)]
X_u = np.linspace(xmin +0.1, xmax-0.1, 100)
Y_u = np.linspace(ymin +0.1, ymax-0.1, 100)
XX, YY= np.meshgrid(X_u, Y_u)

pts = np.vstack([XX.ravel(), YY.ravel()])
pts3 = np.column_stack([XX.ravel(), YY.ravel()])
print("Numero de particulas = %d" % len(pts3))


rc = interaction.get_rc()
lambd = 0.2
rv = (1+lambd)*rc
v0 = 1
mu = 1
deltat = 0.1
diffcoef = 1


params = Params(rc=rc, rv=rv, v0=v0, mu=mu, deltat=deltat, diffcoef=diffcoef, epsilon=epsilon, sigma=sigma)

sim = Simulation(sim_steps, interaction, wall, pts3, params)
grid_rows = sim.particle_handlers.grid.rows
grid_cols = sim.particle_handlers.grid.cols
results = []
cnt = 0
for result in sim.run_gen():
    Xr, Yr = zip(*result)
    cnt += 1
    results.append([Xr, Yr])
    if cnt % 10 == 0:
        print("%d/%d" % (cnt, sim_steps))

print("Verlet changes: %d" % sim.verlet_changes)

pause_step = 1.0/30.0#0.05
plt.figure(figsize=(15, 15))
for i, result in enumerate(results):
    #plt.gcf().clear()
    for artist in plt.gca().lines + plt.gca().collections:
        artist.remove()
    [Xr, Yr] = result
    plt.scatter(Xr, Yr, c='b')
    plt.axvline(x=xmin, c='r')
    plt.axvline(x=xmax, c='r')
    plt.axhline(y=ymin, c='r')
    plt.axhline(y=ymax, c='r')
    plt.xticks(np.arange(xmin, xmax+xmax*.1, xmax/10))
    plt.yticks(np.arange(ymin, ymax+ymax*.1, ymax/10))

    plt.gcf().canvas.draw()
    plt.gcf().canvas.flush_events()
    plt.pause(pause_step)

plt.show()
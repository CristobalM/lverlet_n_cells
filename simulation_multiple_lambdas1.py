import matplotlib.pyplot as plt
import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
from src.wall import WallA

sim_steps = 10
epsilon = 1
sigma = 1

xmin = 0.0
xmax = 1000.0
ymin = 0.0
ymax = 1000.0

interaction = WCAParticleInteraction(epsilon, sigma)
wall = WallA(xmin, xmax, ymin, ymax)

X_u = np.linspace(xmin +0.1, xmax-0.1, 10)
Y_u = np.linspace(ymin +0.1, ymax-0.1, 10)
XX, YY= np.meshgrid(X_u, Y_u)

pts = np.vstack([XX.ravel(), YY.ravel()])
init_positions = np.column_stack([XX.ravel(), YY.ravel()])
particles_num = len(init_positions)
print("Numero de particulas = %d" % particles_num)


rc = interaction.get_rc()
v0 = 10000
mu = 1
deltat = 0.1
diffcoef = 1

max_lambda = min(xmax, ymax)/rc - 1
the_lambdas = np.linspace(0, max_lambda, 500)
times = []
for lambd in the_lambdas:
    #lambd = 0.2
    rv = (1+lambd)*rc
    params = Params(rc=rc, rv=rv, v0=v0, mu=mu, deltat=deltat, diffcoef=diffcoef, epsilon=epsilon, sigma=sigma)

    sim = Simulation(sim_steps, interaction, wall, init_positions, params)
    grid_rows = sim.particle_handlers.grid.rows
    grid_cols = sim.particle_handlers.grid.cols
    results = sim.run()
    times.append(sim.total_time)

times = np.array(times)
both = np.array([the_lambdas, times])
np.save('saved_performance_time_lambdas_%d_%d_%.3f.npy' % (sim_steps, particles_num, max_lambda), both)
plt.plot(the_lambdas, times)
plt.xlabel("Lambda")
plt.ylabel("Tiempo")
plt.xticks(np.arange(0.0, max_lambda + 0.05, max_lambda/12.0))
plt.title("Numero de iteraciones: %d, Numero de particulas: %d" % (sim_steps, particles_num))
plt.show()

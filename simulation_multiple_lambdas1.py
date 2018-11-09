import matplotlib.pyplot as plt
import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
from src.wall import WallA, WallPeriodicBC

import progressbar
import os

#sim_steps = 5000
total_phys_time = 10
epsilon = 0.5
sigma = 1


#lambd = 0.2
v0 = 1
mu = 1
#deltat = 0.005
deltat = 0.01
#deltat = 0.1
diffcoef = 1

all_interactions = False

interaction = WCAParticleInteraction(epsilon, sigma)
rc = interaction.get_rc()
print("RC is = %.3f" % rc)
#rv = (1+lambd)*rc

#wall = WallA(xmin, xmax, ymin, ymax)

particles_x = 32
particles_y = 32
particles_num = particles_x * particles_y

xmin = 0.0
#xmax = 100.0
ymin = 0.0
#ymax = 100.0
"""
X_u = np.linspace(xmin + 0.1, xmax - 0.1, particles_x)
Y_u = np.linspace(ymin + 0.1, ymax - 0.1, particles_y)
XX, YY = np.meshgrid(X_u, Y_u)
init_positions = np.column_stack([XX.ravel(), YY.ravel()])
"""
#particles_num = len(init_positions)
print("Numero de particulas = %d" % particles_num)

max_lambda = 0.3

experiment = 2

wall_to_use = WallPeriodicBC

saved_fname = "saved_performance_time_lambdas_maxlambdas%.2f_%.3fphystime_%s_%.2f_eps%.4f_v0_%.2f_t_%.3f_allints=%s_particlesnum%d_exp%d.npy" %\
              (max_lambda, total_phys_time, wall_to_use.name(), sigma, epsilon, v0, deltat, str(all_interactions), particles_num, experiment)

etas = [0.1, 0.4, 0.6]
if os.path.isfile(saved_fname):
    both = np.load(saved_fname)
    the_lambdas = both[0]
    times_etas = both[1]
else:
    the_lambdas = np.linspace(0.04, max_lambda, 50)

    times_etas = []
    for eta in etas:
        times = []
        #with progressbar.ProgressBar(max_value=len(the_lambdas)) as bar:

        L = np.sqrt(particles_num/eta)
        xmax = L
        ymax = L

        print("L = %.3f, eta = %.1f" % (L, eta))

        X_u = np.linspace(xmin + rc, xmax - rc, particles_x)
        Y_u = np.linspace(ymin + rc, ymax - rc, particles_y)
        XX, YY = np.meshgrid(X_u, Y_u)
        init_positions = np.column_stack([XX.ravel(), YY.ravel()])
        wall = wall_to_use(xmin, xmax, ymin, ymax)
        for n, lambd in enumerate(the_lambdas):
            #lambd = 0.2
            rv = (1+lambd)*rc
            params = Params(rc=rc, rv=rv, v0=v0, mu=mu, deltat=deltat, diffcoef=diffcoef, epsilon=epsilon, sigma=sigma)

            sim = Simulation(total_phys_time, interaction, wall, init_positions, params)
            grid_rows = sim.particle_handlers.grid.rows
            grid_cols = sim.particle_handlers.grid.cols
            results = sim.run()
            times.append(sim.total_phys_time)
            #bar.update(n)

        times = np.array(times)
        times_etas.append(times)
    both = np.array([the_lambdas, times_etas])
    np.save(saved_fname, both)

colors = ['red', 'green', 'blue']
handles = []
for k, times in enumerate(times_etas):
    l,  = plt.plot(the_lambdas, times, c=colors[k], label="eta = %.1f" % etas[k] )
    handles.append(l)
plt.legend(handles=handles)
plt.xlabel("Lambda")
plt.ylabel("Tiempo")
#plt.xticks(np.arange(0.0, max_lambda + 0.05, max_lambda/12.0))
plt.title("Tiempo fisico: %d, Numero de particulas: %d" % (total_phys_time, particles_num))
plt.show()

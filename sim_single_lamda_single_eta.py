import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
from src.wall import WallA, WallPeriodicBC

import os
import sys

assert len(sys.argv) >= 3

lambd = float(sys.argv[1])
eta = float(sys.argv[2])

total_phys_time = 100
epsilon = 0.5
sigma = 1

v0 = 1
mu = 1
deltat = 0.01
diffcoef = 1

all_interactions = False
interaction = WCAParticleInteraction(epsilon, sigma)
rc = interaction.get_rc()

particles_x = 32
particles_y = 32
particles_num = particles_x * particles_y

xmin = 0.0
#xmax = 100.0
ymin = 0.0
#ymax = 100.0


wall_to_use = WallPeriodicBC

L = np.sqrt(particles_num/eta)
xmax = L
ymax = L


params_tuple = [lambd, eta, total_phys_time, wall_to_use.name(), sigma, epsilon, v0, deltat, all_interactions, particles_num]
params_tuple_str = []
for x in params_tuple:
    if type(x) == float:
        params_tuple_str.append("%.4f" % x)
    else:
        params_tuple_str.append(str(x))

fname = 'result_' + '_'.join(params_tuple_str) + '_.txt'

X_u = np.linspace(xmin + rc, xmax - rc, particles_x)
Y_u = np.linspace(ymin + rc, ymax - rc, particles_y)
XX, YY = np.meshgrid(X_u, Y_u)
init_positions = np.column_stack([XX.ravel(), YY.ravel()])
wall = wall_to_use(xmin, xmax, ymin, ymax)

rv = (1+lambd)*rc
params = Params(rc=rc, rv=rv, v0=v0, mu=mu, deltat=deltat, diffcoef=diffcoef, epsilon=epsilon, sigma=sigma)

sim = Simulation(total_phys_time, interaction, wall, init_positions, params)
grid_rows = sim.particle_handlers.grid.rows
grid_cols = sim.particle_handlers.grid.cols
results = sim.run()
sim_time = sim.total_run_time

with open(fname, 'w') as f:
    f.write(sim_time)

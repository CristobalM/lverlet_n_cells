import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
from src.wall import WallA, WallPeriodicBC

import os
import sys
import pickle

assert len(sys.argv) >= 3

lambd = float(sys.argv[1])
eta = float(sys.argv[2])
save_results = True if len(sys.argv) >= 4 and int(sys.argv[3]) > 0 else False

total_phys_time = 500
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
xmax = L + 10*rc
ymax = L + 10*rc


params_tuple = [lambd, eta, total_phys_time, wall_to_use.name(), sigma, epsilon, v0, deltat, all_interactions, particles_num]
params_tuple_str = []
for x in params_tuple:
    if type(x) == float:
        params_tuple_str.append("%.4f" % x)
    else:
        params_tuple_str.append(str(x))

fname = 'result_' + '_'.join(params_tuple_str) + '_.txt'

X_u = np.linspace(xmin + rc*2.0, xmax - rc*2.0, particles_x)
Y_u = np.linspace(ymin + rc*2.0, ymax - rc*2.0, particles_y)
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
    f.write(str(sim_time))


if save_results:
    pkfile = fname + '_positions.pkl'
    with open(pkfile, 'wb') as f:
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

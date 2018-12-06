import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
from src.wall import WallA, WallPeriodicBC

import os
import sys
import pickle

assert len(sys.argv) >= 5

lambd = float(sys.argv[1])
eta = float(sys.argv[2])
file_init = sys.argv[3]
total_phys_time = float(sys.argv[4])
save_results = True if len(sys.argv) >= 6 and int(sys.argv[5]) > 0 else False

#total_phys_time = 1
epsilon = 0.5
sigma = 1

v0 = 1
mu = 1
deltat = 0.01
diffcoef = 1

all_interactions = False
interaction = WCAParticleInteraction(epsilon, sigma)
rc = interaction.get_rc()


xmin = 0.0
#xmax = 100.0
ymin = 0.0
#ymax = 100.0


wall_to_use = WallPeriodicBC

with open(file_init, 'rb') as f:
    init_positions = pickle.load(f)

particles_num = len(init_positions)

L = np.sqrt(particles_num/eta)
xmax = L + 10*rc
ymax = L + 10*rc

print("L = %.3f" % L)


params_tuple = [lambd, eta, total_phys_time, wall_to_use.name(), sigma, epsilon, v0, deltat, all_interactions, particles_num]
params_tuple_str = []
for x in params_tuple:
    if type(x) == float:
        params_tuple_str.append("%.4f" % x)
    else:
        params_tuple_str.append(str(x))

fname = 'result_' + '_'.join(params_tuple_str) + '_.txt'

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

import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
from src.videotool import VideoTool
from src.wall import WallA, WallPeriodicBC

sim_steps = 3000
epsilon = 0.5
sigma = 1

xmin = 0.0
xmax = 5.0
ymin = 0.0
ymax = 5.0

lambd = 0.2
v0 = 1
mu = 1
#deltat = 0.005
deltat = 0.01
diffcoef = 1

all_interactions = False

interaction = WCAParticleInteraction(epsilon, sigma)
rc = interaction.get_rc()
rv = (1+lambd)*rc

wall = WallA(xmin, xmax, ymin, ymax)
#wall = WallPeriodicBC(xmin, xmax, ymin, ymax)

#X_u = np.linspace(xmin +2*rc, xmax-2*rc, 5)
X_u = np.linspace(xmin +0.1, xmax-0.1, 3)
#Y_u = np.linspace(ymin +2*rc, ymax-2*rc, 5)
Y_u = np.linspace(ymin +0.1, ymax-0.1, 3)
XX, YY= np.meshgrid(X_u, Y_u)

pts = np.vstack([XX.ravel(), YY.ravel()])
pts3 = np.column_stack([XX.ravel(), YY.ravel()])
print("Numero de particulas = %d" % len(pts3))


params = Params(rc=rc, rv=rv, v0=v0, mu=mu, deltat=deltat, diffcoef=diffcoef, epsilon=epsilon, sigma=sigma)

sim = Simulation(sim_steps, interaction, wall, pts3, params, all_interactions=all_interactions)

xsize = 1024
ysize = 768

margin = 50

results = []
angles_all = []
for result, angles in sim.run_gen():
    results.append(np.copy(result))
    angles_all.append(np.copy(angles))

VideoTool.generate_video(results,
                         "output_%dsteps_%.1fx%.1f_%s_%.2f_eps%.4f_v0_%.2f_t_%.3f_allints=%s.avi" %
                         (sim_steps, xmax, ymax, wall.name(), sigma, epsilon, v0, deltat, str(all_interactions)),
                         xsize, ysize, xmax - xmin, ymax - ymin, margin=50, rc=rc, all_sim_angles=angles_all)
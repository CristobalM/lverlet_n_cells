import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
from src.videotool import VideoTool
from src.wall import WallA, WallPeriodicBC

sim_steps = 10000
epsilon = 1
sigma = 1

xmin = 0.0
xmax = 40.0
ymin = 0.0
ymax = 40.0

interaction = WCAParticleInteraction(epsilon, sigma)
wall = WallPeriodicBC(xmin, xmax, ymin, ymax)

X_u = np.linspace(xmin +0.1, xmax-0.1, 10)
Y_u = np.linspace(ymin +0.1, ymax-0.1, 10)
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
results = []

xsize = 1024
ysize = 768

margin = 50

results = []
for result in sim.run_gen():
    results.append(np.copy(result))

VideoTool.generate_video(results, "output6.avi", xsize, ysize, xmax - xmin, ymax - ymin, margin=50, rc=rc)

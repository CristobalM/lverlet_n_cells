import matplotlib.pyplot as plt
import numpy as np

from src.params import Params
from src.particle_interaction import WCAParticleInteraction
from src.simulation import Simulation
#from src.videotool import VideoTool
from src.videotool import VideoTool
from src.wall import WallA, WallPeriodicBC
import cv2

sim_steps = 2000
epsilon = 1
sigma = 1

xmin = 0.0
xmax = 50.0
ymin = 0.0
ymax = 50.0

interaction = WCAParticleInteraction(epsilon, sigma)
wall = WallA(xmin, xmax, ymin, ymax)
#wall = WallPeriodicBC(xmin, xmax, ymin, ymax)

#X_u = np.linspace(xmin +0.1, xmax-0.1, 10)
#Y_u = np.linspace(ymin +0.1, ymax-0.1, 10)

#X_u = [np.random.random()*(xmax-xmin) + xmin for _ in range(2)]
#Y_u = [np.random.random()*(ymax-ymin) + ymin for _ in range(1)]
X_u = np.linspace(xmin +0.1, xmax-0.1, 10)
Y_u = np.linspace(ymin +0.1, ymax-0.1, 1)
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
step_pxel = 1
xsize = 1024
ysize = 768

margin = 50


windows = []
virtxsize = xsize - 2*margin
virtysize = ysize - 2*margin

mx = int(margin/(xmax-xmin))
my = int(margin/(ymax-ymin))

multj = virtxsize/(xmax-xmin)
multi = virtysize/(ymax-ymin)
rbor = int(rc*min(multj, multi))
visual_radius = 2
video_tool = VideoTool("outputok.avi", xsize, ysize, xmax - xmin, ymax - ymin, margin=margin)
for result in sim.run_gen():
    window = video_tool.start_window()
    cnt += 1
    for x,y in result:
        video_tool.add_circle(x, y, visual_radius, visual_radius*2)
        video_tool.add_circle(x, y, rbor, 0, c=(0, 255, 0, 100))

    if cnt % 100 == 0:
        print("%d/%d" % (cnt, sim_steps))

video_tool.create_video()
print("Verlet changes: %d" % sim.verlet_changes)

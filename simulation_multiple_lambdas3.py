import matplotlib.pyplot as plt
import numpy as np


from src.experiment import MultipleLambdaExperiment
from src.params import Params, SimulationParams
from src.wall import WallPeriodicBC

xmin = 0.0
xmax = 1000.0
ymin = 0.0
ymax = 1000.0

sim_steps = 100
max_lambda = 2.0

X_u = np.linspace(xmin +0.1, xmax-0.1, 10)
Y_u = np.linspace(ymin +0.1, ymax-0.1, 10)
XX, YY= np.meshgrid(X_u, Y_u)

pts = np.vstack([XX.ravel(), YY.ravel()])
init_positions = np.column_stack([XX.ravel(), YY.ravel()])
particles_num = len(init_positions)

params = Params(rc=None, rv=None, v0=1, mu=1, deltat=0.01, diffcoef=1, epsilon=1, sigma=1)
simulation_params = SimulationParams(init_positions, params, simulation_steps=sim_steps, wall=WallPeriodicBC(xmin, xmax, ymin, ymax))
multiple_lambda_experiment = MultipleLambdaExperiment(simulation_params, max_lambda=max_lambda, lambda_samples=20)

lambdas, times = multiple_lambda_experiment.run_experiment()

plt.plot(lambdas, times)
plt.xlabel("Lambda")
plt.ylabel("Tiempo")
plt.xticks(np.arange(0.0, max_lambda + 0.05, max_lambda / 12.0))
plt.title("Numero de iteraciones: %d, Numero de particulas: %d" % (sim_steps, particles_num))
plt.show()
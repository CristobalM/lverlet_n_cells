from abc import abstractmethod

import numpy as np

from src.params import Params
from src.simulation import Simulation


class Experiment:
    def __init__(self, simulation_params):
        self.simulation_params = simulation_params

    @abstractmethod
    def run_experiment(self):
        pass


class MultipleLambdaExperiment(Experiment):
    def __init__(self, simulation_params, max_lambda=None, lambda_samples=500):
        super().__init__(simulation_params)
        self.max_lambda = max_lambda
        self.lambda_samples = lambda_samples

    def run_experiment(self):
        xmax = self.simulation_params.wall.get_xmax()
        ymax = self.simulation_params.wall.get_ymax()
        rc = self.simulation_params.interaction.get_rc()
        v0 = self.simulation_params.params.v0
        mu = self.simulation_params.params.mu
        deltat = self.simulation_params.params.deltat
        diffcoef = self.simulation_params.params.diffcoef
        sim_steps = self.simulation_params.simulation_steps
        interaction = self.simulation_params.interaction
        wall = self.simulation_params.wall
        init_positions = self.simulation_params.init_positions
        epsilon = self.simulation_params.params.epsilon
        sigma = self.simulation_params.params.sigma

        max_lambda = self.max_lambda if self.max_lambda is not None else min(xmax, ymax) / rc - 1
        the_lambdas = np.linspace(0, max_lambda, self.lambda_samples)
        times = []
        for lambd in the_lambdas:
            rv = (1 + lambd) * rc
            params = Params(rc=rc, rv=rv, v0=v0, mu=mu, deltat=deltat, diffcoef=diffcoef, epsilon=epsilon, sigma=sigma)

            sim = Simulation(sim_steps, interaction, wall, init_positions, params)
            sim.run()
            times.append(sim.total_time)

        return the_lambdas, np.array(times)
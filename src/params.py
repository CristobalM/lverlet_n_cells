from src.particle_interaction import WCAParticleInteraction
from src.wall import WallA


class Params:
    def __init__(self, rc, rv, v0, mu, deltat, diffcoef, epsilon, sigma):
        self.rc = rc
        self.rv = rv
        self.v0 = v0
        self.mu = mu
        self.deltat = deltat
        self.diffcoef =diffcoef
        self.epsilon = epsilon
        self.sigma = sigma


def find_bbox(positions):
    max_x = positions[0][0]
    min_x = positions[0][0]
    max_y = positions[0][1]
    min_y = positions[0][1]
    for x,y  in positions:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y

    return min_x, min_y, max_x, max_y


class SimulationParams:
    def __init__(self, init_positions, params, simulation_steps=10, wall=None, interaction=None):
        self.init_positions = init_positions
        self.params = params
        self.simulation_steps = simulation_steps
        self.wall = wall
        self.interaction = interaction

        if wall is None:
            min_x, min_y, max_x, max_y = find_bbox(init_positions)
            we = (max_x - min_x)/100
            he = (max_y - min_y)/100
            self.wall = WallA(min_x - we, max_x + we, min_y - he, max_y + he)

        if interaction is None:
            self.interaction = WCAParticleInteraction(params.epsilon, params.sigma)
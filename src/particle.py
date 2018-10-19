import time

import scipy.linalg as splalg

from src.grid import Grid


class ParticleHandler:
    def __init__(self, idx, particles_positions, wall, grid, params):
        self.idx = idx
        self.neighbors_list = []
        self.positions = particles_positions
        self.wall = wall
        self.grid = grid
        self.params = params
        self.the_particle_interaction_values = {}

    def get_idx(self):
        return self.idx

    def create_verlet_list(self):
        my_pos = self.positions[self.idx]
        nbors_in_cells = self.grid.get_all_nbors_cells(my_pos)
        self.neighbors_list = []
        for nbor_idx in nbors_in_cells:
            if nbor_idx == self.idx:
                continue
            nbor_pos = self.positions[nbor_idx]
            _, dist = self.wall.pairwise_dist(nbor_pos, my_pos)
            if dist < self.params.rv:
                self.neighbors_list.append(nbor_idx)

    def get_nbors_idxs(self):
        return self.neighbors_list


class ParticleHandlers:
    def __init__(self, particles_positions, params, wall):
        self.wall = wall
        self.params = params
        self.particles_positions = particles_positions

        self.handlers = []
        self.grid = Grid(self.wall, self.params.rv)

    def create_handlers(self):
        for k, position in enumerate(self.particles_positions):
            self.add_handler(ParticleHandler(k, self.particles_positions, self.wall, self.grid, self.params))

        self.create_grid()
        self.calc_verlet_lists()

    def add_handler(self, handler):
        self.handlers.append(handler)

    def create_grid(self):
        ctime = time.time()
        self.grid.clear()
        ctime = time.time() - ctime
        asstime = time.time()
        for handler in self.handlers:
            idx = handler.get_idx()
            position = self.particles_positions[idx]
            self.grid.add_to_grid(idx, position)

        asstime = time.time() - asstime
        return ctime, asstime

    def get_handler(self, idx):
        return self.handlers[idx]

    def calc_verlet_lists(self):
        start_time = time.time()
        for handler in self.handlers:
            handler.create_verlet_list()

        total_time = time.time() - start_time
        return total_time

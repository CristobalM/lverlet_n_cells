import time

import numpy as np
import scipy.linalg as splalg

from src.particle import ParticleHandlers


class Simulation:
    def __init__(self, sim_steps, interactions, wall, init_positions, params, seed=12345):
        self.sim_steps = sim_steps
        self.interactions = interactions
        self.wall = wall
        self.positions = init_positions
        self.positions_verlet_snapshot = np.copy(self.positions)
        self.seed = seed
        self.params = params

        self.particle_handlers = ParticleHandlers(init_positions, params, wall)

        self.sim_results = None
        self.last_angle = None

        self.acc_ctime = 0.0
        self.acc_asstime = 0.0
        self.acc_vtime = 0.0
        self.acc_interaction_time = 0.0
        self.acc_calc_step_time = 0.0
        self.c_ctime = 0
        self.c_asstime = 0
        self.c_vtime = 0

        self.total_time = 0

        self.last_angle = np.zeros(len(init_positions), dtype=np.float32)
        self.verlet_changes = 0

    def run(self):
        tottime = time.time()
        self.init_configs()
        for _ in range(self.sim_steps):
            self.run_step()

        self.sim_results = self.positions
        self.total_time = time.time() - tottime
        return self.sim_results

    def run_gen(self):
        tottime = time.time()
        self.init_configs()
        for _ in range(self.sim_steps):
            self.run_step()
            yield self.positions

        self.sim_results = self.positions
        self.total_time = time.time() - tottime
        return self.sim_results

    def init_configs(self):
        self.particle_handlers.create_handlers()

        np.random.seed(self.seed)
        self.last_angle = np.array([np.random.random() * 2 * np.pi for _ in range(len(self.positions))])

    def run_step(self):
        int_time = time.time()
        interactions_result = self.calc_interactions()
        self.acc_interaction_time += time.time() - int_time
        max_dist = 0
        init_step_time = time.time()
        for k in range(len(self.positions)):
            next_pos = self.next_position(k, interactions_result)
            _, dist_moved = self.wall.pairwise_dist(self.positions_verlet_snapshot[k], next_pos)  #  splalg.norm(self.positions_verlet_snapshot[k] - next_pos)
            if dist_moved > max_dist:
                max_dist = dist_moved
            self.positions[k] = self.wall.next_pos(next_pos[0], next_pos[1])

        self.acc_calc_step_time += time.time() - init_step_time

        ctime, asstime = self.particle_handlers.create_grid()
        self.acc_ctime += ctime
        self.c_ctime += 1
        self.acc_asstime += asstime
        self.c_asstime += 1
        if max_dist > self.params.rv - self.params.rc:
            self.positions_verlet_snapshot = np.copy(self.positions)
            vtime = self.particle_handlers.calc_verlet_lists()
            self.acc_vtime += vtime
            self.c_vtime += 1
            self.verlet_changes += 1

    def calc_interactions(self):
        interactions_result = []
        for k in range(len(self.positions)):
            k_interaction = self.get_particle_interaction(k)
            interactions_result.append(k_interaction)

        return interactions_result

    def next_position(self, k, interactions_result):
        last_position = self.positions[k]
        v0 = self.params.v0
        delta_t = self.params.deltat
        direction = self.get_particle_direction(k)
        mu = self.params.mu
        next_pos = last_position + v0*delta_t*direction + mu*delta_t*interactions_result[k]
        return next_pos

    def get_particle_interaction(self, k):
        mypos = self.positions[k]

        handler = self.particle_handlers.get_handler(k)
        nbors_idxs = handler.get_nbors_idxs()
        Fk = np.zeros(2, dtype=float)
        for nb_idx in nbors_idxs:
            nb_pos = self.positions[nb_idx]
            diff_vec, dist = self.wall.pairwise_dist(mypos, nb_pos)
            Fk += self.interactions.eval(dist)*(diff_vec/dist)

        return Fk

    def get_particle_direction(self, k):
        next_angle = self.last_angle[k] + np.sqrt(2*self.params.diffcoef*self.params.deltat) * np.random.normal()
        self.last_angle[k] = next_angle
        return np.array([np.cos(next_angle), np.sin(next_angle)])

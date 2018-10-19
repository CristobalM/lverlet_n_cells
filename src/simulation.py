import time

import numpy as np
import scipy.linalg as splalg

from src.particle import ParticleHandlers
import progressbar


class Simulation:
    def __init__(self, sim_steps, interactions, wall, init_positions, params, seed=12345, all_interactions=False,
                 save_interactions_idxs=False, save_point_to_point=False):
        self.sim_steps = sim_steps
        self.interactions = interactions
        self.wall = wall
        self.positions = init_positions
        self.positions_verlet_snapshot = np.copy(self.positions)
        self.seed = seed
        self.params = params
        self.all_interactions = all_interactions
        self.save_interactions_idxs = save_interactions_idxs
        self.save_point_to_point = save_point_to_point

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
        self.measure_threshold = self.sim_steps/100
        self.last_interactions = None

    def run(self, show_bar=True):
        tottime = 0
        self.init_configs()
        with progressbar.ProgressBar(max_value=self.sim_steps) as bar:
            for n in range(self.sim_steps):
                if n > self.measure_threshold:
                    t0 = time.time()
                self.run_step()
                if n > self.measure_threshold:
                    tottime += time.time() - t0

                bar.update(n)

        self.sim_results = self.positions
        self.total_time = tottime
        return self.sim_results

    def run_gen(self):
        tottime = 0
        self.init_configs()
        with progressbar.ProgressBar(max_value=self.sim_steps) as bar:
            for n in range(self.sim_steps):
                if n > self.measure_threshold:
                    t0 = time.time()
                self.run_step()
                if n > self.measure_threshold:
                    tottime += time.time() - t0
                bar.update(n)

                yield self.positions, self.last_angle, self.last_interactions

        self.sim_results = self.positions
        self.total_time = tottime
        return self.sim_results, self.last_angle, self.last_interactions

    def init_configs(self):
        self.particle_handlers.create_handlers()

        np.random.seed(self.seed)
        self.last_angle = np.array([np.random.random() * 2 * np.pi for _ in range(len(self.positions))])

    def get_interactions_idx(self, interactions_values):
        result = []
        for k in range(len(self.positions)):
            handler = self.particle_handlers.get_handler(k)
            to_add = []
            nbors_idxs = handler.get_nbors_idxs()
            #result.append(nbors_idxs)
            for nbor in nbors_idxs:
                to_add.append((nbor, handler.the_particle_interaction_values.get(nbor)))
            result.append(to_add)
        self.last_interactions = result
        return result

    def run_step(self):
        int_time = time.time()
        interactions_result = self.calc_interactions()

        if self.save_interactions_idxs:
            self.get_interactions_idx(interactions_result)

        self.acc_interaction_time += time.time() - int_time
        max_dist = 0
        init_step_time = time.time()
        for k in range(len(self.positions)):
            next_pos = self.next_position(k, interactions_result)
            next_pos = self.wall.next_pos(next_pos[0], next_pos[1])
            self.positions[k] = next_pos
            _, dist_moved = self.wall.pairwise_dist(self.positions_verlet_snapshot[k], next_pos)  #  splalg.norm(self.positions_verlet_snapshot[k] - next_pos)
            if dist_moved > max_dist:
                max_dist = dist_moved

            # Antes se hacia la actualizacion aca...

        self.acc_calc_step_time += time.time() - init_step_time

        ctime, asstime = self.particle_handlers.create_grid()
        self.acc_ctime += ctime
        self.c_ctime += 1
        self.acc_asstime += asstime
        self.c_asstime += 1
        if max_dist > (self.params.rv - self.params.rc)/10:
            self.positions_verlet_snapshot = np.copy(self.positions)
            vtime = self.particle_handlers.calc_verlet_lists()
            self.acc_vtime += vtime
            self.c_vtime += 1
            self.verlet_changes += 1

    def calc_interactions(self):
        interactions_result = []
        for k in range(len(self.positions)):
            k_interaction = self.get_particle_interaction(k, all_interactions=self.all_interactions,
                                                          save_point_to_point=self.save_point_to_point)
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

    def get_particle_interaction(self, k, all_interactions=False, save_point_to_point=False):
        mypos = self.positions[k]

        handler = self.particle_handlers.get_handler(k)
        nbors_idxs = handler.get_nbors_idxs()
        Fk = np.zeros(2, dtype=float)

        if all_interactions:
            comparing_to = range(len(handler.positions))
        else:
            comparing_to = nbors_idxs

        for nb_idx in comparing_to:
            if nb_idx == k:
                continue
            nb_pos = self.positions[nb_idx]
            diff_vec, dist = self.wall.pairwise_dist(mypos, nb_pos)
            if dist == 0:
                dist = 0.0000001

            this_force = (self.interactions.eval(dist) / dist) * diff_vec
            Fk += this_force
            if save_point_to_point:
                handler.the_particle_interaction_values[nb_idx] = this_force

        return Fk

    def get_particle_direction(self, k):
        next_angle = self.last_angle[k] + np.sqrt(2*self.params.diffcoef*self.params.deltat) * np.random.normal()
        self.last_angle[k] = next_angle
        return np.array([np.cos(next_angle), np.sin(next_angle)])

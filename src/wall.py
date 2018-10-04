from abc import abstractmethod
import numpy as np
import scipy.linalg as splalg


class Wall:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
    @abstractmethod
    def next_pos(self, x, y):
        pass

    def pairwise_dist(self, leftv, rightv):
        diff_vec = leftv - rightv
        dist = splalg.norm(diff_vec)
        return diff_vec, dist

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_ymax(self):
        return self.y_max

    def get_xmax(self):
        return self.x_max

    def get_ymin(self):
        return self.y_min

    def get_xmin(self):
        return self.x_min

    @abstractmethod
    def nbors_indexes(self, i, j, rows, cols):
        pass


class WallA(Wall):
    def next_pos(self, x, y):
        next_x = x
        next_y = y
        if x < self.x_min:
            next_x = self.x_min
        elif x > self.x_max:
            next_x = self.x_max

        if y < self.y_min:
            next_y = self.y_min
        elif y > self.y_max:
            next_y = self.y_max

        return next_x, next_y

    def nbors_indexes(self, i, j, rows, cols):
        return [(i, j), (i, j + 1), (i, j - 1),
                (i + 1, j), (i + 1, j + 1), (i + 1, j - 1),
                (i - 1, j), (i - 1, j + 1), (i - 1, j - 1)]


class WallPeriodicBC(Wall):
    def nbors_indexes(self, i, j, rows, cols):
        inext = (i+1)%rows
        iprev = (rows + i-1)%rows
        jnext = (j+1)%cols
        jprev = (cols + j - 1) % cols
        return[(i, j), (i, jnext), (i, jprev),
              (inext, j), (inext, jnext), (inext, jprev),
              (iprev, j), (iprev, jnext), (iprev, jprev)]

    def next_pos(self, x, y):
        next_x = (x + self.get_width()*(int(np.abs(x)/self.get_width())+1)) % self.get_width()
        next_y = (y + self.get_height()*(int(np.abs(y)/self.get_height())+1)) % self.get_height()
        return next_x, next_y

    def pairwise_dist(self, leftv, rightv):
        naive_delta_x = np.abs(leftv[0] - rightv[0])
        naive_delta_y = np.abs(leftv[1] - rightv[1])
        delta_x = naive_delta_x
        delta_y = naive_delta_y
        if naive_delta_x > self.get_width()/2:
            delta_x = self.get_width() - naive_delta_x

        if naive_delta_y > self.get_height()/2:
            delta_y = self.get_height() - naive_delta_y

        dist = np.sqrt(delta_x**2 + delta_y**2)
        diff_vec = (leftv - rightv)*(dist/np.sqrt(naive_delta_x**2 + naive_delta_y**2))
        return diff_vec, dist




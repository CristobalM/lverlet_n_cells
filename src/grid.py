import itertools


class Grid:
    def __init__(self, wall, rv):
        self.wall = wall
        self.rv = rv
        self.rows = int(wall.get_height() / rv)
        self.cols = int(wall.get_width() / rv)
        self.deltax = wall.get_width() / self.cols
        self.deltay = wall.get_height() / self.rows
        self.grid = None
        self.create_grid()

    def create_grid(self):
        self.grid = {}

    def get_size(self):
        total = 0
        for row in self.grid:
            total += len(self.grid[row])
        return total

    def get_i_j_from_pos(self, position):
        [x, y] = position
        j = int((x - self.wall.get_xmin()) / self.deltax)
        i = int((y - self.wall.get_ymin()) / self.deltay)
        return i, j

    def add_to_grid(self, idx, position):
        i, j = self.get_i_j_from_pos(position)
        if i not in self.grid:
            self.grid[i] = {}
        if j not in self.grid[i]:
            self.grid[i][j] = []
        self.grid[i][j].append(idx)

    def get_all_nbors_cells(self, position):
        i, j = self.get_i_j_from_pos(position)
        nbors_it = self.get_nbors_iterator(i, j)
        result = [nbor_idx for nbor_idx in nbors_it]
        return result

    def get_nbors_iterator(self, i, j):

        nbors = [get_if_exists(u, v, self.rows, self.cols, self.grid) for u, v in self.nbors_indexes(i, j)]
        nbors = [v for u in nbors if u is not None for v in u]
        return itertools.chain(nbors)

    def nbors_indexes(self, i, j):
        return self.wall.nbors_indexes(i, j, self.rows, self.cols)

    def clear(self):
        self.grid = {}


def get_if_exists(i, j, rows, cols, grid):
    if i < 0 or i >= rows:
        return None
    if j < 0 or j >= cols:
        return None

    ivec = grid.get(i, None)
    jvec = None
    if ivec is not None:
        jvec = ivec.get(j, None)

    return jvec
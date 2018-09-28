import itertools


class Grid:
    def __init__(self, wall, rv):
        self.wall = wall
        self.rv = rv
        self.rows = int(wall.getHeight() / rv)
        self.cols = int(wall.getWidth() / rv)
        self.deltax = wall.getWidth() / self.cols
        self.deltay = wall.getHeight() / self.rows
        self.grid = None
        self.create_grid()

    def create_grid(self):
        self.grid = {}
        #for _ in range(self.rows):
        #    row = []
        #    for _ in range(self.cols):
        #        row.append([])
        #   self.grid.append(row)

    def get_i_j_from_pos(self, position):
        [x, y] = position
        j = int((x-self.wall.getXMin())/self.deltax)
        i = int((y-self.wall.getYMin())/self.deltay)
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
        return [nbor_idx for nbor_idx in nbors_it]

    def get_nbors_iterator(self, i, j):
        nbors = [get_if_exists(u, v, self.grid) for u, v in self.nbors_indexes(i, j)]
        nbors = [u for u in nbors if u is not None]
        return itertools.chain(nbors)

    def nbors_indexes(self, i, j):
        return self.wall.nbors_indexes(i, j, self.rows, self.cols)

    def clear(self):
        self.grid = {}



def get_if_exists(i, j, grid):
    if i < len(grid) or i >= len(grid):
        return None
    if j < len(grid[i]) or j >= len(grid[i]):
        return None

    return grid[i][j]
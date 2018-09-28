from abc import abstractmethod


class Wall:
    @abstractmethod
    def next_pos(self, x, y):
        pass

    @abstractmethod
    def getHeight(self):
        pass

    @abstractmethod
    def getWidth(self):
        pass

    @abstractmethod
    def getXMin(self):
        pass

    @abstractmethod
    def getYMin(self):
        pass

    @abstractmethod
    def getXMax(self):
        pass

    @abstractmethod
    def getYMax(self):
        pass

    @abstractmethod
    def nbors_indexes(self, i, j, rows, cols):
        pass


class WallA(Wall):
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

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

    def getWidth(self):
        return self.x_max - self.x_min

    def getHeight(self):
        return self.y_max - self.y_min

    def getYMax(self):
        return self.y_max

    def getXMax(self):
        return self.x_max

    def getYMin(self):
        return self.y_min

    def getXMin(self):
        return self.x_min

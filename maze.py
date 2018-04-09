from random import shuffle


class Maze:
    def __init__(self, source, max_y, max_x):
        self.source = source
        self.height = max_y
        self.width = max_x


class MazeGenerator:
    def __init__(self, max_size):
        self.maxX = max_size[0]
        self.maxY = max_size[1]
        self.stack = [(0, 0)]
        self.maze_array = [[0] * (self.maxX * 2 - 1) for _ in range(self.maxY * 2 - 1)]

    def run(self):
        self.maze_array[0][0] = 1
        self._generate_stack()
        return Maze(self.maze_array, self.maxY * 2 - 1, self.maxX * 2 - 1)

    def _generate_stack(self, pos=(0, 0)):
        for next_coord in self._get_next(pos):
            if next_coord not in self.stack:
                self.stack.append(next_coord)
                self._carve(pos, next_coord)
                self._generate_stack(next_coord)

    def _get_next(self, pos):
        values = []

        if pos[0] - 1 > 0:
            values.append((pos[0] - 1, pos[1]))
        if pos[0] + 1 < self.maxX:
            values.append((pos[0] + 1, pos[1]))
        if pos[1] - 1 > 0:
            values.append((pos[0], pos[1] - 1))
        if pos[1] + 1 < self.maxY:
            values.append((pos[0], pos[1] + 1))

        shuffle(values)

        for item in values:
            yield item

    def _carve(self, a, b):
        x_dif, y_dif = b[0] - a[0], b[1] - a[1]
        self.maze_array[b[1] * 2][b[0] * 2] = 1
        self.maze_array[a[1] * 2 + y_dif][a[0] * 2 + x_dif] = 1


def generate():
    mg = MazeGenerator((20, 20))
    return mg.run()

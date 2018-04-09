import maze
from random import randint


class MazeGame:
    def __init__(self):
        self.score = 0
        self._maze = maze.generate()
        self._add_border()
        self._populate()
        self._maze.source[self._maze.height - 2][self._maze.width - 2] = 4
        self.position = [1, 1]
        self.fov = (7, 5)

    def _add_border(self):
        self._maze.source = [[0] * self._maze.width] + self._maze.source + [[0] * self._maze.width]
        self._maze.source = [[0] + x + [0] for x in self._maze.source]
        self._maze.height += 2
        self._maze.width += 2

    def _populate(self):
        for y in range(2, self._maze.height):
            for x in range(2, self._maze.width):
                if self._maze.source[y][x] == 1:
                    rand = randint(0, 60)
                    if rand == 43:
                        self._maze.source[y][y] = 2

    def get_window(self):
        fov_center = [self.position[0], self.position[1]]
        ps_pos = [self.fov[0] // 2, self.fov[1] // 2]

        if self.position[0] < self.fov[0] // 2:
            fov_center[0] = self.fov[0] // 2
            ps_pos[0] = self.position[0]
        if self.position[1] < self.fov[1] // 2:
            fov_center[1] = self.fov[1] // 2
            ps_pos[1] = self.position[1]
        if self.position[0] > self._maze.width - self.fov[0] // 2 - 1:
            fov_center[0] = self._maze.width - self.fov[0] // 2 - 1
            ps_pos[0] = self.fov[0] - (self._maze.width - self.position[0] + 1) + 1
        if self.position[1] > self._maze.height - self.fov[1] // 2 - 1:
            fov_center[1] = self._maze.height - self.fov[1] // 2 - 1
            ps_pos[1] = self.fov[1] - (self._maze.height - self.position[1] + 1) + 1

        grid = []
        for y in range(fov_center[1] - self.fov[1] // 2, fov_center[1] + self.fov[1] // 2 + 1):
            row = []
            for x in range(fov_center[0] - self.fov[0] // 2, fov_center[0] + self.fov[0] // 2 + 1):
                row.append(self._maze.source[y][x])
            grid.append(row)

        grid[ps_pos[1]][ps_pos[0]] = 3

        mappings = {
            0: '█',
            1: '░',
            2: '*',
            3: '♥',
            4: '∏'
        }

        view = []
        for row in grid:
            str_row = ''
            for item in row:
                str_row += mappings[item]
            view.append(str_row)
        return view

    def shift_x(self, amount):
        x_pos = self.position[0] + amount
        if 0 < x_pos < self._maze.width:
            if self._maze.source[self.position[1]][x_pos] != 0:
                self.position[0] = x_pos
        self._check_score()

    def shift_y(self, amount):
        y_pos = self.position[1] + amount
        if 0 < y_pos < self._maze.height:
            if self._maze.source[y_pos][self.position[0]] != 0:
                self.position[1] = y_pos
        self._check_score()

    def _check_score(self):
        if self._maze.source[self.position[1]][self.position[0]] == 2:
            self.score += 1
            self._maze.source[self.position[1]][self.position[0]] = 1

    def check_door(self):
        if self._maze.source[self.position[1]][self.position[0]] == 4:
            return True
        return False

class Cell:
    def __init__(self):
        self.walls = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        self.cost = None
        self.heuristic = None

    def set_walls(self, north, south, east, west):
        self.walls['N'] = north
        self.walls['S'] = south
        self.walls['E'] = east
        self.walls['W'] = west

    def set_cost(self, cost):
        self.cost = cost

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic
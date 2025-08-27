class Robo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.trajetoria = [(self.x, self.y)]
        self.pontos = 0
        self.colisoes = 0

    def move(self, direcao, obstaculos=None, grid_size=10):
        dx, dy = 0, 0
        if direcao == "N": dy = 1
        elif direcao == "S": dy = -1
        elif direcao == "E": dx = 1
        elif direcao == "W": dx = -1
        elif direcao == "NE": dx = 1; dy = 1
        elif direcao == "NW": dx = -1; dy = 1
        elif direcao == "SE": dx = 1; dy = -1
        elif direcao == "SW": dx = -1; dy = -1

        nx, ny = self.x + dx, self.y + dy
        if obstaculos and (nx, ny) in obstaculos:
            self.colisoes += 1
        elif 0 <= nx < grid_size and 0 <= ny < grid_size:
            self.x, self.y = nx, ny
            self.trajetoria.append((self.x, self.y))
            self.pontos += 1

    def reset(self):
        self.x, self.y = 0, 0
        self.trajetoria = [(self.x, self.y)]
        self.pontos = 0
        self.colisoes = 0


class Robo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direcao = 0  # 0=N,1=E,2=S,3=W
        self.trajetoria = [(self.x, self.y)]
        self.pontos = 0
        self.colisoes = 0

    def move_forward(self, obstaculos=None, grid_size=10):
        dx, dy = 0, 0
        if self.direcao == 0: dy = 1
        elif self.direcao == 1: dx = 1
        elif self.direcao == 2: dy = -1
        elif self.direcao == 3: dx = -1

        nx, ny = self.x + dx, self.y + dy
        # Checar colisões
        if obstaculos and (nx, ny) in obstaculos:
            self.colisoes += 1
        elif 0 <= nx < grid_size and 0 <= ny < grid_size:
            self.x, self.y = nx, ny
            self.trajetoria.append((self.x, self.y))
            self.pontos += 1

    def turn_left(self):
        self.direcao = (self.direcao - 1) % 4

    def turn_right(self):
        self.direcao = (self.direcao + 1) % 4

    def reset(self):
        self.x, self.y, self.direcao = 0, 0, 0
        self.trajetoria = [(self.x, self.y)]
        self.pontos = 0
        self.colisoes = 0

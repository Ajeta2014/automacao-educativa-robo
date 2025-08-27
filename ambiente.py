import matplotlib.pyplot as plt
import streamlit as st

class Ambiente:
    def __init__(self, grid_size=10, obstaculos=None, linha=None):
        self.grid_size = grid_size
        self.obstaculos = obstaculos or []
        self.linha = linha or []

    def desenha(self, robo):
        grid = [[0]*self.grid_size for _ in range(self.grid_size)]
        for ox, oy in self.obstaculos:
            grid[oy][ox] = 1

        plt.figure(figsize=(6,6))
        plt.imshow(grid, cmap="binary", origin="lower")

        # Linha
        if self.linha:
            lx, ly = zip(*self.linha)
            plt.plot(lx, ly, 'b--', lw=2, label="Linha")

        # Trajetória
        if len(robo.trajetoria) > 1:
            tx, ty = zip(*robo.trajetoria)
            plt.plot(tx, ty, 'orange', lw=2, label="Trajetória")

        # Robô
        plt.scatter(robo.x, robo.y, c="red", s=200, edgecolors="black", marker="o", label="Robô")
        dx, dy = 0, 0
        if robo.direcao == 0: dy=0.4
        elif robo.direcao == 1: dx=0.4
        elif robo.direcao == 2: dy=-0.4
        elif robo.direcao == 3: dx=-0.4
        plt.arrow(robo.x, robo.y, dx, dy, head_width=0.2, head_length=0.2, fc='red', ec='red')

        plt.title("Mini Laboratório de Robótica")
        plt.legend()
        st.pyplot(plt)

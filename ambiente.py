import matplotlib.pyplot as plt
import streamlit as st

class Ambiente:
    def __init__(self, grid_size=10, obstaculos=None, linha=None, metas=None):
        self.grid_size = grid_size
        self.obstaculos = obstaculos or []
        self.linha = linha or []
        self.metas = metas or []

    def desenha(self, robo):
        plt.figure(figsize=(6,6))
        grid = [[0]*self.grid_size for _ in range(self.grid_size)]

        # Obstáculos
        for ox, oy in self.obstaculos:
            plt.scatter(ox, oy, c="black", s=200, label="Obstáculo")

        # Metas
        for mx, my in self.metas:
            plt.scatter(mx, my, c="green", s=200, label="Meta")

        # Linha de percurso
        if self.linha:
            lx, ly = zip(*self.linha)
            plt.plot(lx, ly, 'b--', lw=2, label="Linha")

        # Trajetória do robô
        if len(robo.trajetoria) > 1:
            tx, ty = zip(*robo.trajetoria)
            plt.plot(tx, ty, 'orange', lw=2, label="Trajetória")

        # Robô ilustrado
        plt.scatter(robo.x, robo.y, c="red", s=300, edgecolors="black", marker="o", label="Robô")
        plt.title("Mini Laboratório de Robótica – Módulo Interativo")
        plt.xlim(-0.5, self.grid_size-0.5)
        plt.ylim(-0.5, self.grid_size-0.5)
        plt.grid(True)
        plt.legend()
        st.pyplot(plt)

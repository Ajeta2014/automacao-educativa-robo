import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Definição da classe Robô
class Robo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direcao = 0  # 0 = Norte, 1 = Leste, 2 = Sul, 3 = Oeste
    
    def move_forward(self):
        """Move o robô para frente baseado na direção atual"""
        if self.direcao == 0:  # Norte
            self.y += 1
        elif self.direcao == 1:  # Leste
            self.x += 1
        elif self.direcao == 2:  # Sul
            self.y -= 1
        elif self.direcao == 3:  # Oeste
            self.x -= 1
    
    def turn_left(self):
        """Faz o robô virar à esquerda"""
        self.direcao = (self.direcao - 1) % 4
    
    def turn_right(self):
        """Faz o robô virar à direita"""
        self.direcao = (self.direcao + 1) % 4

# Função para desenhar o ambiente
def desenha_ambiente(robo):
    ambiente = np.zeros((10, 10))  # Ambiente 10x10
    ambiente[4, 4] = 1  # Obstáculo
    ambiente[6, 6] = 1  # Obstáculo
    
    plt.clf()  # Limpa o gráfico anterior
    plt.imshow(ambiente, cmap="binary", origin="lower")
    
    # Marcando o robô no grid
    plt.scatter(robo.x, robo.y, c="red", s=200, label="Robô", edgecolors="black", marker="o")
    
    # Representando a direção do robô com uma seta
    if robo.direcao == 0:  # Norte
        plt.arrow(robo.x, robo.y, 0, 0.4, head_width=0.2, head_length=0.2, fc='red', ec='red')
    elif robo.direcao == 1:  # Leste
        plt.arrow(robo.x, robo.y, 0.4, 0, head_width=0.2, head_length=0.2, fc='red', ec='red')
    elif robo.direcao == 2:  # Sul
        plt.arrow(robo.x, robo.y, 0, -0.4, head_width=0.2, head_length=0.2, fc='red', ec='red')
    elif robo.direcao == 3:  # Oeste
        plt.arrow(robo.x, robo.y, -0.4, 0, head_width=0.2, head_length=0.2, fc='red', ec='red')

    plt.title("Simulador de Robô")
    plt.legend()
    st.pyplot(plt)

# Função para rodar a interface Streamlit
def main():
    st.title("Simulador de Robô - Controle e Automação")

    # Criar o robô (usando st.session_state para manter estado entre cliques)
    if "robo" not in st.session_state:
        st.session_state.robo = Robo()

    robo = st.session_state.robo

    # Exibir o ambiente
    desenha_ambiente(robo)

    # Controle do robô através de botões
    if st.button("Mover para Frente"):
        robo.move_forward()
        desenha_ambiente(robo)

    if st.button("Virar à Esquerda"):
        robo.turn_left()
        desenha_ambiente(robo)

    if st.button("Virar à Direita"):
        robo.turn_right()
        desenha_ambiente(robo)

# Rodar a aplicação Streamlit
if __name__ == "__main__":
    main()

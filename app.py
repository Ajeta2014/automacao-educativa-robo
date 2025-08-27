
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ==============================
# Classe Robô
# ==============================
class Robo:
    def __init__(self, grid_size=10):
        self.x = 0
        self.y = 0
        self.direcao = 0  # 0 = Norte, 1 = Leste, 2 = Sul, 3 = Oeste
        self.trajetoria = [(0, 0)]  # Histórico de posições
        self.grid_size = grid_size

    def move_forward(self, ambiente):
        """Move o robô para frente, verificando colisões"""
        novo_x, novo_y = self.x, self.y
        if self.direcao == 0:  # Norte
            novo_y += 1
        elif self.direcao == 1:  # Leste
            novo_x += 1
        elif self.direcao == 2:  # Sul
            novo_y -= 1
        elif self.direcao == 3:  # Oeste
            novo_x -= 1

        # Verificar limites e obstáculos
        if (0 <= novo_x < self.grid_size and 
            0 <= novo_y < self.grid_size and 
            ambiente[novo_y, novo_x] == 0):
            self.x, self.y = novo_x, novo_y
            self.trajetoria.append((self.x, self.y))
        else:
            st.warning("⚠️ Movimento bloqueado por obstáculo ou limite!")

    def turn_left(self):
        self.direcao = (self.direcao - 1) % 4

    def turn_right(self):
        self.direcao = (self.direcao + 1) % 4

    def sensor_frontal(self, ambiente):
        """Simula um sensor ultrassônico que detecta distância até o obstáculo à frente"""
        distancia = 0
        x, y = self.x, self.y

        while True:
            if self.direcao == 0:  # Norte
                y += 1
            elif self.direcao == 1:  # Leste
                x += 1
            elif self.direcao == 2:  # Sul
                y -= 1
            elif self.direcao == 3:  # Oeste
                x -= 1

            # Verifica se saiu do grid
            if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
                break

            distancia += 1

            # Se encontrou obstáculo
            if ambiente[y, x] == 1:
                break

        return distancia


# ==============================
# Função para desenhar ambiente
# ==============================
def desenha_ambiente(robo, ambiente, distancia_sensor):
    plt.clf()
    plt.imshow(ambiente, cmap="binary", origin="lower")

    # Trajetória
    trajetoria_x, trajetoria_y = zip(*robo.trajetoria)
    plt.plot(trajetoria_x, trajetoria_y, "b--", linewidth=1, label="Trajetória")

    # Robô
    plt.scatter(robo.x, robo.y, c="red", s=200, label="Robô", edgecolors="black", marker="o")

    # Direção do robô + sensor
    if robo.direcao == 0:  # Norte
        dx, dy = 0, 0.5
        plt.plot([robo.x, robo.x], [robo.y, robo.y + distancia_sensor], "g-", linewidth=2, label="Sensor")
    elif robo.direcao == 1:  # Leste
        dx, dy = 0.5, 0
        plt.plot([robo.x, robo.x + distancia_sensor], [robo.y, robo.y], "g-", linewidth=2, label="Sensor")
    elif robo.direcao == 2:  # Sul
        dx, dy = 0, -0.5
        plt.plot([robo.x, robo.x], [robo.y, robo.y - distancia_sensor], "g-", linewidth=2, label="Sensor")
    else:  # Oeste
        dx, dy = -0.5, 0
        plt.plot([robo.x, robo.x - distancia_sensor], [robo.y, robo.y], "g-", linewidth=2, label="Sensor")

    plt.arrow(robo.x, robo.y, dx, dy, head_width=0.3, head_length=0.2, fc="red", ec="red")

    plt.title("🤖 Simulador de Robô com Sensor Ultrassônico")
    plt.legend()
    st.pyplot(plt)


# ==============================
# Aplicação principal Streamlit
# ==============================
def main():
    st.title("🤖 Simulador de Robô com Sensores - Controle e Automação")

    # Configuração inicial
    grid_size = st.sidebar.slider("Tamanho do ambiente (NxN)", 5, 20, 10)

    # Criar ambiente
    if "ambiente" not in st.session_state or st.session_state.grid_size != grid_size:
        ambiente = np.zeros((grid_size, grid_size))
        ambiente[4, 4] = 1
        ambiente[6, 6] = 1
        ambiente[2, 7] = 1
        st.session_state.ambiente = ambiente
        st.session_state.grid_size = grid_size
        st.session_state.robo = Robo(grid_size)

    ambiente = st.session_state.ambiente
    robo = st.session_state.robo

    # Medir distância do sensor
    distancia_sensor = robo.sensor_frontal(ambiente)

    # Exibir ambiente
    desenha_ambiente(robo, ambiente, distancia_sensor)

    # Mostrar leitura do sensor
    st.metric("📡 Distância até obstáculo à frente", f"{distancia_sensor} células")

    # Controles
    st.sidebar.subheader("Controles do Robô")
    if st.sidebar.button("⬆️ Mover para Frente"):
        robo.move_forward(ambiente)
        distancia_sensor = robo.sensor_frontal(ambiente)
        desenha_ambiente(robo, ambiente, distancia_sensor)

    col1, col2 = st.sidebar.columns(2)
    if col1.button("⬅️ Esquerda"):
        robo.turn_left()
        distancia_sensor = robo.sensor_frontal(ambiente)
        desenha_ambiente(robo, ambiente, distancia_sensor)
    if col2.button("➡️ Direita"):
        robo.turn_right()
        distancia_sensor = robo.sensor_frontal(ambiente)
        desenha_ambiente(robo, ambiente, distancia_sensor)

    if st.sidebar.button("🔄 Resetar Robô"):
        st.session_state.robo = Robo(grid_size)
        distancia_sensor = st.session_state.robo.sensor_frontal(ambiente)
        desenha_ambiente(st.session_state.robo, ambiente, distancia_sensor)


# ==============================
if __name__ == "__main__":
    main()


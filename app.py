import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------
# Robô e Movimento
# ------------------------------
class Robo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direcao = 0  # 0=N,1=E,2=S,3=W
        self.trajetoria = [(self.x,self.y)]
        self.pontos = 0
        self.colisoes = 0
    
    def move_forward(self, obstaculos=None, grid_size=10):
        dx, dy = 0,0
        if self.direcao==0: dy=1
        elif self.direcao==1: dx=1
        elif self.direcao==2: dy=-1
        elif self.direcao==3: dx=-1
        
        nx, ny = self.x+dx, self.y+dy
        # Checar colisões
        if obstaculos and (nx,ny) in obstaculos:
            self.colisoes += 1
        elif 0 <= nx < grid_size and 0 <= ny < grid_size:
            self.x, self.y = nx, ny
            self.trajetoria.append((self.x,self.y))
            self.pontos += 1
    
    def turn_left(self): self.direcao = (self.direcao-1)%4
    def turn_right(self): self.direcao = (self.direcao+1)%4
    def reset(self):
        self.x, self.y, self.direcao = 0,0,0
        self.trajetoria = [(self.x,self.y)]
        self.pontos = 0
        self.colisoes = 0

# ------------------------------
# Ambiente
# ------------------------------
def desenha_ambiente(robo, grid_size=10, obstaculos=None, linha=None):
    ambiente = np.zeros((grid_size, grid_size))
    if obstaculos:
        for ox, oy in obstaculos:
            if 0 <= ox < grid_size and 0 <= oy < grid_size:
                ambiente[oy, ox] = 1

    plt.figure(figsize=(6,6))
    plt.imshow(ambiente, cmap="binary", origin="lower")
    
    # Linha de referência (seguidor de linha)
    if linha:
        lx, ly = zip(*linha)
        plt.plot(lx, ly, 'b--', lw=2, label="Linha")
    
    # Trajetória
    if len(robo.trajetoria) > 1:
        tx, ty = zip(*robo.trajetoria)
        plt.plot(tx, ty, 'orange', lw=2, label="Trajetória")
    
    # Robô
    plt.scatter(robo.x, robo.y, c="red", s=200, edgecolors="black", marker="o", label="Robô")
    dx, dy = 0, 0
    if robo.direcao==0: dy=0.4
    elif robo.direcao==1: dx=0.4
    elif robo.direcao==2: dy=-0.4
    elif robo.direcao==3: dx=-0.4
    plt.arrow(robo.x, robo.y, dx, dy, head_width=0.2, head_length=0.2, fc='red', ec='red')
    
    plt.title("Mini Laboratório de Robótica – Avançado")
    plt.legend()
    st.pyplot(plt)

# ------------------------------
# Módulo 0 – Fundamentos Teóricos
# ------------------------------
def modulo_fundamentos():
    st.subheader("Módulo 0 – Fundamentos Teóricos")
    st.markdown("""
    ### 🔹 Matemática
    - Álgebra Linear: vetores, matrizes, rotações.
    - Trigonometria: cálculo de ângulos e movimentos.
    - Cálculo Diferencial: velocidade e aceleração.
    - Estatística: sensores e ruído.
    
    ### 🔹 Física
    - Cinemática: movimento e coordenadas.
    - Dinâmica: forças, torque, leis de Newton.
    - Eletrônica: motores e atuadores.
    
    ### 🔹 Ciência da Computação
    - Programação: Python, C++, ROS.
    - Controle: PID, sensores, atuadores.
    - IA: navegação autônoma, visão computacional.
    """)
    
    st.markdown("### 📝 Mini Quiz")
    q1 = st.radio("Qual lei de Newton explica ação e reação?", 
                  ["1ª Lei – Inércia", "2ª Lei – F=ma", "3ª Lei – Ação e Reação"])
    if q1 == "3ª Lei – Ação e Reação": st.success("✅ Correto!")
    elif q1: st.warning("❌ Tente novamente.")

# ------------------------------
# Dashboard avançado
# ------------------------------
def dashboard(robo):
    st.subheader("📊 Painel de Métricas")
    st.markdown(f"- Posição: ({robo.x}, {robo.y})")
    st.markdown(f"- Direção: {['Norte','Leste','Sul','Oeste'][robo.direcao]}")
    st.markdown(f"- Passos dados: {len(robo.trajetoria)-1}")
    st.markdown(f"- Pontos: {robo.pontos}")
    st.markdown(f"- Colisões: {robo.colisoes}")

# ------------------------------
# Função de gamificação: medalhas
# ------------------------------
def medalhas(robo):
    if robo.pontos >= 10 and robo.colisoes == 0:
        st.success("🏅 Medalha Ouro – Perfeito!")
    elif robo.pontos >= 5:
        st.info("🥈 Medalha Prata – Bom desempenho")
    else:
        st.warning("🥉 Medalha Bronze – Continue praticando")

# ------------------------------
# Interface principal
# ------------------------------
def main():
    st.title("🚀 Mini Laboratório de Robótica – Avançado e Gamificado")
    
    # Sidebar: seleção de módulo
    modulo = st.sidebar.selectbox("Escolha o módulo", 
                                  ["0-Fundamentos","1-Movimento","2-Sensores",
                                   "3-Planejamento","4-Autônomo","5-IA"])
    
    # Obstáculos e linha de exemplo
    obstaculos = [(4,4),(6,6)]
    linha = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)]
    
    # Sessão do robô
    if "robo" not in st.session_state: st.session_state.robo = Robo()
    robo = st.session_state.robo
    
    if modulo=="0-Fundamentos":
        modulo_fundamentos()
    else:
        dashboard(robo)
        desenha_ambiente(robo, obstaculos=obstaculos, linha=(linha if modulo=="4-Autônomo" else None))
        
        col1, col2, col3, col4 = st.columns(4)
        if col1.button("Mover Frente"): robo.move_forward(obstaculos=obstaculos)
        if col2.button("Virar Esquerda"): robo.turn_left()
        if col3.button("Virar Direita"): robo.turn_right()
        if col4.button("Reset"): robo.reset()
        
        medalhas(robo)

# ------------------------------
if __name__ == "__main__":
    main()


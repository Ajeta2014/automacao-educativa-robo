import streamlit as st
from robo import Robo
from ambiente import Ambiente
from modulo import Modulo
from fundamentos import Fundamentos
from gamificacao import Gamificacao

# Inicializar estado
if "robo" not in st.session_state: st.session_state.robo = Robo()
robo = st.session_state.robo

if "fund" not in st.session_state: st.session_state.fund = Fundamentos()
fund = st.session_state.fund

if "game" not in st.session_state: st.session_state.game = Gamificacao()
game = st.session_state.game

# Definição dos módulos
modulos = {
    "0-Fundamentos": Modulo("0-Fundamentos","Aprender matemática, física e ciência da computação aplicadas à robótica.",
                             ["Compreender vetores, matrizes e transformações.",
                              "Entender cinemática e dinâmica.",
                              "Aprender programação e controle básico de robôs."]),
    "1-Movimento": Modulo("1-Movimento","Controlar o robô em todas as direções e diagonais.",
                           ["Mover para frente, trás, esquerda, direita e diagonais.",
                            "Evitar obstáculos e completar trajetórias."]),
    "2-Sensores": Modulo("2-Sensores","Aprender como o robô percebe o ambiente.",
                          ["Detectar obstáculos com sensores.",
                           "Seguir linhas e mapear trajetórias."]),

    "3-Planejamento": Modulo("3-Planejamento","Planejar caminhos eficientes e seguros.",
                             ["Planejar rota do ponto A ao B evitando obstáculos.",
                              "Otimizar trajetória."]),
    "4-Autônomo": Modulo("4-Autônomo","Programar o robô para agir sozinho.",
                          ["Evitar obstáculos automaticamente.",
                           "Seguir linhas e cumprir objetivos sem intervenção."]),
    "5-IA": Modulo("5-IA","Introdução à decisão baseada em dados e padrões.",
                   ["Reconhecer padrões e cores.",
                    "Escolher melhor rota e coletar objetos virtuais."])
}

# Ambientes distintos por módulo
ambientes = {
    "1-Movimento": Ambiente(obstaculos=[(4,4),(6,2)], linha=[(0,0),(2,2),(4,4)], metas=[(8,8)]),
    "2-Sensores": Ambiente(obstaculos=[(3,3),(5,5),(7,2)], linha=[(0,1),(1,2),(2,3)], metas=[(9,9)]),
    "3-Planejamento": Ambiente(obstaculos=[(2,2),(4,4),(6,6)], linha=[(0,0),(1,1),(2,2)], metas=[(9,0)]),
    "4-Autônomo": Ambiente(obstaculos=[(1,1),(3,3),(5,5)], linha=[(0,0),(1,2),(2,4)], metas=[(7,7)]),
    "5-IA": Ambiente(obstaculos=[(2,2),(3,5),(6,6)], linha=[(0,0),(2,2),(4,4)], metas=[(9,5)])
}

st.title("🚀 Mini Laboratório de Robótica – Completo e Gamificado")

# Menu lateral
modulo = st.sidebar.selectbox("Escolha o módulo", list(modulos.keys()))
modulos[modulo].mostrar_info()

# Função de movimento
def move_robo(direcao):
    if modulo != "0-Fundamentos":
        robo.move(direcao, obstaculos=ambientes[modulo].obstaculos)

# Teoria e quiz
if modulo == "0-Fundamentos":
    fund.mostrar()
    fund.quiz()
else:
    ambientes[modulo].desenha(robo)
    game.mostrar(robo)

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    if col1.button("N"): move_robo("N")
    if col2.button("S"): move_robo("S")
    if col3.button("E"): move_robo("E")
    if col4.button("W"): move_robo("W")
    if col5.button("NE"): move_robo("NE")
    if col6.button("NW"): move_robo("NW")
    if col7.button("SE"): move_robo("SE")
    if col8.button("SW"): move_robo("SW")

    if st.button("Reset"): robo.reset()

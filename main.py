import streamlit as st
from robo import Robo
from ambiente import Ambiente
from fundamentos import Fundamentos
from gamificacao import Gamificacao

# Inicializar robô no session_state
if "robo" not in st.session_state:
    st.session_state.robo = Robo()
robo = st.session_state.robo

# Inicializar ambiente e classes auxiliares
if "amb" not in st.session_state:
    st.session_state.amb = Ambiente(obstaculos=[(4,4),(6,6)], linha=[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)])
amb = st.session_state.amb

if "fund" not in st.session_state:
    st.session_state.fund = Fundamentos()
fund = st.session_state.fund

if "game" not in st.session_state:
    st.session_state.game = Gamificacao()
game = st.session_state.game

st.title("🚀 Mini Laboratório de Robótica – Completo e Gamificado")

# Menu lateral
modulo = st.sidebar.selectbox("Escolha o módulo", 
                              ["0-Fundamentos","1-Movimento","2-Sensores",
                               "3-Planejamento","4-Autônomo","5-IA"])

# Função para atualizar movimento
def move_robo(direcao):
    robo.move(direcao, obstaculos=amb.obstaculos)

# Módulo 0 – Teoria e Quiz
if modulo == "0-Fundamentos":
    fund.mostrar()
    fund.quiz()

# Outros módulos – Movimento + Gamificação
else:
    game.mostrar(robo)
    amb.desenha(robo)

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


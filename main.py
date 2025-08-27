import streamlit as st
from robo import Robo
from ambiente import Ambiente
from fundamentos import Fundamentos
from gamificacao import Gamificacao

# Inicializar estado
if "robo" not in st.session_state: st.session_state.robo = Robo()
robo = st.session_state.robo

if "fund" not in st.session_state: st.session_state.fund = Fundamentos()
fund = st.session_state.fund

if "game" not in st.session_state: st.session_state.game = Gamificacao()
game = st.session_state.game

# Ambientes diferentes para cada módulo
ambientes = {
    "1-Movimento": Ambiente(obstaculos=[(4,4)], linha=[(0,0),(1,1),(2,2)]),
    "2-Sensores": Ambiente(obstaculos=[(3,3),(5,5)], linha=[(0,1),(1,2),(2,3)]),
    "3-Planejamento": Ambiente(obstaculos=[(2,2),(4,4),(6,6)], linha=[(0,0),(1,1),(2,2)]),
    "4-Autônomo": Ambiente(obstaculos=[(1,1),(3,3),(5,5)], linha=[(0,0),(1,2),(2,4)]),
    "5-IA": Ambiente(obstaculos=[(2,2),(3,5),(6,6)], linha=[(0,0),(2,2),(4,4)])
}

st.title("🚀 Mini Laboratório de Robótica – Completo e Gamificado")

# Menu lateral
modulo = st.sidebar.selectbox("Escolha o módulo", 
                              ["0-Fundamentos","1-Movimento","2-Sensores","3-Planejamento","4-Autônomo","5-IA"])

# Função de movimento
def move_robo(direcao):
    robo.move(direcao, obstaculos=ambentes[modulo].obstaculos)

if modulo == "0-Fundamentos":
    fund.mostrar()
    fund.quiz()
else:
    ambentes[modulo].desenha(robo)
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



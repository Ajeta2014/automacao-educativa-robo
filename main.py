import streamlit as st
from robo import Robo
from ambiente import Ambiente
from fundamentos import Fundamentos
from gamificacao import Gamificacao

# Inicializar
if "robo" not in st.session_state: st.session_state.robo = Robo()
robo = st.session_state.robo
amb = Ambiente(obstaculos=[(4,4),(6,6)], linha=[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)])
fund = Fundamentos()
game = Gamificacao()

st.title("🚀 Mini Laboratório de Robótica – Modular e Gamificado")

modulo = st.sidebar.selectbox("Escolha o módulo", 
                              ["0-Fundamentos","1-Movimento","2-Sensores",
                               "3-Planejamento","4-Autônomo","5-IA"])

if modulo == "0-Fundamentos":
    fund.mostrar()
    fund.quiz()
else:
    game.mostrar(robo)
    amb.desenha(robo)
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("Mover Frente"): robo.move_forward(obstaculos=amb.obstaculos)
    if col2.button("Virar Esquerda"): robo.turn_left()
    if col3.button("Virar Direita"): robo.turn_right()
    if col4.button("Reset"): robo.reset()

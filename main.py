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

st.title("🚀 Mini Laboratório de Robótica – Completo e Gamificado")

modulo = st.sidebar.selectbox("Escolha o módulo", 
                              ["0-Fundamentos","1-Movimento","2-Sensores",
                               "3-Planejamento","4-Autônomo","5-IA"])

if modulo == "0-Fundamentos":
    fund.mostrar()
    fund.quiz()
else:
    game.mostrar(robo)
    amb.desenha(robo)

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    if col1.button("N"): robo.move("N", obstaculos=amb.obstaculos)
    if col2.button("S"): robo.move("S", obstaculos=amb.obstaculos)
    if col3.button("E"): robo.move("E", obstaculos=amb.obstaculos)
    if col4.button("W"): robo.move("W", obstaculos=amb.obstaculos)
    if col5.button("NE"): robo.move("NE", obstaculos=amb.obstaculos)
    if col6.button("NW"): robo.move("NW", obstaculos=amb.obstaculos)
    if col7.button("SE"): robo.move("SE", obstaculos=amb.obstaculos)
    if col8.button("SW"): robo.move("SW", obstaculos=amb.obstaculos)

    if st.button("Reset"): robo.reset()

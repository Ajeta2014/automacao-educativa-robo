import streamlit as st

class Modulo:
    def __init__(self, nome, missao, objetivos):
        self.nome = nome
        self.missao = missao
        self.objetivos = objetivos

    def mostrar_info(self):
        st.sidebar.subheader(f"Módulo {self.nome}")
        st.sidebar.markdown(f"**Missão:** {self.missao}")
        st.sidebar.markdown("**Objetivos:**")
        for obj in self.objetivos:
            st.sidebar.markdown(f"- {obj}")

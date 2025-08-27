import streamlit as st
import random

class Fundamentos:
    def mostrar(self):
        st.subheader("Módulo 0 – Fundamentos Teóricos")
        st.markdown("""
        ### 🔹 Matemática
        - Álgebra Linear: vetores, matrizes, rotações
        - Trigonometria: seno, cosseno, tangente
        - Cálculo Diferencial: velocidade, aceleração
        - Estatística: ruído de sensores
        
        ### 🔹 Física
        - Cinemática: movimento de corpos
        - Dinâmica: forças, torque, leis de Newton
        - Eletrônica: motores e atuadores
        
        ### 🔹 Ciência da Computação
        - Programação: Python, C++, ROS
        - Controle: PID, sensores, atuadores
        - IA: visão computacional, navegação
        """)

    def quiz(self):
        st.markdown("### 📝 Quiz aleatório")
        perguntas = [
            {"pergunta": "Qual lei de Newton explica ação e reação?", "opcoes": ["1ª Lei", "2ª Lei", "3ª Lei"], "resposta": "3ª Lei"},
            {"pergunta": "Seno, cosseno e tangente são usados em qual área da robótica?", "opcoes": ["Matemática", "Física", "IA"], "resposta": "Matemática"},
            {"pergunta": "Qual sensor é usado para medir distância?", "opcoes": ["Ultrassônico", "Servo", "Motor"], "resposta": "Ultrassônico"},
            {"pergunta": "O que é PID?", "opcoes": ["Controlador", "Motor", "Sensor"], "resposta": "Controlador"}
        ]
        pergunta = random.choice(perguntas)
        escolha = st.radio(pergunta["pergunta"], pergunta["opcoes"])
        if escolha == pergunta["resposta"]:
            st.success("✅ Correto!")
        elif escolha:
            st.warning("❌ Tente novamente.")



import streamlit as st

class Fundamentos:
    def mostrar(self):
        st.subheader("Módulo 0 – Fundamentos Teóricos")
        st.markdown("""
        ### 🔹 Matemática
        - Álgebra Linear, Trigonometria, Cálculo Diferencial, Estatística
        
        ### 🔹 Física
        - Cinemática, Dinâmica, Torque, Leis de Newton
        
        ### 🔹 Ciência da Computação
        - Programação (Python, C++), Controle PID, Sensores, IA
        """)

    def quiz(self):
        st.markdown("### 📝 Mini Quiz")
        q1 = st.radio("Qual lei de Newton explica ação e reação?", 
                      ["1ª Lei – Inércia", "2ª Lei – F=ma", "3ª Lei – Ação e Reação"])
        if q1 == "3ª Lei – Ação e Reação": st.success("✅ Correto!")
        elif q1: st.warning("❌ Tente novamente.")

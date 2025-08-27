import streamlit as st

class Gamificacao:
    def mostrar(self, robo):
        st.subheader("📊 Painel de Métricas")
        st.markdown(f"- Posição: ({robo.x}, {robo.y})")
        st.markdown(f"- Direção: {['Norte','Leste','Sul','Oeste'][robo.direcao]}")
        st.markdown(f"- Passos: {len(robo.trajetoria)-1}")
        st.markdown(f"- Pontos: {robo.pontos}")
        st.markdown(f"- Colisões: {robo.colisoes}")
        self.medalha(robo)

    def medalha(self, robo):
        if robo.pontos >= 10 and robo.colisoes == 0:
            st.success("🏅 Medalha Ouro – Perfeito!")
        elif robo.pontos >= 5:
            st.info("🥈 Medalha Prata – Bom desempenho")
        else:
            st.warning("🥉 Medalha Bronze – Continue praticando")

import streamlit as st
import random

class Fundamentos:
    def mostrar(self):
        st.subheader("Módulo 0 – Fundamentos Teóricos Explicados")
        
        st.markdown("### Matemática")
        st.markdown("""
        - **Álgebra Linear:** vetores, matrizes e transformações lineares.  
          *Explicação:* Usada para representar movimentos e posições de robôs em 2D e 3D.
          
        - **Geometria Analítica:** cálculo de posições, ângulos, distâncias e interseções.  
          *Explicação:* Permite calcular trajetórias e colisões entre objetos no espaço.
          
        - **Trigonometria:** seno, cosseno, tangente.  
          *Explicação:* Essencial para movimentos rotacionais e ângulos de juntas de robôs.
          
        - **Cálculo Diferencial e Integral:** derivadas e integrais para velocidade, aceleração, trajetória.  
          *Explicação:* Permite prever e controlar o movimento dos robôs com precisão.
          
        - **Estatística e Probabilidade:** análise de ruído de sensores e probabilidade de falhas.  
          *Explicação:* Ajuda a filtrar dados ruidosos e prever falhas no sistema.
        """)

        st.markdown("### Física")
        st.markdown("""
        - **Cinemática:** movimento de corpos rígidos, velocidade linear e angular.  
          *Explicação:* Permite entender como robôs se deslocam e giram.
          
        - **Dinâmica:** forças, torque (τ = F × d), leis de Newton, energia cinética e potencial.  
          *Explicação:* Essencial para projetar sistemas que aplicam força e movimento.
          
        - **Eletrônica Básica:** motores, sensores, atuadores, resistores, capacitores.  
          *Explicação:* Entender o funcionamento dos componentes que movem e controlam robôs.
          
        - **Mecânica de Materiais:** tensão, deformação, flexão e torção.  
          *Explicação:* Permite dimensionar estruturas de robôs que suportem cargas.
        """)

        st.markdown("### Ciência da Computação")
        st.markdown("""
        - **Programação:** Python, estruturas de dados, loops, funções, orientação a objetos.  
          *Explicação:* Base para criar algoritmos que controlam robôs e processam dados.
          
        - **Controle:** PID, sistemas em malha aberta e fechada, estabilidade.  
          *Explicação:* Mantém movimentos precisos e estáveis, mesmo com perturbações.
          
        - **Inteligência Artificial:** visão computacional, aprendizado de máquina, navegação autônoma.  
          *Explicação:* Permite que robôs detectem objetos, tomem decisões e se movimentem sozinhos.
          
        - **Redes e Comunicação:** protocolos, transmissão de dados entre sensores e controladores.  
          *Explicação:* Fundamental para integração de sistemas e troca de informações em tempo real.
        """)

    def quiz(self):
        st.markdown("### Quiz Aleatório de Fundamentos com Explicação")
        perguntas = [
            {"pergunta": "Qual lei de Newton explica ação e reação?", "opcoes": ["1ª Lei", "2ª Lei", "3ª Lei"], "resposta": "3ª Lei",
             "explicacao": "A 3ª Lei afirma que para toda ação há uma reação igual e oposta, fundamental em robótica para entender forças."},
            
            {"pergunta": "Seno, cosseno e tangente são usados em qual área da robótica?", "opcoes": ["Matemática", "Física", "IA"], "resposta": "Matemática",
             "explicacao": "Funções trigonométricas são usadas para calcular ângulos e movimentos rotacionais de robôs."},
            
            {"pergunta": "Qual sensor é usado para medir distância?", "opcoes": ["Ultrassônico", "Servo", "Motor"], "resposta": "Ultrassônico",
             "explicacao": "O sensor ultrassônico mede distâncias emitindo ondas sonoras e calculando o tempo de retorno."},
            
            {"pergunta": "O que é PID?", "opcoes": ["Controlador", "Motor", "Sensor"], "resposta": "Controlador",
             "explicacao": "PID é um controlador que ajusta saídas para manter variáveis como velocidade ou posição estáveis."},
            
            {"pergunta": "Qual unidade é usada para medir torque?", "opcoes": ["Newton", "Newton-metro", "Pascal"], "resposta": "Newton-metro",
             "explicacao": "Torque mede a força de rotação aplicada a um eixo, calculado em Newton-metros (N·m)."},
            
            {"pergunta": "Qual componente armazena carga elétrica?", "opcoes": ["Resistor", "Capacitor", "Indutor"], "resposta": "Capacitor",
             "explicacao": "O capacitor armazena energia elétrica temporariamente e ajuda a filtrar sinais em circuitos."},
            
            {"pergunta": "Em Python, qual estrutura é usada para armazenar múltiplos valores ordenados?", "opcoes": ["Lista", "Dicionário", "Tupla"], "resposta": "Lista",
             "explicacao": "Listas armazenam múltiplos itens em ordem, permitindo acesso e manipulação simples."},
            
            {"pergunta": "O que representa a derivada de uma função de posição em relação ao tempo?", "opcoes": ["Aceleração", "Velocidade", "Força"], "resposta": "Velocidade",
             "explicacao": "A derivada da posição em relação ao tempo é a velocidade, usada para movimentação precisa de robôs."},
            
            {"pergunta": "Qual protocolo é comumente usado em comunicação industrial entre PLCs?", "opcoes": ["HTTP", "Modbus", "FTP"], "resposta": "Modbus",
             "explicacao": "Modbus é um protocolo industrial para comunicação de dados entre controladores e sensores."},
            
            {"pergunta": "Qual sensor pode detectar obstáculos usando luz infravermelha?", "opcoes": ["IR", "Ultrassônico", "GPS"], "resposta": "IR",
             "explicacao": "Sensores IR detectam obstáculos refletindo luz infravermelha, útil para robôs móveis."}
        ]
        
        pergunta = random.choice(perguntas)
        escolha = st.radio(pergunta["pergunta"], pergunta["opcoes"])
        
        if escolha == pergunta["resposta"]:
            st.success(f"✅ Correto! {pergunta['explicacao']}")
        elif escolha:
            st.warning(f"❌ Tente novamente. Explicação: {pergunta['explicacao']}")


# Mini Laboratório de Robótica — Plataforma Educativa (Streamlit)
# Autor: ChatGPT
# Requisitos: streamlit, numpy, matplotlib
# Rode com: streamlit run mini_lab_robotica.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import heapq

# =============================================
# Utilidades de Ambiente
# =============================================

def criar_ambiente(n, densidade=0.15, seed=None):
    """Cria um grid NxN com obstáculos (1 = obstáculo, 0 = livre).
    densidade em [0, 0.6] aprox. """
    rng = np.random.default_rng(seed)
    env = np.zeros((n, n), dtype=int)
    mask = rng.random((n, n)) < float(densidade)
    env[mask] = 1
    return env


def limpar_ambiente(env):
    env[:] = 0


def desenhar_linha(env, caminho="reta"):
    """Marca uma linha (valor 2) para laboratório de seguidor de linha.
    caminho: 'reta' | 'curva' | 'zigzag'. """
    n = env.shape[0]
    # Zera linhas anteriores (valor 2)
    env[env == 2] = 0
    if caminho == "reta":
        x = n // 2
        env[:, x] = 2
    elif caminho == "curva":
        for y in range(n):
            x = int((n/2) + (n/4) * np.sin(2 * np.pi * y / max(1, (n-1))))
            env[y, np.clip(x, 0, n-1)] = 2
    elif caminho == "zigzag":
        x = 1
        step = 1
        for y in range(n):
            env[y, np.clip(x, 0, n-1)] = 2
            if x >= n-2:
                step = -1
            if x <= 1:
                step = 1
            x += step


# =============================================
# Classe do Robô
# =============================================
class Robo:
    def __init__(self, grid_size=10, x=0, y=0, direcao=0):
        self.x = int(x)
        self.y = int(y)
        self.direcao = int(direcao)  # 0=N,1=L,2=S,3=O
        self.grid_size = int(grid_size)
        self.trajetoria = [(self.x, self.y)]

    # ---- Movimento
    def move_forward(self, env):
        nx, ny = self.x, self.y
        if self.direcao == 0:
            ny += 1
        elif self.direcao == 1:
            nx += 1
        elif self.direcao == 2:
            ny -= 1
        else:
            nx -= 1
        if self.posicao_valida(env, nx, ny):
            self.x, self.y = nx, ny
            self.trajetoria.append((self.x, self.y))
            return True
        return False

    def turn_left(self):
        self.direcao = (self.direcao - 1) % 4

    def turn_right(self):
        self.direcao = (self.direcao + 1) % 4

    def posicao_valida(self, env, x, y):
        n = self.grid_size
        return 0 <= x < n and 0 <= y < n and env[y, x] != 1

    def reset(self, x=0, y=0, direcao=0):
        self.x, self.y, self.direcao = int(x), int(y), int(direcao)
        self.trajetoria = [(self.x, self.y)]

    # ---- Sensores (distâncias em células)
    def sensor_frontal(self, env, max_alcance=None):
        return self._raycast(env, self.direcao, max_alcance)

    def sensor_esquerda(self, env, max_alcance=None):
        return self._raycast(env, (self.direcao - 1) % 4, max_alcance)

    def sensor_direita(self, env, max_alcance=None):
        return self._raycast(env, (self.direcao + 1) % 4, max_alcance)

    def _raycast(self, env, direcao, max_alcance=None):
        dx, dy = {0:(0,1), 1:(1,0), 2:(0,-1), 3:(-1,0)}[direcao]
        n = env.shape[0]
        x, y = self.x, self.y
        dist = 0
        limite = max_alcance if max_alcance is not None else (2*n)
        for _ in range(limite):
            x += dx; y += dy
            if not (0 <= x < n and 0 <= y < n):
                break
            dist += 1
            if env[y, x] == 1:  # obstáculo
                break
        return dist

    # ---- Sensor de linha (valor 2 no grid)
    def sensor_linha(self, env):
        # Lê célula imediatamente à frente.
        dx, dy = {0:(0,1), 1:(1,0), 2:(0,-1), 3:(-1,0)}[self.direcao]
        x, y = self.x + dx, self.y + dy
        n = env.shape[0]
        if 0 <= x < n and 0 <= y < n:
            return 1 if env[y, x] == 2 else 0
        return 0


# =============================================
# Desenho/Visualização
# =============================================

def desenhar(env, robo: Robo, titulo="", mostrar_sensores=False, path=None):
    plt.clf()
    # 0 = livre, 1 = obstáculo, 2 = linha
    cmap = plt.cm.binary
    # Vamos mapear 2 (linha) para tons intermediários
    vis = env.copy()
    plt.imshow(vis, cmap="binary", origin="lower")

    # Trajetória
    if robo.trajetoria:
        tx, ty = zip(*robo.trajetoria)
        plt.plot(tx, ty, "--", linewidth=1, label="Trajetória")

    # Caminho planejado
    if path:
        px, py = zip(*path)
        plt.plot(px, py, "-", linewidth=2, label="Caminho")

    # Robô
    plt.scatter(robo.x, robo.y, s=200, marker="o", edgecolors="black", label="Robô")

    # Direção seta
    dx, dy = {0:(0,0.6), 1:(0.6,0), 2:(0,-0.6), 3:(-0.6,0)}[robo.direcao]
    plt.arrow(robo.x, robo.y, dx, dy, head_width=0.3, head_length=0.2)

    # Sensores (raios)
    if mostrar_sensores:
        f = robo.sensor_frontal(env)
        l = robo.sensor_esquerda(env)
        r = robo.sensor_direita(env)
        # Frontal
        if robo.direcao == 0:
            plt.plot([robo.x, robo.x], [robo.y, robo.y + f], linewidth=2)
            plt.plot([robo.x, robo.x - l], [robo.y, robo.y], linewidth=2)
            plt.plot([robo.x, robo.x + r], [robo.y, robo.y], linewidth=2)
        elif robo.direcao == 1:
            plt.plot([robo.x, robo.x + f], [robo.y, robo.y], linewidth=2)
            plt.plot([robo.x, robo.x], [robo.y, robo.y + l], linewidth=2)
            plt.plot([robo.x, robo.x], [robo.y, robo.y - r], linewidth=2)
        elif robo.direcao == 2:
            plt.plot([robo.x, robo.x], [robo.y, robo.y - f], linewidth=2)
            plt.plot([robo.x, robo.x + l], [robo.y, robo.y], linewidth=2)
            plt.plot([robo.x, robo.x - r], [robo.y, robo.y], linewidth=2)
        else:
            plt.plot([robo.x, robo.x - f], [robo.y, robo.y], linewidth=2)
            plt.plot([robo.x, robo.x], [robo.y, robo.y - l], linewidth=2)
            plt.plot([robo.x, robo.x], [robo.y, robo.y + r], linewidth=2)

    plt.title(titulo)
    plt.legend(loc="upper right")
    st.pyplot(plt)


# =============================================
# Planejamento de Caminho (BFS, Dijkstra, A*)
# =============================================

def vizinhos(env, x, y):
    n = env.shape[0]
    for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
        nx, ny = x+dx, y+dy
        if 0 <= nx < n and 0 <= ny < n and env[ny, nx] != 1:
            yield nx, ny


def bfs(env, start, goal):
    q = deque([start])
    prev = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal:
            break
        for nb in vizinhos(env, *cur):
            if nb not in prev:
                prev[nb] = cur
                q.append(nb)
    if goal not in prev:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def dijkstra(env, start, goal):
    dist = {start: 0}
    prev = {start: None}
    pq = [(0, start)]
    while pq:
        d, cur = heapq.heappop(pq)
        if cur == goal:
            break
        if d > dist.get(cur, float('inf')):
            continue
        for nb in vizinhos(env, *cur):
            nd = d + 1  # custo uniforme
            if nd < dist.get(nb, float('inf')):
                dist[nb] = nd
                prev[nb] = cur
                heapq.heappush(pq, (nd, nb))
    if goal not in prev:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


def heuristica(a, b):
    # Manhattan
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def a_estrela(env, start, goal):
    g = {start: 0}
    prev = {start: None}
    pq = [(heuristica(start, goal), start)]
    while pq:
        f, cur = heapq.heappop(pq)
        if cur == goal:
            break
        for nb in vizinhos(env, *cur):
            ng = g[cur] + 1
            if ng < g.get(nb, float('inf')):
                g[nb] = ng
                prev[nb] = cur
                fscore = ng + heuristica(nb, goal)
                heapq.heappush(pq, (fscore, nb))
    if goal not in prev:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


# =============================================
# Módulos (Páginas)
# =============================================

def modulo_fundamentos(env, robo):
    st.subheader("Módulo 1 — Fundamentos de Movimento")
    colA, colB, colC, colD = st.columns(4)
    if colA.button("⬆️ Frente"):
        robo.move_forward(env)
    if colB.button("⬅️ Esquerda"):
        robo.turn_left()
    if colC.button("➡️ Direita"):
        robo.turn_right()
    if colD.button("🔄 Reset Posição"):
        robo.reset()

    desenhar(env, robo, titulo="Movimento e Trajetória")


def modulo_sensores(env, robo):
    st.subheader("Módulo 2 — Sensores e Percepção")
    max_alc = st.slider("Alcance máx. do sensor (células)", 1, env.shape[0]*2, env.shape[0])
    f = robo.sensor_frontal(env, max_alc)
    l = robo.sensor_esquerda(env, max_alc)
    r = robo.sensor_direita(env, max_alc)
    c1, c2, c3 = st.columns(3)
    c1.metric("Frontal", f)
    c2.metric("Esquerda", l)
    c3.metric("Direita", r)

    st.info("Dica: use os botões de movimento do módulo 1 para mudar posição/direção e volte aqui.")
    desenhar(env, robo, titulo="Leituras de Sensores (raios)", mostrar_sensores=True)


def modulo_planejamento(env, robo):
    st.subheader("Módulo 3 — Planejamento de Caminho (BFS / Dijkstra / A*)")
    n = env.shape[0]
    col1, col2, col3 = st.columns(3)
    sx = col1.number_input("Start X", 0, n-1, value=int(robo.x))
    sy = col2.number_input("Start Y", 0, n-1, value=int(robo.y))
    robo_start = (int(sx), int(sy))
    gx = col1.number_input("Goal X", 0, n-1, value=min(n-1, int(robo.x)+3))
    gy = col2.number_input("Goal Y", 0, n-1, value=min(n-1, int(robo.y)+3))
    goal = (int(gx), int(gy))

    alg = col3.selectbox("Algoritmo", ["BFS", "Dijkstra", "A*"])

    path = None
    if st.button("▶️ Calcular Caminho"):
        if alg == "BFS":
            path = bfs(env, tuple(robo_start), tuple(goal))
        elif alg == "Dijkstra":
            path = dijkstra(env, tuple(robo_start), tuple(goal))
        else:
            path = a_estrela(env, tuple(robo_start), tuple(goal))
        st.session_state.path_planejado = path
        if path is None:
            st.error("Nenhum caminho encontrado.")
        else:
            st.success(f"Caminho com {len(path)} passos encontrado.")

    path = st.session_state.get("path_planejado")
    desenhar(env, robo, titulo=f"Planejamento: {alg}", path=path)

    if path:
        if st.button("🤖 Seguir Caminho (passo a passo)"):
            # Move 1 passo por clique
            # Primeira posição do path é a posição inicial; buscamos a próxima.
            try:
                idx = path.index((robo.x, robo.y))
            except ValueError:
                # Se o robô não está exatamente sobre o path, reposiciona ao início
                robo.reset(*path[0], direcao=robo.direcao)
                idx = 0
            if idx < len(path)-1:
                nx, ny = path[idx+1]
                # Ajusta direção (simples)
                if nx > robo.x: robo.direcao = 1
                elif nx < robo.x: robo.direcao = 3
                elif ny > robo.y: robo.direcao = 0
                else: robo.direcao = 2
                robo.move_forward(env)


def modulo_autonomo(env, robo):
    st.subheader("Módulo 4 — Controle Autônomo (Reativo)")
    estrategia = st.selectbox("Estratégia", [
        "Desvio por Parede (direita)",
        "Desvio por Parede (esquerda)",
        "Seguidor de Linha"
    ])

    if estrategia.startswith("Desvio"):
        passos = st.slider("Passos por execução", 1, 50, 5)
        if st.button("▶️ Executar"):
            for _ in range(passos):
                f = robo.sensor_frontal(env)
                l = robo.sensor_esquerda(env)
                r = robo.sensor_direita(env)
                if f <= 1:
                    # Parede à frente: escolha lado
                    if "direita" in estrategia:
                        # prioriza direita
                        if r > l:
                            robo.turn_right()
                        else:
                            robo.turn_left()
                    else:
                        # prioriza esquerda
                        if l > r:
                            robo.turn_left()
                        else:
                            robo.turn_right()
                else:
                    robo.move_forward(env)

    else:
        st.caption("Para o seguidor de linha, desenhe uma linha no ambiente (aba Lateral > Linha)")
        passos = st.slider("Passos por execução", 1, 50, 10)
        ganho_curva = st.slider("Ganho de Curva", 1, 5, 2)
        if st.button("▶️ Executar Seguidor"):
            for _ in range(passos):
                leitura = robo.sensor_linha(env)
                if leitura == 1:
                    # Linha à frente: siga em frente
                    robo.move_forward(env)
                else:
                    # Procura a linha (varre)
                    for _ in range(ganho_curva):
                        robo.turn_left()
                        if robo.sensor_linha(env) == 1:
                            break
                    robo.move_forward(env)

    desenhar(env, robo, titulo=f"Autônomo: {estrategia}")


def modulo_ia(env, robo):
    st.subheader("Módulo 5 — Integração com IA (Política Linear Simples)")
    st.caption("Demonstração didática: uma política linear decide a ação com base nas distâncias dos sensores (frente/esq/dir).")

    # Pesos da política (w_f, w_l, w_r) por ação: F, L, R
    if "ia_pesos" not in st.session_state:
        st.session_state.ia_pesos = {
            "F": np.array([ 1.0, -0.2, -0.2]),
            "L": np.array([-0.5,  1.0, -0.3]),
            "R": np.array([-0.5, -0.3,  1.0]),
        }

    pesos = st.session_state.ia_pesos

    def escolher_acao(obs):
        # obs = [f,l,r] normalizados
        scores = {a: float(np.dot(w, obs)) for a, w in pesos.items()}
        return max(scores, key=scores.get), scores

    # Normalização simples pelo tamanho do grid
    nmax = env.shape[0]
    f = robo.sensor_frontal(env)
    l = robo.sensor_esquerda(env)
    r = robo.sensor_direita(env)
    obs = np.array([f, l, r], dtype=float) / max(1.0, nmax)

    acao, scores = escolher_acao(obs)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Frente", f)
    c2.metric("Esq", l)
    c3.metric("Dir", r)
    c4.metric("Ação IA", acao)

    st.json({"scores": scores})

    colA, colB, colC = st.columns(3)
    if colA.button("▶️ Executar Ação da IA"):
        if acao == "F":
            robo.move_forward(env)
        elif acao == "L":
            robo.turn_left()
        else:
            robo.turn_right()

    with st.expander("Ajustar Pesos (aprendizado manual)"):
        for a in ["F","L","R"]:
            p = pesos[a]
            w0 = st.slider(f"{a} - w_frente", -2.0, 2.0, float(p[0]), 0.1)
            w1 = st.slider(f"{a} - w_esq",    -2.0, 2.0, float(p[1]), 0.1)
            w2 = st.slider(f"{a} - w_dir",    -2.0, 2.0, float(p[2]), 0.1)
            pesos[a] = np.array([w0, w1, w2])
        st.session_state.ia_pesos = pesos

    desenhar(env, robo, titulo="IA: Política Linear em Ação", mostrar_sensores=True)


# =============================================
# App Principal (Menu e Estado Global)
# =============================================

def inicializar_estado():
    if "grid_n" not in st.session_state:
        st.session_state.grid_n = 12
    if "densidade" not in st.session_state:
        st.session_state.densidade = 0.15
    if "seed" not in st.session_state:
        st.session_state.seed = 42
    if "env" not in st.session_state:
        st.session_state.env = criar_ambiente(st.session_state.grid_n, st.session_state.densidade, st.session_state.seed)
    if "robo" not in st.session_state:
        st.session_state.robo = Robo(grid_size=st.session_state.grid_n)
    if "path_planejado" not in st.session_state:
        st.session_state.path_planejado = None


def painel_lateral():
    st.sidebar.title("📚 Mini Lab de Robótica")
    st.sidebar.caption("Aprenda robótica do básico ao avançado, com laboratórios interativos.")

    # Config do ambiente
    n = st.sidebar.slider("Tamanho do ambiente (N)", 6, 30, st.session_state.grid_n)
    dens = st.sidebar.slider("Densidade de obstáculos", 0.0, 0.5, float(st.session_state.densidade), 0.01)
    seed = st.sidebar.number_input("Seed", 0, 10_000, int(st.session_state.seed))

    colA, colB = st.sidebar.columns(2)
    if colA.button("🌍 Novo Ambiente"):
        st.session_state.grid_n = n
        st.session_state.densidade = dens
        st.session_state.seed = seed
        st.session_state.env = criar_ambiente(n, dens, seed)
        st.session_state.robo = Robo(grid_size=n)
        st.session_state.path_planejado = None

    if colB.button("🧹 Limpar Obstáculos"):
        limpar_ambiente(st.session_state.env)
        st.session_state.path_planejado = None

    # Linha para seguidor de linha
    st.sidebar.markdown("---")
    st.sidebar.subheader("Linha (para seguidor)")
    modo_linha = st.sidebar.selectbox("Desenhar Linha", ["nenhuma", "reta", "curva", "zigzag"])
    if modo_linha != "nenhuma":
        desenhar_linha(st.session_state.env, modo_linha)

    st.sidebar.markdown("---")
    modulo = st.sidebar.radio("Escolha o módulo:", [
        "Fundamentos de Movimento",
        "Sensores e Percepção",
        "Planejamento de Caminho",
        "Controle Autônomo",
        "Integração com IA",
    ])
    return modulo


def main():
    st.set_page_config(page_title="Mini Lab de Robótica", layout="wide")
    inicializar_estado()

    modulo = painel_lateral()

    env = st.session_state.env
    robo = st.session_state.robo

    # Cabeçalho
    st.title("🤖 Mini Laboratório de Robótica — Plataforma Educativa")
    st.caption("5 módulos: Movimento, Sensores, Planejamento, Autonomia e IA. Controle tudo no menu lateral.")

    if modulo == "Fundamentos de Movimento":
        modulo_fundamentos(env, robo)
    elif modulo == "Sensores e Percepção":
        modulo_sensores(env, robo)
    elif modulo == "Planejamento de Caminho":
        modulo_planejamento(env, robo)
    elif modulo == "Controle Autônomo":
        modulo_autonomo(env, robo)
    else:
        modulo_ia(env, robo)


if __name__ == "__main__":
    main()

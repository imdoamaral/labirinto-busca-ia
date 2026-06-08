"""Algoritmos de busca clássica no labirinto conhecido (Parte II do enunciado).

Implementa, com uma assinatura única, os cinco algoritmos obrigatórios:
    BFS, DFS, UCS (custo uniforme), Busca Gulosa e A*.

Cada função recebe um `ProblemaLabirinto` e devolve uma tupla:
    (caminho, metricas)
onde `caminho` é a lista de estados do início ao objetivo (ou None se a busca
falhar) e `metricas` é um objeto `Metricas` preenchido.

Parâmetro opcional `traco`: se uma lista for passada, registramos nela a ORDEM
em que os nós são explorados (retirados da fronteira). É usado só pela camada de
visualização; por padrão (None) não há custo algum, então as chamadas em massa
da Parte III e do modo online não são afetadas.

Todas as buscas seguem o mesmo esqueleto e diferem apenas na ESTRUTURA DA
FRONTEIRA, que é o que define a ordem de visita dos nós:
    BFS    -> fila (FIFO)                  | collections.deque
    DFS    -> pilha (LIFO)                 | lista usada como pilha
    UCS    -> fila de prioridade por g(n)  | heapq
    Gulosa -> fila de prioridade por h(n)  | heapq
    A*     -> fila de prioridade por f=g+h | heapq
"""
import time
import heapq
from collections import deque
from itertools import count

from core.metricas import Metricas


# --- Funções auxiliares compartilhadas -------------------------------------

def _reconstruir_caminho(veio_de, objetivo):
    """Refaz o caminho do início até o objetivo seguindo os "pais".

    `veio_de` mapeia estado -> estado anterior; o início aponta para None.
    Caminhamos de trás para frente a partir do objetivo e invertemos no fim.
    """
    caminho = []
    atual = objetivo
    while atual is not None:
        caminho.append(atual)
        atual = veio_de[atual]
    caminho.reverse()
    return caminho


def _finalizar(problema, veio_de, objetivo, metricas, tempo_inicial):
    """Preenche as métricas finais quando o objetivo é encontrado."""
    caminho = _reconstruir_caminho(veio_de, objetivo)
    metricas.sucesso = True
    metricas.passos = len(caminho) - 1                  # nº de movimentos
    # Custo do caminho = soma dos custos de entrar em cada célula (menos o início).
    metricas.custo = sum(problema.mapa.custo_entrada(p) for p in caminho[1:])
    metricas.tempo = time.perf_counter() - tempo_inicial
    return caminho, metricas


# --- Buscas não-informadas (sem heurística) --------------------------------

def bfs(problema, traco=None):
    """Busca em Largura. Explora por camadas; encontra o caminho com MENOS
    passos. Só é ótima em custo quando todos os movimentos custam o mesmo."""
    tempo_inicial = time.perf_counter()
    metricas = Metricas()

    fronteira = deque([problema.inicio])
    veio_de = {problema.inicio: None}   # também faz o papel de "já alcançados"
    metricas.fronteira_max = 1

    while fronteira:
        estado = fronteira.popleft()    # FIFO: tira o mais antigo
        metricas.explorados += 1
        if traco is not None:
            traco.append(estado)

        if problema.objetivo_atingido(estado):
            return _finalizar(problema, veio_de, estado, metricas, tempo_inicial)

        metricas.expandidos += 1
        for _acao, sucessor, _custo in problema.sucessores(estado):
            if sucessor not in veio_de:
                veio_de[sucessor] = estado
                fronteira.append(sucessor)
        metricas.fronteira_max = max(metricas.fronteira_max, len(fronteira))

    metricas.tempo = time.perf_counter() - tempo_inicial
    return None, metricas


def dfs(problema, traco=None):
    """Busca em Profundidade. Vai fundo em um ramo antes de retroceder.
    É rápida e gasta pouca memória, mas NÃO garante o melhor caminho."""
    tempo_inicial = time.perf_counter()
    metricas = Metricas()

    fronteira = [problema.inicio]       # lista usada como pilha (LIFO)
    veio_de = {problema.inicio: None}
    metricas.fronteira_max = 1

    while fronteira:
        estado = fronteira.pop()        # LIFO: tira o mais recente
        metricas.explorados += 1
        if traco is not None:
            traco.append(estado)

        if problema.objetivo_atingido(estado):
            return _finalizar(problema, veio_de, estado, metricas, tempo_inicial)

        metricas.expandidos += 1
        # Empilhamos os sucessores em ordem REVERSA: como a pilha é LIFO, isso
        # faz com que eles sejam desempilhados da esquerda para a direita — ou
        # seja, na mesma ordem em que foram gerados (cima, baixo, esquerda,
        # direita). É a convenção padrão de varredura da árvore de estados: o
        # primeiro filho gerado é o primeiro a ser explorado.
        for _acao, sucessor, _custo in reversed(list(problema.sucessores(estado))):
            if sucessor not in veio_de:
                veio_de[sucessor] = estado
                fronteira.append(sucessor)
        metricas.fronteira_max = max(metricas.fronteira_max, len(fronteira))

    metricas.tempo = time.perf_counter() - tempo_inicial
    return None, metricas


def ucs(problema, traco=None):
    """Busca de Custo Uniforme. Expande sempre o nó de menor custo acumulado
    g(n). É ótima mesmo com custos variados (aqui, por causa da lama)."""
    tempo_inicial = time.perf_counter()
    metricas = Metricas()

    ordem = count()                     # desempate estável quando os custos empatam
    fronteira = [(0, next(ordem), problema.inicio)]   # (g, ordem, estado)
    custo_ate = {problema.inicio: 0}    # melhor g(n) conhecido para cada estado
    veio_de = {problema.inicio: None}
    metricas.fronteira_max = 1

    while fronteira:
        custo_atual, _, estado = heapq.heappop(fronteira)
        metricas.explorados += 1
        if traco is not None:
            traco.append(estado)

        # Pode haver entradas "obsoletas" no heap (achamos um caminho melhor
        # depois de inserir esta). Se for o caso, ignoramos.
        if custo_atual > custo_ate.get(estado, float("inf")):
            continue

        if problema.objetivo_atingido(estado):
            return _finalizar(problema, veio_de, estado, metricas, tempo_inicial)

        metricas.expandidos += 1
        for _acao, sucessor, custo in problema.sucessores(estado):
            novo_custo = custo_atual + custo
            if novo_custo < custo_ate.get(sucessor, float("inf")):
                custo_ate[sucessor] = novo_custo
                veio_de[sucessor] = estado
                heapq.heappush(fronteira, (novo_custo, next(ordem), sucessor))
        metricas.fronteira_max = max(metricas.fronteira_max, len(fronteira))

    metricas.tempo = time.perf_counter() - tempo_inicial
    return None, metricas


# --- Buscas informadas (usam a heurística de Manhattan) --------------------

def gulosa(problema, traco=None):
    """Busca Gulosa (best-first). Expande o nó que PARECE mais perto do
    objetivo segundo h(n). É rápida, mas não considera o custo já gasto,
    então pode devolver um caminho pior que o ótimo."""
    tempo_inicial = time.perf_counter()
    metricas = Metricas()

    ordem = count()
    inicio = problema.inicio
    fronteira = [(problema.heuristica(inicio), next(ordem), inicio)]  # (h, ordem, estado)
    veio_de = {inicio: None}
    metricas.fronteira_max = 1

    while fronteira:
        _, _, estado = heapq.heappop(fronteira)
        metricas.explorados += 1
        if traco is not None:
            traco.append(estado)

        if problema.objetivo_atingido(estado):
            return _finalizar(problema, veio_de, estado, metricas, tempo_inicial)

        metricas.expandidos += 1
        for _acao, sucessor, _custo in problema.sucessores(estado):
            if sucessor not in veio_de:
                veio_de[sucessor] = estado
                heapq.heappush(fronteira,
                               (problema.heuristica(sucessor), next(ordem), sucessor))
        metricas.fronteira_max = max(metricas.fronteira_max, len(fronteira))

    metricas.tempo = time.perf_counter() - tempo_inicial
    return None, metricas


def a_estrela(problema, traco=None):
    """A*. Ordena a fronteira por f(n) = g(n) + h(n), equilibrando o custo já
    gasto (g) com a estimativa até o objetivo (h). Com heurística admissível,
    encontra o caminho ótimo geralmente expandindo bem menos nós que a UCS."""
    tempo_inicial = time.perf_counter()
    metricas = Metricas()

    ordem = count()
    inicio = problema.inicio
    # Cada entrada guarda (f, g, ordem, estado): f para priorizar, g para o custo real.
    fronteira = [(problema.heuristica(inicio), 0, next(ordem), inicio)]
    custo_ate = {inicio: 0}
    veio_de = {inicio: None}
    metricas.fronteira_max = 1

    while fronteira:
        _, custo_atual, _, estado = heapq.heappop(fronteira)
        metricas.explorados += 1
        if traco is not None:
            traco.append(estado)

        # Ignora entradas obsoletas (g pior do que o melhor já conhecido).
        if custo_atual > custo_ate.get(estado, float("inf")):
            continue

        if problema.objetivo_atingido(estado):
            return _finalizar(problema, veio_de, estado, metricas, tempo_inicial)

        metricas.expandidos += 1
        for _acao, sucessor, custo in problema.sucessores(estado):
            novo_custo = custo_atual + custo
            if novo_custo < custo_ate.get(sucessor, float("inf")):
                custo_ate[sucessor] = novo_custo
                veio_de[sucessor] = estado
                prioridade = novo_custo + problema.heuristica(sucessor)
                heapq.heappush(fronteira, (prioridade, novo_custo, next(ordem), sucessor))
        metricas.fronteira_max = max(metricas.fronteira_max, len(fronteira))

    metricas.tempo = time.perf_counter() - tempo_inicial
    return None, metricas


# Registro dos algoritmos, na ordem da tabela do enunciado.
ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "Gulosa": gulosa,
    "A*": a_estrela,
}

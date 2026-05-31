"""Hill-Climbing (subida de encosta) para otimizar a ordem de coleta.

Estratégia: a cada passo, examina TODA a vizinhança e move-se para o melhor
vizinho. Para quando nenhum vizinho melhora o custo — esse ponto é um
"mínimo local", que pode ou não ser o ótimo global. É justamente essa limitação
que motiva a têmpera simulada.
"""
from parte3_local.custo import custo_rota
from parte3_local.vizinhanca import vizinhos_por_inversao


def hill_climbing(ordem_inicial, distancias, inicio, objetivo, max_iteracoes=1000):
    """Devolve (melhor_ordem, melhor_custo, historico_de_custos)."""
    atual = list(ordem_inicial)
    custo_atual = custo_rota(atual, distancias, inicio, objetivo)
    historico = [custo_atual]            # custo a cada passo (curva de convergência)

    for _ in range(max_iteracoes):
        melhor_vizinho = None
        melhor_custo = custo_atual
        for vizinho in vizinhos_por_inversao(atual):
            custo_vizinho = custo_rota(vizinho, distancias, inicio, objetivo)
            if custo_vizinho < melhor_custo:
                melhor_custo = custo_vizinho
                melhor_vizinho = vizinho

        if melhor_vizinho is None:       # nenhum vizinho melhora -> mínimo local
            break

        atual, custo_atual = melhor_vizinho, melhor_custo
        historico.append(custo_atual)

    return atual, custo_atual, historico

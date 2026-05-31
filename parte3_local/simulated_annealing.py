"""Simulated Annealing (têmpera simulada) para otimizar a ordem de coleta.

Diferença central em relação ao Hill-Climbing: além de aceitar melhorias, às
vezes ACEITA PIORAS, com probabilidade exp(-Δ/T). Isso permite escapar de
mínimos locais. A temperatura T começa alta (muitas pioras aceitas, exploração)
e cai geometricamente (T *= taxa_resfriamento), passando a aceitar cada vez
menos pioras (refinamento), como no resfriamento de um metal.
"""
import math
import random

from parte3_local.custo import custo_rota
from parte3_local.vizinhanca import vizinho_aleatorio


def simulated_annealing(ordem_inicial, distancias, inicio, objetivo,
                        temp_inicial=100.0, taxa_resfriamento=0.995,
                        temp_minima=1e-3):
    """Devolve (melhor_ordem, melhor_custo, historico_do_melhor_custo)."""
    atual = list(ordem_inicial)
    custo_atual = custo_rota(atual, distancias, inicio, objetivo)
    melhor, melhor_custo = list(atual), custo_atual
    historico = [melhor_custo]
    temperatura = temp_inicial

    while temperatura > temp_minima:
        vizinho = vizinho_aleatorio(atual)
        custo_vizinho = custo_rota(vizinho, distancias, inicio, objetivo)
        delta = custo_vizinho - custo_atual

        # Aceita se melhora (delta < 0); se piora, aceita com probabilidade
        # exp(-delta/T), que diminui conforme a temperatura cai.
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            atual, custo_atual = vizinho, custo_vizinho
            if custo_atual < melhor_custo:
                melhor, melhor_custo = list(atual), custo_atual

        historico.append(melhor_custo)
        temperatura *= taxa_resfriamento

    return melhor, melhor_custo, historico
